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