# Python 代码审查 Agent

使用 DeepSeek API 的入门学习项目。用户指定示例文件后，模型请求调用 `read_file`，Python 读取文件并返回结果，模型再解释代码和提出修改建议。

## 环境与安装

需要 Python 3.10 或更高版本，以及 DeepSeek API Key。以下命令在 Windows PowerShell 中运行，工作目录为本仓库。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

在 `.env` 中填写自己的 `DEEPSEEK_API_KEY`。不要提交或分享 `.env`。模型可通过 `DEEPSEEK_MODEL` 配置，终端中已有的环境变量优先于文件配置。

## 运行

第一课演示基础模型调用，第二课演示工具调用循环：

```powershell
.\.venv\Scripts\python.exe lesson_01.py
.\.venv\Scripts\python.exe lesson_02.py
```

运行其中一个程序后可以输入多行内容，最后单独输入 `/send` 提交。例如第二课输入：

```text
检查 example.py，解释它的功能，找出边界问题并给出修改建议。
/send
```

观察终端中的 `[工具请求]`、`[工具结果]` 和最终回答。工具只读取 `examples` 内不超过 20 KB 的 UTF-8 Python 文件，不执行代码。

## 文件说明

- `lesson_01.py`：模型调用、多行输入和本地配置加载。
- `lesson_02.py`：工具定义、参数检查、工具执行及 Agent 循环。
- `examples/example.py`：用于分析平均值函数边界情况的示例。
- `.env.example`：可分享的配置模板，不包含真实密钥。

## 当前范围

每次运行处理一个用户任务，任务内保留模型和工具消息，最多请求模型 6 轮。支持工具错误反馈和基本 API 错误提示，尚未实现连续用户对话和自动重试。分析基于静态阅读，不能替代代码运行测试。

基础 API 调用及文件工具调用已由使用者实机验证。文件读取、越界拒绝、缺失文件和模拟工具循环已做本地检查。
