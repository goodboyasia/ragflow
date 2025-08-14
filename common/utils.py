# 将 remove_emoji 方法替换为以下实现
import re


def remove_emoji_from_text(text):
    """移除字符串中的emoji和其他特殊符号"""
    # 匹配各种emoji字符的正则表达式
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # 表情符号
        "\U0001F300-\U0001F5FF"  # 符号和图标
        "\U0001F680-\U0001F6FF"  # 交通和地图符号
        "\U0001F1E0-\U0001F1FF"  # 国旗
        "\U00002500-\U00002BEF"  # 各种符号
        "\U00002702-\U000027B0"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # 变体选择器
        "\u3030"
        "\u2022"  # 项目符号
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def remove_emoji(data):
    """递归地从数据结构中移除emoji"""
    if isinstance(data, str):
        return remove_emoji_from_text(data)
    elif isinstance(data, dict):
        return {key: remove_emoji(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [remove_emoji(item) for item in data]
    else:
        return data

print("are you ok?")