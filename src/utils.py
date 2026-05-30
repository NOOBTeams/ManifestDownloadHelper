"""工具函数模块"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from config import SECRET_KEY


def generate_table(secret_key: str):
    """生成编码表"""
    table = list("0123456789")
    seed = 0
    for i in range(len(secret_key)):
        seed = (seed * 31 + ord(secret_key[i])) & 0xFFFF
    for i in range(len(table) - 1, 0, -1):
        temp = float(seed) * 1103515245.0 + 12345.0
        seed = int(temp) & 0x7FFFFFFF
        j = seed % (i + 1)
        table[i], table[j] = table[j], table[i]
    return table


def encode_appid(appid: str) -> str:
    """编码AppID"""
    table = generate_table(SECRET_KEY)
    sub_string = ''
    sum_val = 0
    for i in appid:
        sub_string += table[int(i)]
        sum_val += int(i)
    length_char = chr(65 + len(appid) - 1)
    check_sum = (sum_val * 7) % 10
    return length_char + str(check_sum) + sub_string


def sanitize_filename(filename: str) -> str:
    """清理文件名，移除非法字符"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()


def generate_filename(game_name: str, appid: int) -> str:
    """生成文件名：游戏名称_appid.zip"""
    safe_name = sanitize_filename(game_name)
    return f"{safe_name}_{appid}.zip"


def ensure_dir(path: str) -> None:
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)


def get_history_file() -> str:
    """获取历史记录文件路径"""
    from config import DATA_DIR
    ensure_dir(DATA_DIR)
    return os.path.join(DATA_DIR, "history.json")


def load_history() -> List[Dict]:
    """加载历史记录"""
    history_file = get_history_file()
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_history(history: List[Dict]) -> None:
    """保存历史记录"""
    history_file = get_history_file()
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def add_to_history(game: Dict, file_path: str, file_size: int) -> None:
    """添加下载记录到历史"""
    history = load_history()
    record = {
        "game": game,
        "timestamp": datetime.now().isoformat(),
        "file_path": file_path,
        "file_size": file_size
    }
    history.insert(0, record)  # 最新记录在最前面
    # 只保留最近100条记录
    if len(history) > 100:
        history = history[:100]
    save_history(history)


def is_ascii(text: str) -> bool:
    """检查文本是否为ASCII"""
    try:
        text.encode("ascii")
        return True
    except UnicodeEncodeError:
        return True