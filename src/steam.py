"""Steam游戏清单下载核心功能"""

import json
import random
import requests
import os
import urllib3
from typing import Dict, List, Optional
from tqdm import tqdm
from urllib3.exceptions import InsecureRequestWarning
from config import (
    API_SERVERS, STEAM_SEARCH_API, DEFAULT_HEADERS,
    DEFAULT_LANGUAGE, DEFAULT_COUNTRY, DEFAULT_LIMIT,
    MANIFESTS_DIR, DOWNLOAD_TIMEOUT, MAX_SRC_ATTEMPTS
)
from .utils import encode_appid, generate_filename, ensure_dir, is_ascii, add_to_history

# 禁用SSL验证警告
urllib3.disable_warnings(InsecureRequestWarning)


class SteamManifestDownloader:
    """Steam游戏清单下载器"""

    def __init__(self):
        self.ensure_directories()

    def ensure_directories(self):
        """确保必要的目录存在"""
        ensure_dir(MANIFESTS_DIR)

    def get_random_api(self) -> str:
        """随机选择一个API服务器"""
        return random.choice(API_SERVERS)

    def translate_to_english(self, term: str) -> Optional[str]:
        """翻译为英文"""
        translate_api = (
            "https://translate.googleapis.com/translate_a/single"
            "?client=gtx&sl=auto&tl=en&dt=t&q={}"
        )
        try:
            response = requests.get(
                translate_api.format(requests.utils.quote(term)),
                headers=DEFAULT_HEADERS,
                timeout=10,
                verify=False,
            )
            response.raise_for_status()
            data = response.json()
            translated = "".join(part[0] for part in data[0])
            return translated.strip()
        except Exception:
            return None

    def search_games(self, term: str, **kwargs) -> List[Dict]:
        """搜索游戏"""
        limit = kwargs.get('limit', DEFAULT_LIMIT)
        language = kwargs.get('language', DEFAULT_LANGUAGE)
        country = kwargs.get('country', DEFAULT_COUNTRY)
        translate_fallback = kwargs.get('translate_fallback', True)

        # 首先搜索
        items = self._fetch_store(term, language, country)

        # 如果结果太少且 term 是非 ASCII，尝试翻译
        if translate_fallback and len(items) < limit and not is_ascii(term):
            translated = self.translate_to_english(term)
            if translated and translated.lower() != term.lower():
                translated_items = self._fetch_store(translated, "english", country)
                # 合并结果，去重
                seen = {item.get("id") for item in items}
                for item in translated_items:
                    if item.get("id") not in seen:
                        items.append(item)
                        seen.add(item.get("id"))

        # 格式化结果
        results = []
        for item in items[:limit]:
            image = (
                item.get("tiny_image")
                or item.get("large_capsule_image")
                or item.get("header_image")
                or ""
            )
            results.append({
                "name": item.get("name", ""),
                "appid": item.get("id"),
                "image": image,
            })
        return results

    def _fetch_store(self, term: str, language: str, country: str) -> List[Dict]:
        """从Steam商店获取数据"""
        params = {
            "term": term,
            "l": language,
            "cc": country,
        }
        response = requests.get(
            STEAM_SEARCH_API,
            params=params,
            timeout=15,
            headers=DEFAULT_HEADERS,
            verify=False,
        )
        response.raise_for_status()
        payload = response.json()
        return payload.get("items", [])

    def select_games(self, games: List[Dict]) -> List[Dict]:
        """交互式选择游戏"""
        if not games:
            print("没有找到游戏")
            return []

        print("\n找到以下游戏：")
        for i, game in enumerate(games, 1):
            print(f"{i}. {game['name']} (AppID: {game['appid']})")

        while True:
            try:
                choice = input(f"\n请选择游戏编号 (1-{len(games)})，或输入多个编号用空格分隔: ")
                if choice.lower() == 'q':
                    return []

                indices = [int(x) - 1 for x in choice.split()]
                selected = []
                for idx in indices:
                    if 0 <= idx < len(games):
                        selected.append(games[idx])
                    else:
                        print(f"警告: 编号 {idx + 1} 无效")

                if selected:
                    return selected
                else:
                    print("请至少选择一个游戏")
            except ValueError:
                print("请输入有效的数字编号")

    def download_manifest(self, game: Dict) -> bool:
        """下载游戏清单"""
        appid = str(game['appid'])
        api_base_url = self.get_random_api()
        encoded_id = encode_appid(appid)

        # 生成文件名
        filename = generate_filename(game['name'], game['appid'])
        file_path = os.path.join(MANIFESTS_DIR, filename)

        # 检查文件是否已存在
        if os.path.exists(file_path):
            print(f"文件已存在: {filename}")
            return True

        print(f"\n正在下载 {game['name']}...")

        # 尝试不同的下载源
        for src in range(MAX_SRC_ATTEMPTS):
            download_url = f'{api_base_url}download?id={encoded_id}&src={src}'
            print(f"尝试从 src={src} 下载: {download_url}")

            try:
                with requests.get(download_url, stream=True, timeout=DOWNLOAD_TIMEOUT) as response:
                    response.raise_for_status()

                    # 获取文件大小
                    total_size = int(response.headers.get('content-length', 0))

                    # 下载文件
                    with open(file_path, 'wb') as f, tqdm(
                        desc=f"下载 src={src}",
                        total=total_size,
                        unit='iB',
                        unit_scale=True,
                        unit_divisor=1024,
                    ) as bar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                bar.update(len(chunk))

                    # 获取文件大小
                    file_size = os.path.getsize(file_path)

                    # 添加到历史记录
                    add_to_history(game, file_path, file_size)

                    print(f"✅ 下载成功！文件已保存至: {filename}")
                    return True

            except requests.exceptions.RequestException as e:
                print(f"src={src} 下载失败: {e}")
                if src < MAX_SRC_ATTEMPTS - 1:
                    print("切换到下一个源...\n")
                continue

        print(f"❌ 所有下载源均失败")
        return False

    def search_and_download(self, query: str, **kwargs) -> None:
        """搜索并下载的完整流程"""
        print(f"正在搜索: {query}")

        # 搜索游戏
        games = self.search_games(query, **kwargs)

        if not games:
            print("未找到相关游戏")
            return

        # 显示结果并让用户选择
        selected_games = self.select_games(games)

        if not selected_games:
            print("没有选择任何游戏")
            return

        # 下载选中的游戏
        success_count = 0
        for game in selected_games:
            if self.download_manifest(game):
                success_count += 1

        print(f"\n下载完成: {success_count}/{len(selected_games)} 个游戏下载成功")


def main():
    """测试函数"""
    downloader = SteamManifestDownloader()

    # 测试搜索
    games = downloader.search_games("艾尔登法环")
    print(f"搜索结果: {len(games)} 个游戏")

    # 测试下载第一个游戏
    if games:
        downloader.download_manifest(games[0])


if __name__ == "__main__":
    main()