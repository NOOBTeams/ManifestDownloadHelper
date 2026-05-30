"""配置管理模块"""

# API服务器列表
API_SERVERS = [
    "https://api.owner-79d.workers.dev/",
    "https://api.fuadnafis917.workers.dev/",
    "https://api-psi-eight-12.vercel.app/",
    "https://api.fuad0.workers.dev/",
    "https://api.owner-eab.workers.dev/",
    "https://api-self-rho-49.vercel.app/",
    "https://api-bakaneko.fly.dev/",
    "https://api-ivory-psi-29.vercel.app/",
    "https://api.nekone-b85.workers.dev/"
]

# Steam API相关配置
STEAM_SEARCH_API = "https://store.steampowered.com/api/storesearch/"
SECRET_KEY = "N4F1S_FU4D_OWN_SYSTEM_2025"
SRCS = 6  # 下载源数量

# 默认搜索参数
DEFAULT_LANGUAGE = "schinese"
DEFAULT_COUNTRY = "CN"
DEFAULT_LIMIT = 10

# HTTP请求头
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}

# 路径配置
MANIFESTS_DIR = "manifests"
DATA_DIR = "data"
HISTORY_FILE = "data/history.json"

# 下载配置
DOWNLOAD_TIMEOUT = 15
MAX_SRC_ATTEMPTS = 6  # 每个服务器尝试的src数量