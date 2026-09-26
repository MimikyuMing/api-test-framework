# Restful-Booker API 笔记

来源：https://restful-booker.herokuapp.com
记录时间：2026-09-24

## 1. GET /ping

- 方法：GET
- URL：/ping
- 请求体：无
- 响应：201 Created
- 用途：健康检查

## 2. GET /booking

- 方法：GET
- URL：/booking
- 请求体：无
- 响应：200，返回 bookingid 数组
- 用途：列表查询

## 3. GET /booking/{id}

- 方法：GET
- URL：/booking/1
- 请求体：无
- 响应：200，返回 booking 详情
- 已删除的 id 返回 404

## 4. POST /auth

- 方法：POST
- URL：/auth
- 请求体：{"username":"admin","password":"password123"}
- 响应：200，返回 {"token":"..."}
- 用途：更新和删除需要此 token
- token 有效期约 10 分钟

## 5. POST /booking

- 方法：POST
- URL：/booking
- 请求体：booking 对象
- 响应：200，返回 bookingid 和 booking

## 6. PUT /booking/{id}

- 方法：PUT
- URL：/booking/{id}
- 请求头：Cookie: token=xxx
- 请求体：booking 对象
- 响应：200，返回更新后的 booking

## 7. DELETE /booking/{id}

- 响应：实测返回 200 或 201，不稳定
- 以官方文档 201 为准，但断言时接受两者
- 更稳的做法：不断言状态码，断言删除后 GET 返回 404

## 注意事项

- 更新和删除必须带 token，否则返回 403
- 服务端偶尔返回 503，重试即可
- Windows 下 curl 需用 curl.exe，且需加 --ssl-revoke-best-effort
- 用 Python requests 调接口比 curl 更稳

## 异常场景实测

### POST /booking 缺必填字段

- 缺少 `firstname` 时，返回 500
- 服务端未做字段校验，直接内部错误
- 这类 500 是**预期失败**，测试时不应重试

### POST /booking totalprice 边界

- `totalprice: 0`：返回 200，正常创建
- 服务端不校验 totalprice 下限