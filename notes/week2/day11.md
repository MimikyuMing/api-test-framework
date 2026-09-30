# Day 11：Allure 报告

## 一、Allure 的组成

| 组件 | 作用 |
|---|---|
| allure-pytest | pytest 插件，生成 JSON 格式的测试结果 |
| allure 命令行 | 把 JSON 渲染成 HTML 报告 |

两者缺一不可。只装 `allure-pytest`，只能生成 JSON，看不到 HTML。

## 二、常用注解

| 注解 | 作用 | 显示位置 |
|---|---|---|
| @allure.feature | 功能模块 | 报告的 Feature 分组 |
| @allure.story | 子功能 | Feature 下的 Story |
| @allure.title | 用例标题 | 用例列表里显示的名字 |
| @allure.severity | 优先级 | 标记 critical / normal / minor |
| @allure.step | 测试步骤 | 用例详情里的步骤 |
| @allure.description | 描述 | 用例详情 |

## 三、@allure.step 的两种用法

**装饰器：**

```python
@allure.step("发送创建请求")
def send_create_request(client, payload):
    return client.post("/booking", json=payload)
```

**上下文管理器（更常用）：**

```python
with allure.step("发送创建请求"):
    resp = client.post("/booking", json=payload)
```

上下文管理器可以直接写在用例里，不用额外定义函数。

## 四、为什么加步骤

不加步骤，报告只显示用例通过或失败。

加了步骤，报告显示每一步的执行结果：

```
✓ 准备请求数据
✓ 发送创建请求
✗ 校验响应字段
```

失败时一眼看出卡在哪一步。

## 五、报告查看

```powershell
pytest
allure serve reports/allure-results
```

- `allure serve` 启动临时 Web 服务，自动打开浏览器；
- 关闭终端后服务停止；
- 也可以用 `allure generate` 生成静态 HTML，但 `serve` 更方便。

## 六、参数化用例在 Allure 里的显示

参数化用例会显示为多个独立用例，用 `ids` 区分。

```python
@pytest.mark.parametrize("case", CASES, ids=[c["case"] for c in CASES])
```

报告里显示：

```
test_create_booking_data_driven[normal]
test_create_booking_data_driven[zero_price]
test_create_booking_data_driven[missing_firstname]
```

## 七、面试问题补充

### Q1：Allure 和 pytest-html 有什么区别？

- pytest-html 生成单文件 HTML，简单但不支持步骤、分组、附件
- Allure 支持 Feature/Story 分组、步骤、附件（截图、日志）、历史趋势
- Allure 需要额外安装命令行工具，pytest-html 只需 pip 装插件
- 团队协作、报告共享场景，Allure 更专业

### Q2：Allure 报告的数据从哪来？

- `allure-pytest` 插件在测试执行时收集结果
- 结果以 JSON 格式写入 `reports/allure-results/`
- `allure serve` 读取 JSON，渲染成 HTML
- JSON 是原始数据，HTML 是展示层，两者分离

### Q3：@allure.step 和普通函数调用有什么区别？

- 普通函数调用不会在报告里体现
- `@allure.step` 装饰的函数会在报告里显示为独立步骤
- `with allure.step(...)` 的代码块也会显示为步骤
- 步骤是报告的可读性来源，失败时能快速定位

### Q4：Allure 的 severity 有什么用？

- 标记用例优先级：blocker / critical / normal / minor / trivial
- 报告里可以按 severity 筛选
- 适合区分核心用例和边缘用例
- 面试时能说清"我如何标记测试优先级"是加分项

### Q5：Allure 报告里怎么附上请求和响应？

- 用 `allure.attach` 附加文本、图片、HTML
- 常见做法：在 HTTP 客户端里自动附加请求和响应
- 也可以在用例里手动 attach

```python
allure.attach(resp.text, name="response", attachment_type=allure.attachment_type.JSON)
```

### Q6：Allure 报告能保存历史趋势吗？

- 能，但需要 `allure generate` + `allure serve` 配合
- 默认 `allure serve` 只显示当前一次运行
- 历史趋势需要配置 `allure-results` 的累积目录
- CI 里通常用 `allure generate --clean` 生成报告，再用 artifact 保存

### Q7：CI 里怎么集成 Allure？

- GitHub Actions 里跑 pytest，生成 `allure-results`
- 用 `allure generate` 生成 HTML
- 用 `actions/upload-artifact` 上传报告
- 或者用 GitHub Pages 部署报告
- Day 12 会具体实现




