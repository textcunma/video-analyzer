import os
from typing import Any


class DownloadVideo:
    """1つの映像ファイルをダウンロードするクラス
    """
    def __init__(self, url, save_dir) -> None:
        """
        :param args 引数
        """
        # 保存ディレクトリ作成
        os.makedirs(save_dir, exist_ok=True)

        # プライベートメンバ変数
        self.__save_dir = save_dir
        self.__download_url = args.download_url


    def __call__(self) -> Any:
        pass


# テスト用コード
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="コマンドライン引数")
    parser.add_argument(
        "--download_dir", type=str, default="./movie/", help="ダウンロードしたファイルを置くディレクトリ"
    )
    parser.add_argument("--download_url", default=['https://youtu.be/R9JBN_x9zFQ','https://youtu.be/lgKjhlmTqek'], help="ダウンロードしたい動画のURL")
    args = parser.parse_args()
