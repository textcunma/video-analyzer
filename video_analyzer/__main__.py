"""
エントリーポイント
コマンドライン引数の処理等
"""
import yaml
import argparse

from utils import update_args, print_time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from video_processor import VideoDownloader, analyze_net_video, analyze_local_video

parser = argparse.ArgumentParser(description="コマンドライン引数")
parser.add_argument("--download_flg", action="store_false", help="ダウンロードするかのフラグ")
parser.add_argument("--video_urls", nargs="*", type=str, help="ダウンロードしたい動画のURL")
parser.add_argument("--video_paths", nargs="*", type=str, help="ダウンロードしたい動画のURL")
parser.add_argument(
    "--save_dir", type=str, default="./videos/", help="ダウンロードしたファイルを保存するディレクトリ"
)
parser.add_argument(
    "--movie_dir", type=str, default="./videos/", help="映像ファイルが置かれたディレクトリ"
)
parser.add_argument("--max_workers", type=int, default=5, help="実行可能タスクの最大数")
args = parser.parse_args()

# ymlファイルに記述された引数で更新
# [NEW] コンテクストマネージャー
with open("./cfg.yml", "r", encoding="utf-8") as handle:
    options_yaml = yaml.load(handle, Loader=yaml.SafeLoader)
update_args(options_yaml, vars(args))

# 変更不可にするためタプル化
args.video_urls = tuple(args.video_urls)


@print_time
def generate_frame_local():
    """逐次的に実行"""
    for path in args.video_paths:
        analyze_local_video(path)


@print_time
def generate_frame_local_thread():
    """スレッドベースの非同期実行"""
    with ThreadPoolExecutor(max_workers=args.max_workers) as exe:
        for path in args.video_paths:
            exe.submit(analyze_local_video, path)


@print_time
def generate_frame_local_process():
    """プロセスベースの非同期実行"""
    with ProcessPoolExecutor(max_workers=args.max_workers) as exe:
        for path in args.video_paths:
            exe.submit(analyze_local_video, path)


if args.download_flg:
    # 保存先を登録
    VideoDownloader.set_save_dir(args.save_dir)

    with ThreadPoolExecutor(max_workers=args.max_workers) as exe:
        for url in args.video_urls:
            exe.submit(analyze_net_video, url)
else:
    # 速度比較
    generate_frame_local()  # 14.31s
    # generate_frame_local_thread()   # 4.88s
    # generate_frame_local_process()      # 9.1s

# async await
# 高速化(numba)
