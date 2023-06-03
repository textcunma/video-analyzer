import os

from yt_dlp import YoutubeDL

class VideoProcessor:
    """映像に関する処理をするクラス
    """
    def __init__(self, video_name: str, video_path: str, video_url: str) -> None:
        """イニシャライザ（インスタンスの初期化）
        :param video_name 映像ファイル名
        :type video_name str
        :param video_path 映像ファイルのパス名
        :type video_path str
        """
        self._video_name = video_name
        self._video_path = video_path
        self._video_url = video_url

        # 保存ディレクトリ作成
        os.makedirs(video_path, exist_ok=True)

    # 映像ファイルのダウンロード
    def download(self):
        ydl_opts = {'format': 'best', 'outtmpl' : self._save_dir+self._video_name+'.mp4'}
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self._download_url])

    # 映像ファイルの分析
    def analyze(self):
        pass

# テスト用コード
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="コマンドライン引数")
    parser.add_argument(
        "--save_dir", type=str, default="./movie/", help="ダウンロードしたファイルを保存するディレクトリ"
    )
    parser.add_argument("--download_url", default=['https://youtu.be/lgKjhlmTqek'], help="ダウンロードしたい動画のURL")
    args = parser.parse_args()