import os

from yt_dlp import YoutubeDL

class VideoDownloader:
    """1つの映像ファイルをダウンロードするクラス
    """
    def __init__(self, url: str, save_dir: str) -> None:
        """イニシャライザ（インスタンスの初期化）
        :param args 引数
        """
        # 保存ディレクトリ作成
        os.makedirs(save_dir, exist_ok=True)

        # プライベートインスタンス変数(見かけだけプライベート)
        self._save_dir = save_dir
        self._download_url = url
        self._video_name = url.split('/')[-1]

    def __call__(self) -> None:
        ydl_opts = {'format': 'best', 'outtmpl' : self._save_dir+self._video_name+'_.mp4'}
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self._download_url])

# テスト用コード
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="コマンドライン引数")
    parser.add_argument(
        "--save_dir", type=str, default="./movie/", help="ダウンロードしたファイルを保存するディレクトリ"
    )
    parser.add_argument("--download_url", default=['https://youtu.be/lgKjhlmTqek'], help="ダウンロードしたい動画のURL")
    args = parser.parse_args()

    # ダウンロード
    [VideoDownloader(url, args.save_dir)() for url in args.download_url]


