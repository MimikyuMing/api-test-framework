# Day 6：数据驱动 + 参数化

## 一、为什么用数据驱动

**写死的问题**：

- payload 写死在测试函数里
- 想测第二组数据，要么复制函数，要么写 for 循环
- 非开发人员不能加用例

**数据驱动后**：

- 数据放 YAML，代码只写一次
- 新增场景只改 YAML
- 用例列表一目了然

---

## 二、项目结构

| 文件 | 作用 |
|---|---|
| `data/booking_cases.yaml` | 测试数据 |
| `src/utils/data_loader.py` | 读取 YAML |
| `tests/test_booking_data_driven.py` | 参数化用例 |

---

## 三、`@pytest.mark.parametrize` 用法

```python
CASES = load_yaml("booking_cases.yaml")["create_booking"]

@pytest.mark.parametrize("case", CASES, ids=[c["case"] for c in CASES])
def test_create_booking_data_driven(client, case):
    resp = client.post("/booking", json=case["payload"])
    assert resp.status_code == case["expected_status"]
```

| 参数 | 含义 |
|---|---|
| `"case"` | 参数名，测试函数用它接收当前数据 |
| `CASES` | 数据列表，每个元素跑一次 |
| `ids=[...]` | 用例名，输出更可读 |


## 四、重试策略的边界问题
**现象**：`missing_firstname `预期 500，但被重试了 3 次，浪费请求、拖慢测试。

**原因**：`HttpClient` 默认对 5xx 重试，但它不知道这次 500 是预期的。

**解决**：给 `request` 加 `retry` 参数，单次请求可覆盖。

```python
def request(self, method, path, retry=None, **kwargs):
    max_retry = self.retry if retry is None else retry
    ...
```
测试里：

```python
expected = case["expected_status"]
retry = 0 if expected >= 400 else None
resp = client.post("/booking", json=case["payload"], retry=retry)
```
**核心原则**：重试策略要区分“预期失败”和“非预期故障”。

## 五、面试问题补充
### Q1：数据驱动有什么好处？
- 数据和代码分离，改数据不改代码

- 新增场景成本低

- 非开发人员也能加用例

- 用例列表一目了然，覆盖情况清晰

### Q2：数据驱动用什么格式存数据？
常见几种：

| 格式 | 优点 | 缺点 |
|---|---|---|
| YAML | 可读性好，支持嵌套和注释 | 缩进敏感 |
| JSON | 机器友好，通用 | 不支持注释 |
| CSV | 适合表格型数据 | 不支持嵌套 |
| Excel | 非技术人员友好 | 需要额外库，版本控制差 |
| 数据库 | 集中管理，适合大规模 | 需要额外维护 |
选择依据：数据复杂度、谁维护、是否需要版本控制。

### Q3：@pytest.mark.parametrize 的 ids 有什么用？
- 不加 ids：用例名是 [case0]、[case1]，看不出测什么

- 加 ids：用例名是 [normal]、[missing_firstname]，一眼看出哪个失败

- ids 可以是列表，也可以是函数

### Q4：参数化时，用例之间的数据怎么隔离？
- 每次参数化都是一次独立的测试调用

- fixture 如果依赖当前用例数据，要用 function 级

- 不要用模块级变量缓存上一个用例的数据

- 如果用 session 级 fixture，要保证数据不互相污染

### Q5：重试策略为什么不能一刀切？
- 非预期 5xx：可能是临时故障，重试有意义

- 预期 5xx：测试本身测错误路径，重试浪费且语义错

- 4xx：请求本身有问题，重试无效

- 非幂等请求（POST）：重试可能造成重复创建

- 所以要区分“该重试的”和“不该重试的”

### Q6：如何给一个用例单独关掉重试？
- 给 request 方法加 retry 参数，默认用全局配置

- 单次调用传 retry=0 覆盖

- 测试里根据 expected_status 自动决定

- 这是框架灵活性的体现：默认行为 + 单次覆盖

### Q7：数据文件格式错了会怎样？
- YAML 语法错误：yaml.YAMLError

- 文件不存在：FileNotFoundError

- 字段缺失：运行时 KeyError

- 好的做法：加载后校验必要字段，格式错误时抛清晰错误信息

---

## 三、提交

```powershell
git add .
git commit -m "day6: data driven + param + retry boundary + notes"
```


