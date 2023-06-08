import os
import cv2
import yt_dlp
import numpy as np
import numpy.typing as npt

from typing import Generator
from yt_dlp import YoutubeDL
from utils import print_time_arg, print_time_arg_return


class VideoProcessor:
    """映像処理に関するクラス"""

    def __init__(
        self,
        video_path: str,
        result_save_dir: str = "./result/",
        resize_ratio: float = 0.4,
    ) -> None:
        """

        Args:
            video_path (str): 映像ファイルのパス名
            result_save_dir (str): 処理結果を保存するパス名
            resize_ratio (float): 画像リサイズ比 - 計算負荷を抑えるため
        """
        self._video_path = video_path
        self._video_name = os.path.splitext(os.path.basename(video_path))[0].split("/")[
            -1
        ]
        self._result_save_dir = result_save_dir

        # 画像リサイズ関連
        self._resize_ratio = resize_ratio  # リサイズ比率
        self._new_w = 0  # リサイズ後の幅
        self._new_h = 0  # リサイズ後の高さ
        self._resize_frame = lambda img: cv2.resize(img, (self._new_w, self._new_h))

    def _load_video(self) -> cv2.VideoCapture:
        """OpenCVライブラリを用いて映像を読み込む

        Return:
            cap (cv2.VideoCapture): 映像キャプチャ情報
        """
        cap = cv2.VideoCapture(self._video_path)

        # 例外処理
        if not cap.isOpened():
            print("Failed: open video file")
            exit(1)

        self._new_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * self._resize_ratio)
        self._new_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * self._resize_ratio)
        return cap

    def _calc_hist(self, img: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """ヒストグラムを計算

        Args:
            img (ndarray): 画像情報(3チャンネル)

        Returns:
            hist (ndarray): ヒストグラム(1チャンネル)
        """
        hist: npt.NDArray[np.float64] = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist


class KeyframeExtractor(VideoProcessor):
    """キーフレーム抽出のクラス"""

    def __init__(
        self, video_path: str, result_save_dir: str, synth_frame_columns: int = 6
    ) -> None:
        """

        Args:
            video_path (str): 映像ファイルのパス名
        """
        super().__init__(video_path, result_save_dir)
        os.makedirs(self._result_save_dir, exist_ok="True")

        self._synth_frame_columns = synth_frame_columns  # 合成画像の列数
        self._keyframes_num = 0  # キーフレーム数

    def _extract_keyframes(self, threshold: float = 0.5) -> Generator:
        """ヒストグラムを用いたキーフレーム抽出

        ヒストグラム差分を計算し、その差分がしきい値以上ならばキーフレームとする

        Args:
            threshold (float): しきい値

        Yields:
            keyframes (list): キーフレーム情報リスト
        """
        cap = self._load_video()
        keyframes = []

        ret, frame = cap.read()
        frame = self._resize_frame(frame)
        keyframes.append(frame)  # 1フレーム目は必ずキーフレーム
        self._keyframes_num += 1
        prev_hist = self._calc_hist(frame)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = self._resize_frame(frame)
            cur_hist = self._calc_hist(frame)
            hist_diff = cv2.compareHist(prev_hist, cur_hist, cv2.HISTCMP_BHATTACHARYYA)

            if hist_diff > threshold:
                keyframes.append(frame)
                self._keyframes_num += 1
                prev_hist = cur_hist

                if self._keyframes_num % self._synth_frame_columns == 0:
                    yield keyframes
                    keyframes = []  # 初期化
        cap.release()
        yield keyframes

    @print_time_arg("extract-keyframe")
    def generate_synth_keyframe(self) -> None:
        """合成キーフレーム画像を生成"""
        print(f"generate synthesized keyframe:{self._video_path}")
        synth_img = None
        for frames in self._extract_keyframes():
            if synth_img is None:
                synth_img = cv2.hconcat(frames)
            elif len(frames) == 0:
                break
            else:
                if len(frames) != self._synth_frame_columns:
                    frames += [
                        np.zeros((self._new_h, self._new_w, 3), dtype=np.uint8)
                        for _ in range(self._synth_frame_columns - len(frames))
                    ]
                try:
                    synth_img = cv2.vconcat([synth_img, cv2.hconcat(frames)])
                except:
                    print("Error: Concat Image")
        cv2.imwrite(self._result_save_dir + self._video_name + ".jpg", synth_img)


class VideoDownloader:
    download_save_dir = ""  # ダウンロード保存先

    def __init__(self, video_url: str) -> None:
        """

        Args:
            video_url (str): ダウンロードしたい映像ファイルのurl
        """
        video_name = video_url.split("/")[-1]
        self.video_path = self.download_save_dir + video_name + ".mp4"
        self._video_url = video_url

    @print_time_arg_return("download video")
    def __call__(self) -> bool:
        if not os.path.exists(self.video_path):
            if not self.is_valid_link(self._video_url):
                print("Don't donwoload video")
                return False

            ydl_opts = {"format": "best", "outtmpl": self.video_path}
            with YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([self._video_url])
                except yt_dlp.utils.DownloadError:
                    print("don't exist videos")
                    return False
        else:
            print("Download : already completed")

        return True

    def get_video_path(self) -> str:
        """映像ファイルのパスを出力
        
        Return:
            (str): 映像ファイルのパス名
        """
        return self.video_path

    @staticmethod
    def is_valid_link(url: str) -> bool:
        """YouTubeのURLかどうかを確認(YouTube動画のみダウンロード可能)

        Args:
            url (str): ダウンロードしたい動画のurl
        """
        return True if url.startswith("https://youtu.be") else False

    @classmethod
    def set_save_dir(cls, save_dir: str) -> None:
        """保存先ディレクトリの設定と作成

        Args:
            save_dir (str): 保存先ディレクトリ
        """
        cls.download_save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)


def analyze_video(save_dir: str, download_flg: bool, path_or_url: str) -> None:
    """映像を分析

    Args:
        save_dir (str): 生成結果を保存するディレクトリ名
        download_flg (bool): ダウンロードするかどうか(True: する, False: しない)
        path_or_url (str): 映像ファイルのパス名 or 映像ファイルのURL

    """
    video_path = ""

    if download_flg:
        vd = VideoDownloader(path_or_url)
        if vd():
            video_path = vd.get_video_path()
    else:
        video_path = path_or_url

    ke = KeyframeExtractor(video_path, save_dir)
    ke.generate_synth_keyframe()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="コマンドライン引数")
    parser.add_argument(
        "--download_save_dir",
        type=str,
        default="./videos/",
        help="ダウンロードしたファイルを保存するディレクトリ",
    )
    parser.add_argument(
        "--result_save_dir", type=str, default="./result/", help="生成された合成画像を保存するディレクトリ"
    )
    parser.add_argument(
        "--video_urls",
        default=("https://youtu.be/DCfk7tc_KqE",),
        help="ダウンロードしたい動画のURL",
    )
    args = parser.parse_args()

    # 保存先を登録
    VideoDownloader.set_save_dir(args.download_save_dir)

    for url in args.video_urls:
        analyze_video(args.result_save_dir, True, url)
