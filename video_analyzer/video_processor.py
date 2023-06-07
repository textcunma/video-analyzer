import os
import cv2
import yt_dlp
import numpy as np
import numpy.typing as npt

from typing import Generator
from yt_dlp import YoutubeDL
from utils import print_time_arg, print_time_arg_return

class KeyframeExtractor:
    """映像のキーフレーム抽出のクラス"""

    def __init__(self, video_path: str) -> None:
        """イニシャライザ（インスタンスの初期化）
        Args:
            video_path (str): 映像ファイルのパス名
        """
        self._video_path = video_path
        self._video_name = os.path.splitext(os.path.basename(video_path))[0].split("/")[
            -1
        ]
        self._synth_frame_columns = 6  # 合成画像の列数
        self._new_w = 0  # リサイズ後の幅
        self._new_h = 0  # リサイズ後の高さ
        self._keyframes_num = 0
        self._resize_ratio = 0.4
        self._resize_frame = lambda img: cv2.resize(
            img, (self._new_w, self._new_h)
        )  # [NEW] 無名関数

    def _load_video(self) -> cv2.VideoCapture:
        """OpenCVライブラリを用いて映像を読み込む
        Return:
            cap (cv2.VideoCapture): 映像キャプチャ情報
        """
        cap = cv2.VideoCapture(self._video_path)

        # 例外処理
        if not cap.isOpened():
            print("Failed")
            return

        self._new_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * self._resize_ratio)
        self._new_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * self._resize_ratio)
        return cap

    def _calc_hist(self, img: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """ヒストグラムを計算
        Args:
            img (ndarray): 画像情報(3チャンネル)

        Returns:
            hist (ndarray): ヒストグラム(1チャンネル)6
        """
        hist: npt.NDArray[np.float64] = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist

    def _extract_keyframes(self, threshold: float = 0.5) -> Generator:
        """ヒストグラムを用いたキーフレーム抽出
        ヒストグラム差分を計算し、その差分がしきい値以上ならばキーフレームとする
        Args:
            threshold (float): しきい値

        Yield:
            keyframes (list): キーフレーム情報リスト
        """
        cap = self._load_video()
        keyframes = []

        ret, frame = cap.read()
        frame = self._resize_frame(frame)
        keyframes.append(frame)  # 1フレーム目は必ずキーれフレーム
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


    @print_time_arg("extract-keyframe")  # [NEW] デコレーター
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
                    # [NEW]　内包表記
                    frames += [
                        np.zeros((self._new_h, self._new_w, 3), dtype=np.uint8)
                        for _ in range(self._synth_frame_columns - len(frames))
                    ]
                try:
                    synth_img = cv2.vconcat([synth_img, cv2.hconcat(frames)])
                except:
                    print("Error: Concat Image")
        cv2.imwrite(self._video_name + ".jpg", synth_img)


class VideoDownloader(KeyframeExtractor):
    save_dir = ""  # [NEW] クラス変数

    def __init__(self, video_url: str) -> None:
        """
        Args:
            video_url (str): ダウンロードしたい映像ファイルのurl
        """
        video_name = video_url.split("/")[-1]
        video_path = self.save_dir + video_name + ".mp4"

        super().__init__(video_path)  # 親クラスのイニシャライザをオーバーライド
        self._video_url = video_url  # [NEW] インスタンス変数

    @print_time_arg_return("download video")
    def __call__(self) -> bool:
        if not os.path.exists(self._video_path):
            if not self.is_valid_link(self._video_url):
                print("Don't donwoload video")
                return False

            ydl_opts = {"format": "best", "outtmpl": self._video_path}  # 親クラスの変数を使用
            with YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([self._video_url])
                except yt_dlp.utils.DownloadError:
                    print("don't exist videos")
                    return False
        else:
            print("Download : already completed")

        return True

    @staticmethod  # [NEW] スタティックメソッド
    def is_valid_link(url: str) -> bool:
        """YouTubeのURLかどうかを確認
        Args:
            url (str): ダウンロードしたい動画のurl
        """
        # YouTube動画のみダウンロード可能
        if not url.startswith("https://youtu.be"):
            return False
        else:
            return True

    @classmethod  # [NEW] クラスメソッド
    def set_save_dir(cls, save_dir: str) -> None:
        """保存先ディレクトリの設定と作成
        Args:
            save_dir (str): 保存先ディレクトリ
        """
        cls.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)


def analyze_net_video(url: str) -> None:
    """インターネットにある映像を分析
    Args:
        url (str): インターネットにある映像のurl
    """
    vd = VideoDownloader(url)
    if vd():
        vd.generate_synth_keyframe()


def analyze_local_video(path: str) -> None:
    """ローカルにある映像を分析
    Args:
        path (str): ローカルにある映像のパス
    """
    ke = KeyframeExtractor(path)
    ke.generate_synth_keyframe()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="コマンドライン引数")
    parser.add_argument(
        "--save_dir", type=str, default="./videos/", help="ダウンロードしたファイルを保存するディレクトリ"
    )
    parser.add_argument(
        "--video_urls",
        default=("https://youtu.be/DCfk7tc_KqE",),
        help="ダウンロードしたい動画のURL",
    )
    args = parser.parse_args()

    # 保存先を登録
    VideoDownloader.set_save_dir(args.save_dir)

    for url in args.video_urls:
        analyze_net_video(url)
