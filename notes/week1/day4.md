# Day 4：HTTP 客户端封装

## 为什么封装

- 避免每个用例重复写 base_url、timeout、headers
- 统一日志、重试、失败处理
- base_url 变化时只改一处

## 核心代码

（见 src/client/http_client.py）

## 关键设计点

| 设计 | 原因 |
|---|---|
| `base_url.rstrip("/")` | 防止拼接出 `//` |
| `requests.Session()` | 复用 TCP 连接，保持 Cookie |
| 只对 5xx 重试 | 4xx 重试无意义 |
| `**kwargs` 透传 | 支持 json/headers/params 等参数 |

## 面试问题补充

### Q1：为什么用 requests.Session()，而不是每次 requests.get？

**回答要点**：
- Session 复用底层 TCP 连接，避免每次重新握手，性能更好
- Session 自动保持 Cookie，登录后的 token 能自动带上
- Session 可以统一设置 headers、auth、proxies
- 每次 requests.get 都会创建新连接，高频请求时开销明显

**追问：Session 是线程安全的吗？**
- 不是。多线程共享一个 Session 需要加锁，或者每个线程用独立 Session
- pytest-xdist 并发时，每个进程有独立 Session，不会有这个问题

---

### Q2：重试为什么只针对 5xx，不针对 4xx？

**回答要点**：
- 5xx 是服务端错误，可能是瞬时故障（如超时、临时过载），重试有机会成功
- 4xx 是客户端错误，请求本身有问题（参数错、无权限、资源不存在），重试不会改变结果
- 部分 3xx 重定向也不该盲目重试，可能造成循环

**追问：超时该不该重试？**
- 该。超时是网络层问题，属于瞬时故障
- 但要注意幂等性：GET、PUT、DELETE 可以重试，POST 重试可能导致重复创建
- 更严谨的做法：给非幂等请求加幂等键，或者只在明确安全时重试

---

### Q3：重试次数怎么定？无限重试行不行？

**回答要点**：
- 不能无限重试，否则会放大服务端压力，也拖慢测试
- 一般 2–3 次足够
- 配合退避策略（指数退避 + 抖动）更好，避免同时重试打爆服务端
- 生产级框架会用 `urllib3.Retry` 或 `tenacity` 做更完整的重试控制

---

### Q4：为什么把日志放在客户端里，而不是每个用例里打？

**回答要点**：
- 客户端是请求的统一入口，在这里打日志能覆盖所有请求
- 用例里打日志容易漏、格式不统一
- 统一日志格式后，出问题时能快速定位是哪次请求、什么响应

---

### Q5：这个封装有什么不足？

**回答要点**：
- 没有做认证自动注入（token 目前还是手动传）
- 没有做请求/响应 schema 校验（后面 pydantic 补）
- 重试没有退避策略，简单粗暴
- 没有区分可重试异常类型（目前所有 RequestException 都重试）
- 日志没有写文件，只输出到控制台

---

### Q6：如果接口需要登录才能访问，你怎么处理？

**回答要点**：
- 用 fixture 在 session 级登录一次，拿到 token
- 把 token 注入到 HttpClient，或者通过 headers 参数传
- 后面 Day 5 会具体实现

---

### Q7：`requests.Session()` 和 `requests.request()` 有什么区别？

**回答要点**：
- `requests.request()` 每次创建新 Session，请求完就丢弃
- `requests.Session()` 手动管理生命周期，可复用连接和 Cookie
- `requests.get()` 等价于 `requests.request("GET", ...)`，内部也是临时 Session


## 补充：重试策略的边界

**问题**：如果测试本身就是在测错误路径（如缺字段返回 500），默认重试会浪费请求，也拖慢测试。

**解决**：`request` 方法加 `retry=None` 参数，允许单次请求覆盖默认重试次数。

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

重试策略要区分“预期失败”和“非预期故障”，不能一刀切