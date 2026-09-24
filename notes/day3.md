# Day 3：配置管理

## 为什么配置要外置

- 代码里写死 base_url，改环境要改代码
- 配置外置后，改 YAML 就行，代码不动
- 面试常问：环境与配置分离

## YAML 语法要点

- 用空格缩进，不能用 Tab
- 冒号后面要有一个空格
- 字符串一般不加引号，除非含特殊字符
- `#` 开头是注释
- 支持嵌套：缩进表示层级

## 配置加载器写法

```python
from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "config.yaml"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


        
---

## 收尾二：提交一次 Git

确认在项目根目录，运行：

```powershell
git add .
git commit -m "day3: config yaml + config loader + test"



## 面试问题补充

### Q1：为什么配置要外置，不写在代码里？

**回答要点**：
- 环境切换（本地/测试/预发/生产）只需改 YAML，代码不动
- 敏感信息（账号、token）不硬编码在代码里
- 非开发人员也能改配置
- 符合 12-Factor App 的 config 原则

---

### Q2：为什么用 YAML，不用 JSON 或 INI？

**回答要点**：
- YAML 支持注释，JSON 不支持
- YAML 支持嵌套和多行字符串，INI 只有扁平键值对
- YAML 可读性好，适合配置文件
- 缺点：缩进敏感，容易写错；解析比 JSON 慢
- JSON 适合机器交互，YAML 适合人写配置

---

### Q3：为什么用 `yaml.safe_load` 而不是 `yaml.load`？

**回答要点**：
- `yaml.load` 可以反序列化任意 Python 对象，有代码执行风险
- `safe_load` 只解析基本类型：str、int、float、bool、list、dict、None
- 配置文件不需要复杂对象，用 `safe_load` 就够，也更安全

---

### Q4：`Path(__file__).parent.parent.parent` 是什么意思？

**回答要点**：
- `__file__` 是当前文件路径
- `.parent` 一次是上一级目录
- 这里从 `src/utils/config_loader.py` 往上退三层到项目根
- 好处：无论从哪里运行，路径都正确
- 替代方案：环境变量、`importlib.resources`

---

### Q5：如果配置里有敏感信息怎么办？

**回答要点**：
- 不把敏感信息写进 `config.yaml`，用环境变量或 `.env` 文件
- `.env` 加入 `.gitignore`，不提交
- 代码用 `os.environ` 或 `python-dotenv` 读取
- CI 里用 GitHub Secrets 注入

---

### Q6：配置加载失败会怎样？怎么处理？

**回答要点**：
- 文件不存在：`FileNotFoundError`
- YAML 格式错：`yaml.YAMLError`
- 缺字段：`KeyError`（使用时才报）
- 更好的做法：加载后校验必填字段，缺失时抛明确错误