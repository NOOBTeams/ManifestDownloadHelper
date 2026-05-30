"""Steam游戏清单下载工具 - 主程序入口"""

import argparse
import sys
from src.steam import SteamManifestDownloader


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Steam游戏清单下载工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py "艾尔登法环"              # 搜索并下载艾尔登法环
  python main.py "elden ring"            # 搜索英文游戏
  python main.py "原神" -n 5            # 显示5个搜索结果
  python main.py -h                     # 显示帮助信息
        """
    )

    parser.add_argument(
        "query",
        help="搜索关键词（游戏名称）"
    )

    parser.add_argument(
        "-n", "--limit",
        type=int,
        default=10,
        help="最大搜索结果数量 (默认: 10)"
    )

    parser.add_argument(
        "-l", "--language",
        default="schinese",
        help="Steam语言代码 (默认: schinese)"
    )

    parser.add_argument(
        "-c", "--country",
        default="CN",
        help="国家代码 (默认: CN)"
    )

    parser.add_argument(
        "--no-translate",
        action="store_true",
        help="禁用自动翻译回退功能"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Steam Manifest Downloader 0.3.0"
    )

    args = parser.parse_args()

    # 创建下载器
    downloader = SteamManifestDownloader()

    # 设置搜索参数
    search_kwargs = {
        'limit': args.limit,
        'language': args.language,
        'country': args.country,
        'translate_fallback': not args.no_translate
    }

    try:
        # 执行搜索和下载
        downloader.search_and_download(args.query, **search_kwargs)
        input("\n\n按任意键退出...")
    except KeyboardInterrupt:
        input("\n\n操作被用户中断")
        sys.exit(1)
    except Exception as e:
        input(f"\n发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()