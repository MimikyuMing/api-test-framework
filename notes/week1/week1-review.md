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