# 第一周复盘

## 完成内容

| Day | 主题 | 产出 |
|---|---|---|
| Day 1 | 环境 + API 探索 | venv、目录结构、api-notes.md |
| Day 2 | pytest + requests 基础 | test_smoke.py、day2.md |
| Day 3 | 配置管理 | config.yaml、config_loader.py、test_config.py、day3.md |
| Day 4 | HTTP 客户端封装 | logger.py、http_client.py、day4.md |
| Day 5 | fixture + 登录鉴权 | conftest.py、test_auth.py、test_booking_crud.py、day5.md |
| Day 6 | 数据驱动 | booking_cases.yaml、data_loader.py、test_booking_data_driven.py、day6.md |
| Day 7 | 闭环用例 + 复盘 | test_booking_flow.py、day7.md、week1-review.md |

## 覆盖的接口

- GET /ping
- GET /booking
- GET /booking/{id}
- POST /auth
- POST /booking
- PUT /booking/{id}
- DELETE /booking/{id}

## 用例数量

- test_smoke.py：2 个
- test_auth.py：2 个
- test_booking_crud.py：5 个
- test_booking_data_driven.py：3 个
- test_booking_flow.py：1 个

合计约 13 个用例。

## 学到的东西

### 框架层

- pytest 的发现规则
- fixture 作用域：function / class / module / session
- conftest.py 的作用和就近优先
- yield fixture 的 setup/teardown
- 参数化 @pytest.mark.parametrize
- 数据驱动：数据和代码分离

### 设计层

- 配置外置，用 YAML
- HTTP 客户端封装：统一 base_url、超时、重试、日志
- 重试要区分预期失败和非预期故障
- 闭环用例和单接口用例的职责不同

### 排错层

- 500 不一定是服务端问题
- 用日志定位请求和响应
- 用最小复现排除测试代码问题

## 还不会 / 需要加强

- Allure 报告（Day 11）
- pydantic schema 校验（Day 9）
- 异常场景和边界值（Day 10）
- GitHub Actions CI（Day 12）
- 断言封装（Day 8）

## 下周计划

- Day 8：断言封装
- Day 9：pydantic 响应校验
- Day 10：异常场景和边界值
- Day 11：Allure 报告
- Day 12：GitHub Actions CI
- Day 13：README + 代码整理
- Day 14：简历描述 + 面试准备

---

# 第一周检测题与点评

## 评分总览

| 分组 | 得分 | 满分 |
|---|---|---|
| 第一组：概念确认 | 43 | 50 |
| 第二组：设计判断 | 45 | 50 |
| 第三组：场景分析 | 22 | 40 |
| 合计 | 110 | 140 |

换算约 78 分。

---

## 第一组：概念确认

### 1. pytest 怎么发现测试用例？

**我的答案**：从 root 的 pytest.ini 找 testpaths，用 test_xx 格式找文件和函数。

**点评**：方向对，但不完整。

漏了两点：

- 文件格式有两种：`test_*.py` **和** `*_test.py`
- 类名规则：类要匹配 `Test*`，类里方法匹配 `test_*`

另外 `test_xx` 是笔误，应该是 `test_*`。

**完整答案**：pytest 从 `testpaths` 开始，找 `test_*.py` 或 `*_test.py` 文件，找 `test_*` 函数，找 `Test*` 类里的 `test_*` 方法。

**评分**：7/10

---

### 2. fixture 有哪四种作用域？

**我的答案**：function、class、module、session；function 是单个函数，class 则是类，module 是模块内，session 是一次会话中。

**点评**：完全正确。

**补充**：实际选择时有个原则——能用小作用域就用小的，因为大作用域容易造成状态污染。但创建成本高时（如登录）用大作用域。

**评分**：10/10

---

### 3. conftest.py 放在不同位置的区别？

**我的答案**：放在 root 目录则是 src 下全局生效，tests 则是仅在 tests 下生效。

**点评**：基本对，但有一处表述不准。

`root` 的 conftest.py 影响的不是"src 下"，而是项目根目录及所有子目录——包括 `src/`、`tests/`，甚至其他任何目录。

**准确说法**：root conftest.py 作用于整个项目；tests/ 下的只作用于 tests/ 及子目录。

**评分**：8/10

---

### 4. fixture 里 return 和 yield 的区别？

**我的答案**：return 是没有后续执行，而 yield 在返回数据之后结束本次用例 test 之后会继续执行后续，一般用于后续需要还原/清除数据用。

**点评**：理解正确，但表述略模糊。

"return 没有后续执行"——这个说法不准确。准确说是：fixture 用 return 时，没有 teardown 阶段。fixture 执行完就结束。

**补充**：teardown 无论用例成功或失败都会执行，这是关键特性。

**评分**：8/10

---

### 5. @pytest.mark.parametrize 的 ids 有什么用？

**我的答案**：将参数进行 id 划分，否则会出现 case0、case1 的下标而不是之前预设定的 case 的 name。

**点评**：正确。

**补充**：`ids` 可以是列表，也可以是函数。当参数化数据是对象或复杂结构时，用函数动态生成 id 更灵活。

**评分**：10/10

---

## 第二组：设计判断

### 6. 为什么重试只针对 5xx，不针对 4xx？

**我的答案**：5xx 一般是服务端问题，而 4xx 则是客户端问题，服务端问题有可能是瞬时的故障（网络波动，过载等），而客户端更多是本身的请求格式，自身网络等问题。

**点评**：核心对，但有一处小错误。

你说"客户端更多是本身的请求格式、自身网络等问题"——自身网络问题不会返回 4xx。网络问题是连接失败，抛 `ConnectionError`，属于 `RequestException`，不是 4xx。4xx 是服务端返回的客户端错误。

**完整答案**：

- 5xx：服务端错误，可能瞬时，重试有意义
- 4xx：服务端告诉客户端"你的请求有问题"，重试无用
- 网络异常（连接失败、超时）：属于另一类，通常也重试

**评分**：7/10

---

### 7. 为什么创建 booking 不需要 token，更新和删除需要？

**我的答案**：Restful 风格认为创建是匿名的，而更新删除需要权限因此需要鉴权，有的，如果设计上认为创建也需要权限的话，也是需要做区分设计，这些因项目的设计而发生变化。

**点评**：正确。

**补充**：这是 Restful-Booker 的设计，不是所有项目的通用规则。真实项目里，有些系统连创建也需要登录。测试框架要能适应不同鉴权规则。

**评分**：10/10

---

### 8. auth_token 为什么用 session 级，new_booking 为什么用 function 级？

**我的答案**：由于 token 是一段时间内可以连续使用的，因此采用 session 方式能更好节省资源，避免反复请求服务器 token 导致耗时、资源占用等问题。而 new_booking 是用于测试 update 的问题，使用 function 是因为有可能在进行单个函数测试的时候，前者可能采用 delete，后续立即接上需要用到 new_booking 的时候，由于不是 function 导致它被移除了，而产生非业务/设计上的问题导致本次测试失败的问题。

**点评**：核心对，但表述可以更清晰。

`new_booking` 用 function 级的根本原因是：每个用例需要独立的测试数据。如果共享，用例执行顺序会互相影响——前一个用例删了 booking，后一个用例查询就 404。

**补充**：这是测试隔离原则——用例之间不能有隐式依赖。

**评分**：8/10

---

### 9. 预期返回 500 的用例为什么不应该走默认重试？

**我的答案**：因为我认为它应该失败，如果他的走向是满足我的预期的，就没有必要重试增加测试的耗时/资源占用，除非设计中需要对重试机制有一定的测试逻辑。

**点评**：正确，而且补了例外情况，很到位。

**补充**：这也是重试策略的一个通用原则——重试要区分"预期失败"和"非预期故障"。

**评分**：10/10

---

### 10. 闭环用例和单接口用例，哪个更重要？

**我的答案**：都很重要，单接口用于测试当前接口是否高可用、正确，而闭环则是用来测试评估业务逻辑是否有误，逻辑闭环是否出现问题。

**点评**：正确。

**补充**：

- 单接口用例定位问题快——失败时知道是哪个接口
- 闭环用例发现问题广——接口都正常，组合起来可能出问题
- 生产级测试两者都要有，但比例可以调整

**评分**：10/10

---

## 第三组：场景分析

### 11. 闭环用例执行到"更新"失败，"创建"已成功，残留数据怎么处理？

**我的答案**：使用类似于 try-finally 的设计思路，保证每次执行之后都会回到最初的起点。

**点评**：思路对，但没说具体怎么实现。

**具体做法**：用 fixture 的 yield 做 teardown。

```python
@pytest.fixture
def new_booking(client):
    resp = client.post("/booking", json=payload)
    booking_id = resp.json()["bookingid"]
    yield booking_id
    # teardown：无论测试成功失败都会执行
    client.delete(f"/booking/{booking_id}", headers=auth_headers)
```

即使测试在"更新"那一步失败，teardown 仍会删除残留数据。

**评分**：7/10

---

### 12. 如果 POST /booking 也开始需要 token，框架怎么改？

**我的答案**：在 conftest 里创建 headers 数据传给测试。

**点评**：可行，但不够优。

**更好的做法**：把认证注入到 HttpClient 本身。比如 HttpClient 加一个 `default_headers`，创建时传入 auth_headers，所有请求自动带上。

```python
client = HttpClient(base_url, default_headers={"Cookie": f"token={token}"})
```

这样测试用例不用每次都传 headers，减少重复。

**我的方案的问题**：每个用例都要显式传 headers，容易漏，维护成本高。

**评分**：6/10

---

### 13. 测试越来越慢，怎么排查？

**我的答案**：先跑一遍，看看在哪个环节 slow，如果每一个环节都是这个问题，先查看是否是网络问题，不是的话，就是判断是否是逻辑问题。

**点评**：方向对，但没说用什么工具。

**补充**：

- pytest 有 `--durations=10` 参数，显示最慢的 10 个用例
- `--durations=0` 显示全部
- 如果怀疑是某个接口慢，可以给 HTTP 客户端加耗时日志
- 如果是网络问题，看超时和重试次数

**评分**：6/10

---

### 14. 如果接口返回的字段经常变，测试怎么设计才能减少维护成本？

**我的答案**：类似第 12 题，在 conftest 里做参数化。

**点评**：方向不对。

第 14 题问的是：如果接口返回的字段经常变，测试怎么减少维护成本。

**正确做法**：

- 用 pydantic 只校验关键字段，不校验所有字段
- 或者只断言业务关心的字段，其他字段忽略
- 如果字段名经常变，说明接口不稳定，可以和开发沟通，或者只在 schema 层面做宽松校验

**和 conftest 无关**，这是断言策略问题。

**评分**：3/10

---

## 薄弱点总结

1. **pytest 发现规则的细节**：漏了 `*_test.py` 和 `Test*` 类
2. **异常类型区分**：网络异常 ≠ 4xx，两者属于不同层
3. **认证注入的设计**：应该注入到客户端，而不是每个用例手动传
4. **字段校验策略**：pydantic 只校验关键字段，不是所有字段
5. **慢测试排查工具**：`--durations` 参数

---

## 后续补充计划

- 第 12 题涉及的认证注入设计，Day 9 或后续重构时补
- 第 14 题涉及的 schema 宽松校验，Day 9（pydantic）会补
- 异常类型层级（`requests.exceptions`），建议单独查文档
- `--durations` 工具，建议 Day 11 接 Allure 时一起用

---

## 一句话总结

概念和设计判断比较扎实，场景分析偏弱。

主要短板在：**异常类型的层次区分**、**框架设计的抽象能力**（认证注入、字段校验策略）、**排查工具的使用**。

这些会在 Day 8–14 逐步补上。
