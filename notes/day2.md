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