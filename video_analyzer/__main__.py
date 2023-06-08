"""
エントリーポイント
コマンドライン引数の処理等
"""
import yaml
import argparse

from video_analyzer.utils import update_args, print_time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from video_analyzer.video_processor import VideoDownloader, analyze_video

parser = argparse.ArgumentParser(description="コマンドライン引数")
parser.add_argument("--download_flg", action="store_false", help="ダウンロードするかのフラグ")
parser.add_argument("--video_urls", nargs="*", type=str, help="ダウンロードしたい動画のURL")
parser.add_argument("--video_paths", nargs="*", type=str, help="ダウンロードしたい動画のURL")
parser.add_argument(
    "--download_save_dir", type=str, default="./videos/", help="ダウンロードしたファイルを保存するディレクトリ"
)
parser.add_argument(
    "--result_save_dir", type=str, default="./result/", help="生成された合成画像を保存するディレクトリ"
)
parser.add_argument("--max_workers", type=int, default=5, help="実行可能タスクの最大数")
parser.add_argument("--mode", default = "default", choices=['default', 'thread', 'process'], help="実行方法")
args = parser.parse_args()

# ymlファイルに記述された引数で更新
with open("./cfg.yml", "r", encoding="utf-8") as handle:
    options_yaml = yaml.load(handle, Loader=yaml.SafeLoader)
update_args(options_yaml, vars(args))

# 変更不可にするためタプル化
args.video_urls = tuple(args.video_urls)


@print_time
def generate_keyframes(paths_or_urls: str, mode: str = "default"):
    if mode == "default":
        # 逐次的に実行
        for path_or_url in paths_or_urls:
            analyze_video(args.result_save_dir, args.download_flg, path_or_url)

    elif mode == "thread":
        # スレッドベースの非同期実行
        with ThreadPoolExecutor(max_workers=args.max_workers) as exe:
            for path_or_url in paths_or_urls:
                exe.submit(
                    analyze_video, args.result_save_dir, args.download_flg, path_or_url
                )

    elif mode == "process":
        # プロセスベースの非同期実行
        with ProcessPoolExecutor(max_workers=args.max_workers) as exe:
            for path_or_url in paths_or_urls:
                exe.submit(
                    analyze_video, args.result_save_dir, args.download_flg, path_or_url
                )
    else:
        print(f"{mode}: This Mode doesn't exist")


if args.download_flg:
    VideoDownloader.set_save_dir(args.download_save_dir)
    generate_keyframes(args.video_urls, mode=args.mode)
else:
    generate_keyframes(args.video_paths, mode=args.mode)
