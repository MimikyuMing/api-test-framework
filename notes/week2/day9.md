# Day 9：pydantic 响应校验

## 一、schema 校验和字段断言的区别

| | schema 校验 | 字段断言 |
|---|---|---|
| 检查什么 | 结构：字段是否存在、类型是否正确 | 值：字段的具体内容 |
| 失败说明 | 接口契约变了 | 业务逻辑错了 |
| 例子 | firstname 字段没了 | firstname 不是 "Jim" |

两者互补，不是替代关系。

## 二、本项目模型

| 类 | 对应什么 | 用途 |
|---|---|---|
| BookingDates | bookingdates 嵌套对象 | 校验 checkin / checkout |
| Booking | booking 详情 | 校验 booking 的全部字段 |
| BookingResponse | 创建接口的返回 | 包含 bookingid 和 booking |

## 三、类型说明

| 字段 | 类型 | 说明 |
|---|---|---|
| firstname | str | 字符串 |
| totalprice | int | 整数 |
| depositpaid | bool | 布尔值 |
| checkin / checkout | date | 日期，pydantic 自动转换 |
| additionalneeds | Optional[str] | 可选字段，默认 None |

## 四、为什么用 date 不用 str

- 用 str："2026-01-01" 和 "abc" 都是合法字符串，无法发现格式错误
- 用 date：pydantic 会尝试解析，格式不对直接报错
- 能发现接口返回的日期格式变了

## 五、断言顺序

状态码 → 结构 → 字段值。

- 状态码不对，后面不用看
- 结构不对，字段断言可能报 KeyError
- 结构对了，再验证具体值

## 六、面试问题补充

### Q1：pydantic 和 jsonschema 有什么区别？

**回答要点**：
- pydantic 是 Python 类型系统驱动的模型，写起来简洁
- jsonschema 用 JSON 描述结构，跨语言
- pydantic 支持自定义校验、类型转换、嵌套模型
- 测试项目里，如果被测对象是 Python 服务，pydantic 更自然

### Q2：schema 校验失败怎么定位问题？

**回答要点**：
- pydantic 的错误信息包含字段名、期望类型、实际值
- 常见错误：字段缺失、类型不对、日期格式错
- 看错误信息里的 loc 字段，定位到具体路径
- 如果是接口变更导致，先和开发确认是否为预期变更

### Q3：schema 校验应该严格到什么程度？

**回答要点**：
- 太严：接口新增字段就报错，维护成本高
- 太松：字段类型变了也不报错，失去意义
- 一般做法：必填字段必须校验，可选字段可选校验，允许额外字段
- pydantic 默认忽略额外字段，可以配置为禁止

### Q4：如果接口返回的字段经常变，怎么处理？

**回答要点**：
- 只校验关键字段，不校验所有字段
- 用 Optional 标记可能缺失的字段
- 如果接口不稳定，和开发沟通，或只在 schema 层面做宽松校验
- 或者把不稳定的字段单独隔离，只对稳定字段做严格校验

### Q5：pydantic 能做类型转换，这是好是坏？

**回答要点**：
- 好：接口返回 "111" 能自动转成 111，兼容性好
- 坏：接口返回 "111" 本该是 int，如果接口真的返回字符串，测试可能不发现
- 严格场景下，配置 pydantic 禁止自动转换（strict mode）
- 默认行为是宽松转换，适合大多数测试场景

### Q6：assert_schema 和其他断言怎么配合？

**回答要点**：
- 先 assert_status_code，确认请求成功
- 再 assert_schema，确认结构正确
- 再 assert_field，确认具体值
- 顺序不能乱：状态码不对时，响应体可能不是 JSON，schema 校验会抛奇怪的错误

### Q7：schema 校验能发现哪些字段断言发现不了的问题？

**回答要点**：
- 字段改名：schema 报字段缺失，字段断言可能返回 None 而不报错
- 字段类型变更：schema 报类型错误，字段断言可能因为值相等而不发现
- 必填字段缺失：schema 直接报错
- 嵌套结构变化：比如 bookingdates 从对象变成字符串

### Q8：为什么 additionalneeds 用 Optional？

**回答要点**：
- Restful-Booker 里 additionalneeds 是可选的
- 有些 booking 有，有些没有
- 用 Optional[str] = None，字段缺失时默认 None，不报错
- 不加 Optional，字段缺失时会报字段缺失错误