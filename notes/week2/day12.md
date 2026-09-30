
# Day 12：GitHub Actions CI

## 一、CI 是什么

Continuous Integration，持续集成。每次代码提交，自动执行构建、测试、检查，尽早发现问题。

## 二、GitHub Actions 是什么

GitHub 提供的 CI 服务，免费额度对个人项目足够。

- 在仓库里放 YAML 文件描述要做什么
- 每次 push 或 PR，GitHub 自动执行
- 执行环境是 GitHub 提供的虚拟机

## 三、本项目 workflow

文件位置：`.github/workflows/test.yml`

触发条件：push 到 main，或向 main 提 PR。

执行步骤：

1. Checkout 代码
2. 装 Python 3.14
3. 装依赖
4. 跑 pytest
5. 下载 Allure CLI
6. 生成 Allure 报告
7. 上传报告作为 artifact

## 四、关键配置

| 配置 | 含义 |
|---|---|
| on: push / pull_request | 触发条件 |
| runs-on: ubuntu-latest | 运行环境 |
| actions/checkout@v4 | 拉代码 |
| actions/setup-python@v5 | 装 Python |
| pip install -r requirements.txt | 装依赖 |
| pytest | 跑测试 |
| if: always() | 即使测试失败也执行后续步骤 |
| actions/upload-artifact@v4 | 上传报告 |

## 五、为什么用 if: always()

- 测试失败时，也想看 Allure 报告
- 不加 if: always()，pytest 失败后后续步骤会跳过
- 报告生成和上传都应该用 if: always()

## 六、关于 Node.js 20 弃用警告

GitHub Actions 正在从 Node.js 20 升级到 24。

- 警告不影响功能
- 等官方更新 action 版本后，改版本号即可
- 不需要现在处理

## 七、关于 ubuntu-latest 迁移提示

`ubuntu-latest` 将来会指向 Ubuntu 26。

- 目前不影响
- 真出问题时，锁定具体版本，如 `ubuntu-24.04`

## 八、面试问题补充

### Q1：CI 和本地跑测试有什么区别？

- 本地跑靠自觉，容易忘记
- CI 每次提交自动跑，不会漏
- CI 环境干净，能发现"本地能跑但换个环境就挂"的问题
- CI 结果对团队可见，PR 里有状态标记

### Q2：CI 里测试失败了怎么办？

- 看 Actions 页面的失败步骤
- 看日志：哪个用例失败、什么断言、什么响应
- 下载 Allure 报告，看步骤级的失败位置
- 区分：代码问题、环境问题、外部依赖问题

### Q3：测试依赖外部服务（如 Restful-Booker），CI 稳定性怎么保证？

- 外部服务挂了，CI 会失败，这是真实风险
- 缓解方式：
  - 加重试（已有 pytest-rerunfailures）
  - 区分"真失败"和"外部服务不可用"
  - 极端情况用 mock 替代外部依赖
- 面试可讲：测试依赖外部的权衡

### Q4：CI 里怎么保存测试报告？

- 生成 HTML 报告（allure generate）
- 用 actions/upload-artifact 上传
- 在 Actions 页面可以下载
- 进一步：部署到 GitHub Pages，或集成到 PR 评论

### Q5：CI 和 CD 有什么区别？

- CI：持续集成，自动构建和测试
- CD：持续交付/部署，自动发布到环境
- 本项目只做 CI，不做 CD（测试框架不需要部署）
- 真实项目里，CI 通过后触发 CD 部署到测试环境或生产

### Q6：workflow 里的 secrets 怎么用？

- 敏感信息（token、密码）不写在 YAML 里
- 用 GitHub Secrets 存储，workflow 里用 `${{ secrets.XXX }}` 引用
- 本项目不需要，因为用的是公开练习 API 的固定账号
- 真实项目里，测试账号密码、API key 都要用 secrets

### Q7：怎么让 CI 只在特定分支跑？

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
```

- 指定分支列表
- 也可以用路径过滤：只在某些文件变更时触发

### Q8：CI 跑得慢怎么优化？

- 用缓存：actions/cache 缓存 pip 依赖
- 并行执行：pytest-xdist 多进程
- 只跑受影响的用例：pytest-testmon 或自定义选择逻辑
- 减少外部依赖：用 mock 替代真实 API
