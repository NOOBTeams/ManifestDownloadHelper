import os
import random
import requests
from tqdm import tqdm
from constraints import API_SERVERS, SECRET_KEY, SRCS

MANIFEST_SAVE_DIR = 'manifest'
os.makedirs(MANIFEST_SAVE_DIR, exist_ok=True)


def get_random_api():
    return random.sample(API_SERVERS, 1)[0]


def generate_table(secret_key: str):
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


TABLE = generate_table(SECRET_KEY)


def encode_appid(appid: str):
    sub_string = ''
    sum = 0
    for i in appid:
        sub_string += TABLE[int(i)]
        sum += int(i)
    length_char = chr(65 + len(appid) - 1)
    check_sum = (sum * 7) % 10
    return length_char + str(check_sum) + sub_string


def main(appid: str):
    api_base_url = get_random_api()
    encoded_id = encode_appid(appid)
    api_url = f'{api_base_url}proxy?id={encoded_id}'
    print(f"Proxy URL: {api_url}")

    # 定义你要保存在本地的文件名 (可以根据实际下载的文件类型改后缀)
    local_filename = f"{appid}_download.zip"
    file_path = os.path.join(MANIFEST_SAVE_DIR, local_filename)
    download_success = False

    for i in range(SRCS):
        download_url = f'{api_base_url}download?id={encoded_id}&src={i}'
        print(f"正在尝试从 src={i} 下载: {download_url}")

        try:
            with requests.get(download_url, stream=True, timeout=15) as response:
                response.raise_for_status()

                # 获取文件总大小 (如果服务器没返回 content-length，默认设为 0)
                total_size = int(response.headers.get('content-length', 0))

                # 配置 tqdm 进度条
                with open(file_path, 'wb') as f, tqdm(
                        desc=f"下载 src={i}",  # 进度条前面的文字描述
                        total=total_size,  # 文件的总字节数
                        unit='iB',  # 单位后缀 (如 KiB, MiB)
                        unit_scale=True,  # 自动根据大小转换单位 (比如把 byte 转成 MB)
                        unit_divisor=1024,  # 按照 1024 进制转换
                ) as bar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            # 核心：每次写入后，更新进度条前进 len(chunk) 个字节
                            bar.update(len(chunk))

            print(f"✅ 下载成功！文件已保存至: {local_filename}")
            download_success = True
            break

        except requests.exceptions.RequestException as e:
            # 捕获请求失败 (如网络不通、404、超时等)
            print(f"src={i} 下载失败: {e}")
            print("切换到下一个 src...\n")
            continue

    if not download_success:
        print("所有 src 均下载失败。")


if __name__ == '__main__':
    main("774181")
