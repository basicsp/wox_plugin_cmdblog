import re

def pertty(text):
    """替换Markdown中的部分特殊符号，支持代码块，便于wox复制"""
    return text.replace("```", "").replace("\n", "")


if __name__ == "__main__":
    print(pertty("""`1111`
    1234"""))
