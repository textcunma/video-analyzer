"""
エントリーポイント
コマンドライン引数の処理等
"""

import yaml
import argparse

from utils import update_args
from video_processor import VideoDownloader, KeyframeExtractor

parser = argparse.ArgumentParser(description="コマンドライン引数")
parser.add_argument("--download_flg", action="store_false", help="ダウンロードするかのフラグ")
parser.add_argument("--video_urls", default=("",), help="ダウンロードしたい動画のURL")
parser.add_argument("--video_paths", default=("",), help="ダウンロードしたい動画のURL")
parser.add_argument(
    "--save_dir", type=str, default="./videos/", help="ダウンロードしたファイルを保存するディレクトリ"
)
parser.add_argument(
    "--movie_dir", type=str, default="./videos/", help="映像ファイルが置かれたディレクトリ"
)

args = parser.parse_args()

# ymlファイルに記述された引数で更新
# [NEW] コンテクストマネージャー
with open("../cfg.yml", "r", encoding="utf-8") as handle:
    options_yaml = yaml.load(handle, Loader=yaml.SafeLoader)
update_args(options_yaml, vars(args))

if args.download_flg:
    for url in args.video_urls:
        vd = VideoDownloader(url, args.save_dir)
        vd()
        vd.generate_synth_keyframe()
else:
    for path in args.video_paths:
        ke = KeyframeExtractor(path)
        ke.generate_synth_keyframe()

# 並列処理
# 型判定（mypy）
# 高速化(numba)
