# Day 5：fixture 设计 + 登录鉴权

## 一、fixture 作用域

| 作用域 | 生命周期 | 适用场景 |
|---|---|---|
| function | 每个测试函数一次 | 测试数据、临时资源 |
| class | 每个测试类一次 | 类内共享 |
| module | 每个测试文件一次 | 文件内共享 |
| session | 整个会话一次 | 登录 token、全局客户端 |

选择原则：能用更小作用域就用更小，避免状态污染；但高频创建成本高时用大作用域。

---

## 二、conftest.py

- pytest 自动发现，不需要 import
- 放在哪一层，fixture 就作用于那一层及以下
- 本项目放在 `tests/conftest.py`
- 根目录的 conftest.py 作用于整个项目；tests/ 下的只作用于测试
- 多层 conftest.py 可以共存，同名 fixture 就近优先

---

## 三、本项目 fixture 设计

| fixture | 作用域 | 依赖 | 作用 |
|---|---|---|---|
| config | session | 无 | 读取 config.yaml |
| client | session | config | 创建 HttpClient |
| auth_token | session | client, config | 调 /auth 拿 token |
| auth_headers | session | auth_token | 包装 Cookie 头 |
| new_booking | function | client | 每个用例独立 booking |

依赖关系：
config → client → auth_token → auth_headers
client → new_booking


---

## 四、关键规则

- session 级 fixture 不能依赖 function 级 fixture，否则报错
- fixture 同名时，就近优先
- yield 前是 setup，yield 后是 teardown
- teardown 无论用例成功还是失败都会执行

---

## 五、面试问题补充

### Q1：fixture 的作用域有哪些？怎么选？

- function：每个用例都新建，适合会互相污染的数据
- class：类内共享
- module：文件内共享
- session：全局共享，适合登录 token、数据库连接
- 选择原则：能用更小作用域就用更小；但高频创建成本高时用大作用域

---

### Q2：fixture 能不能依赖另一个 fixture？

- 能，把依赖的 fixture 名写在参数里
- pytest 会自动先创建被依赖的 fixture
- 作用域必须兼容：session 不能依赖 function，否则报错

---

### Q3：conftest.py 放在项目根目录和放在 tests/ 下有什么区别？

- 根目录：作用于整个项目，包括 src/
- tests/：只作用于 tests/ 及子目录
- 一般测试 fixture 放 tests/，跨层共享的放根目录
- 多层 conftest.py 可以共存，就近优先

---

### Q4：登录 token 为什么用 session 级，不用 function 级？

- 登录是有成本的（网络请求 + 服务端计算）
- 每个用例都登录一次会拖慢测试
- token 在有效期内是共享的，不需要每次重新拿
- 但要注意 token 过期：如果测试跑很久，需要处理过期刷新

---

### Q5：new_booking 为什么用 function 级？

- 每个用例都需要独立的 booking
- 如果共享，前一个用例删了，后一个就 404
- 测试数据互相隔离，避免执行顺序影响结果
- 代价是创建成本，但 API 调用很快，可以接受

---

### Q6：fixture 的 yield 和 return 有什么区别？

**在普通 Python 函数里：**

- `return`：函数执行到 return 就结束，返回值给调用方，只有一次。
- `yield`：函数变成生成器。调用时不会立即执行，每次 `next()` 才执行到下一个 yield，暂停在那里，下次继续。

**在 pytest fixture 里：**

用 `return`：

```python
@pytest.fixture
def user():
    return {"name": "Tom"}
```
- 返回数据给测试函数

- 没有清理逻辑

- fixture 执行完就结束

用 `yield`：

```python
@pytest.fixture
def user():
    print("setup：创建用户")
    user = {"name": "Tom"}
    yield user
    print("teardown：删除用户")
```

执行顺序：

1. 测试开始前，pytest 调用 fixture

2. 执行到 yield user，把 user 交给测试函数

3. fixture 暂停在这里，不结束

4. 测试函数执行

5. 测试函数结束后，pytest 回到 fixture 的 yield 之后，继续执行

6. 执行 teardown，fixture 真正结束


**本项目示例：**
```python
@pytest.fixture
def new_booking(client):
    payload = {...}
    resp = client.post("/booking", json=payload)
    booking_id = resp.json()["bookingid"]
    yield booking_id, payload          # 测试函数在这里拿到数据
    # ↓ 测试函数跑完后，回到这里
    client.delete(f"/booking/{booking_id}", headers=...)
```
一句话总结：
| | return | yield |
|---|---|---|
| fixture 里有几次 | 只能一次 | 只能一次 |
| 测试前提供数据 | 是 | 是 |
| 测试后能清理 | 不能 | 能 |
| 本质 | 普通返回值 | 生成器暂停 |


### Q7：如果 fixture 里 assert 失败会怎样？
- fixture 报错，所有依赖它的用例都会标记为 ERROR，不是 FAILED

- ERROR 表示用例没跑起来，FAILED 表示用例跑了但断言失败

- 所以 auth_token 里 assert 失败，会导致整个会话的鉴权用例都 ERROR

### Q8：测试数据怎么隔离？
function 级 fixture 创建独立数据

- 用唯一标识（时间戳、uuid）避免冲突

- teardown 清理数据

- 不要依赖测试执行顺序

- 并发执行时也要考虑隔离

### Q9：conftest.py 中 fixture 的定义顺序有没有要求？
- 定义顺序不重要。pytest 按依赖关系和作用域自动决定创建顺序。

- 如果 b 依赖 a，即使 b 定义在 a 前面，pytest 也会先创建 a。

- 多个 fixture 作用域不同时，按作用域从大到小创建：session → module → class → function。

- 同名 fixture 就近覆盖：目录越深，优先级越高。

### Q10：setup 和 teardown 是什么？
- setup：测试执行前的准备动作，如创建连接、登录、造数据。

- teardown：测试执行后的清理动作，如删数据、断开连接、登出。

- pytest 用 fixture 的 yield 实现：yield 之前是 setup，yield 之后是 teardown。

- unittest 用 setUp / tearDown 方法。

- teardown 即使测试失败也会执行，保证资源被清理。

**执行顺序：**

1. fixture setup（yield 之前）

2. 注入返回值给测试函数

3. 执行测试函数

4. 测试函数结束（成功或失败）

5. fixture teardown（yield 之后）

6. 下一个用例

**什么时候需要 teardown：**
| 场景 | teardown 做什么 |
|---|---|
| 创建了数据库记录 | 删除记录 |
| 打开了文件 | 关闭文件 |
| 建立了网络连接 | 断开连接 |
| 登录了账号 | 登出 |
| 启动了进程 | 终止进程 |
| 创建了临时目录 | 删除目录 |

**什么时候不需要 teardown：**

- 只读操作：GET 请求、读配置

- 无状态资源：纯函数返回值


### Q11：DELETE 返回 200 和 201 不一致，怎么处理？
**问题现象：**

- 手动调 try_crud.py 时，DELETE 返回 200

- pytest 里跑时，DELETE 返回 201

- 官方文档写的是 201

**原因：**Restful-Booker 是公开练习 API，行为不稳定。

**两种处理方式：**

方式 A：接受多个状态码

```python
assert resp.status_code in (200, 201), f"意外状态码: {resp.status_code}"
```
方式 B（推荐）：不断言状态码，断言业务效果

```python
client.delete(f"/booking/{booking_id}", headers=auth_headers)
resp = client.get(f"/booking/{booking_id}")
assert resp.status_code == 404
```
**为什么不推荐方式 A：**

- 状态码是接口实现细节，可能变

- 业务行为（删除后查不到）不会变

- 面试时如果问“你怎么处理不稳定的接口”，这是个好例子

- 核心原则：测行为，不测实现
