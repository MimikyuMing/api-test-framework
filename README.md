
# API Test Framework

基于 pytest 的接口自动化测试框架，支持数据驱动、环境切换、断言封装、Allure 报告与 GitHub Actions CI。

[![API Tests](https://github.com/MimikyuMing/api-test-framework/actions/workflows/test.yml/badge.svg)](https://github.com/MimikyuMing/api-test-framework/actions/workflows/test.yml)

## 技术栈

- Python 3.14
- pytest
- requests
- pydantic
- allure-pytest
- GitHub Actions

## 目录结构

```
api-test-framework/
├── config/                  # 配置
│   └── config.yaml
├── data/                    # 测试数据
│   └── booking_cases.yaml
├── src/
│   ├── client/
│   │   └── http_client.py   # HTTP 客户端封装
│   ├── models/
│   │   └── booking.py       # pydantic 数据模型
│   └── utils/
│       ├── assert_util.py   # 断言封装
│       ├── config_loader.py # 配置加载
│       ├── data_loader.py   # 数据加载
│       └── logger.py        # 日志
├── tests/
│   ├── conftest.py          # fixture 定义
│   ├── test_auth.py
│   ├── test_booking_crud.py
│   ├── test_booking_data_driven.py
│   ├── test_booking_flow.py
│   ├── test_negative.py
│   ├── test_schema.py
│   └── test_smoke.py
├── reports/                 # Allure 报告输出
├── requirements.txt
├── pytest.ini
└── README.md
```

## 安装

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

## 运行测试

```bash
pytest
```

## 查看 Allure 报告

```bash
allure serve reports/allure-results
```

需要先安装 Allure 命令行工具：https://github.com/allure-framework/allure2/releases

## 如何新增用例

1. 在 `data/` 下加 YAML 数据（如果数据驱动）
2. 在 `tests/` 下加测试函数
3. 用 `@pytest.mark.parametrize` 读取 YAML 数据
4. 用 `assert_util` 里的断言函数

## 框架特性

- **数据驱动**：测试数据放在 YAML，新增场景不改代码
- **fixture 分层**：session 级复用登录 token，function 级隔离测试数据
- **HTTP 客户端封装**：统一 base_url、超时、重试、日志
- **断言封装**：统一失败信息格式，便于定位
- **schema 校验**：pydantic 模型校验响应结构
- **重试策略**：只对 5xx 重试，预期失败不重试
- **Allure 报告**：Feature/Story 分组、步骤、优先级
- **CI**：每次 push 自动跑测试，报告作为 artifact 上传

## 被测对象

Restful-Booker 公开 API：https://restful-booker.herokuapp.com

## 已知限制

- 依赖公网服务，服务不可用时测试会失败
- Allure 报告需本地安装 Allure CLI 才能查看
- 未做并发测试、Mock 测试、数据库校验

## 后续计划

- [ ] 增加并发执行（pytest-xdist）
- [ ] 增加 Mock 外部依赖
- [ ] 添加代码覆盖率检查



