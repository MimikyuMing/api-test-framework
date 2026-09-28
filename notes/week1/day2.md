# Day 2：pytest 与 requests 基础

## pytest 测试发现规则

pytest 按顺序查找测试：

1. 从 `pytest.ini` 的 `testpaths` 开始（本项目为 `tests`）
2. 文件必须匹配 `test_*.py` 或 `*_test.py`
3. 函数必须匹配 `test_*`
4. 类必须匹配 `Test*`，类里的方法必须匹配 `test_*`

不满足上述规则的，pytest 不会执行。

## assert 规则

- Python 关键字，条件为 False 时抛 `AssertionError`
- pytest 把 AssertionError 标记为测试失败
- 可以写失败提示：`assert 条件, "失败信息"`
- 失败时 pytest 显示：出错代码行、失败信息、表达式实际结果

## pytest 常用命令

| 命令 | 含义 |
|---|---|
| `pytest` | 运行所有测试 |
| `pytest -v` | 详细输出 |
| `pytest tests/test_smoke.py` | 只运行指定文件 |
| `pytest tests/test_smoke.py::test_ping` | 只运行指定用例 |
| `pytest --collect-only` | 只收集，不执行 |
| `pytest -k "keyword"` | 按名称过滤 |
| `pytest -x` | 第一个失败后停止 |
| `pytest --lf` | 只运行上次失败的用例 |

## requests 基础

| 写法 | 含义 |
|---|---|
| `requests.get(url)` | 发送 GET |
| `requests.post(url, json=payload)` | 发送 POST，`json=` 自动序列化并设置 Content-Type |
| `requests.post(url, data=payload)` | 发送 POST，`data=` 用于表单 |
| `resp.status_code` | HTTP 状态码 |
| `resp.json()` | 把响应体解析为 dict/list |
| `resp.text` | 响应体原文 |
| `resp.headers` | 响应头 |

## 关键区别

- `json=` 与 `data=`：前者发 JSON，后者发表单
- `resp.json()` 与 `resp.text`：前者解析，后者原文
- 状态码断言和字段断言应放在不同 assert，失败时更清晰

## 面试问题补充

### Q1：pytest 和 unittest 有什么区别？为什么选 pytest？

**回答要点**：
- pytest 用例用 `assert`，unittest 必须用 `self.assertEqual` 等方法
- pytest 支持 fixture 依赖注入，unittest 用 setUp/tearDown，作用域固定
- pytest 支持 `@pytest.mark.parametrize` 参数化，unittest 需要用 subTest 或 ddt
- pytest 插件生态丰富：allure、rerunfailures、xdist、cov
- pytest 能直接运行 unittest 用例，反过来不行

---

### Q2：pytest 是怎么发现测试的？

**回答要点**：
- 从 `testpaths` 指定的目录开始
- 文件名匹配 `test_*.py` 或 `*_test.py`
- 函数名匹配 `test_*`
- 类名匹配 `Test*`，类里方法匹配 `test_*`
- 类不能有 `__init__`，否则不会被收集

---

### Q3：assert 失败时，pytest 会显示什么？

**回答要点**：
- 出错代码行
- 自定义失败提示（如果写了）
- pytest 自己推导的表达式实际值
- 这是 pytest 的 assertion rewriting 机制：导入时重写 AST，插入中间变量

---

### Q4：`resp.json()` 和 `resp.text` 有什么区别？

**回答要点**：
- `resp.text` 是响应体原文，字符串
- `resp.json()` 把响应体解析为 Python 对象（dict/list）
- 如果响应不是合法 JSON，`resp.json()` 会抛 `JSONDecodeError`
- 调试时先看 `resp.text`，再决定是否 `resp.json()`

---

### Q5：`json=` 和 `data=` 有什么区别？

**回答要点**：
- `json=payload`：序列化为 JSON，自动设置 `Content-Type: application/json`
- `data=payload`：dict 会被编码为表单，`Content-Type: application/x-www-form-urlencoded`
- `data=` 传字符串时直接作为请求体，不编码
- 测试 JSON 接口用 `json=`，测试表单接口用 `data=`