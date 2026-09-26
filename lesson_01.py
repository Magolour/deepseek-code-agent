"""第一课：向 DeepSeek 发送一条消息，并显示回答。"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


def read_question():
    """逐行收集问题，单独输入 /send 后提交；保留代码缩进和空行。"""
    print("请输入问题，可以粘贴多行代码。结束后另起一行输入 /send 并回车。")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "/send":
            break
        lines.append(line)
    return "\n".join(lines)


def main():
    # 从脚本所在目录加载配置，因此从其他目录启动也能找到 .env。
    # 已有的终端环境变量优先，不会被文件覆盖。
    load_dotenv(Path(__file__).resolve().parent / ".env", encoding="utf-8-sig")
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key or api_key == "replace_with_your_key":
        raise SystemExit("请在脚本旁的 .env 文件中填写 DEEPSEEK_API_KEY，再运行程序。")

    # SDK 负责网络通信；base_url 决定请求发送给 DeepSeek。
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
        timeout=60.0,
        max_retries=0,
    )

    question = read_question()
    if not question.strip():
        raise SystemExit("问题不能为空，请重新运行并输入问题。")

    # 消息列表：系统消息规定回答方式，用户消息承载本次问题。
    messages = [
        {"role": "system", "content": "你是 Python 助教，请用简短的中文和小例子回答。"},
        {"role": "user", "content": question},
    ]

    print("正在等待模型回答……")
    response = client.chat.completions.create(
        model=os.environ.get("DEEPSEEK_MODEL", "deepseek-flash"),
        messages=messages,
        stream=False,
    )

    # choices 是候选回答列表，[0] 取第一个回答。
    print("\n模型回答：")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
