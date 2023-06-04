"""
エントリーポイント
コマンドライン引数の処理等
"""

import yaml
import argparse

from utils import update_args

parser = argparse.ArgumentParser(description="コマンドライン引数")
parser.add_argument("--download_flg", action="store_false", help="ダウンロードするかのフラグ")
parser.add_argument("--download_url", default=(""), help="ダウンロードしたい動画のURL")
parser.add_argument(
    "--save_dir", type=str, default="./videos/", help="ダウンロードしたファイルを保存するディレクトリ"
)
parser.add_argument(
    "--movie_dir", type=str, default="./videos/", help="映像ファイルが置かれたディレクトリ"
)

global args
args = parser.parse_args()

# ymlファイルに記述された引数で更新
with open("../cfg.yml", "r", encoding="utf-8") as handle:
    options_yaml = yaml.load(handle, Loader=yaml.SafeLoader)
update_args(options_yaml, vars(args))


# 並列処理
# 無名関数
# 型判定
# 高速化
