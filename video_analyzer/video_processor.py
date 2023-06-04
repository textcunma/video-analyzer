import os
import cv2
import numpy as np
from yt_dlp import YoutubeDL


class VideoProcessor:
    """映像に関する処理をするクラス"""

    def __init__(self, video_name: str, video_path: str) -> None:
        """イニシャライザ（インスタンスの初期化）
        Args:
            video_name (str): 映像ファイル名
            video_path (str): 映像ファイルのパス名
        """
        self._video_name = video_name
        self._video_path = video_path
        self._synth_frame_columns = 6   # 合成画像の列数
        self._new_w = 0  # リサイズ後の幅
        self._new_h = 0  # リサイズ後の高さ
        self._resize_ratio = 0.4
        self._keyframes_num = 0

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

    def _resize_frame(self, img: np.ndarray) -> np.ndarray:
        """画像を拡大縮小"""
        return cv2.resize(img, (self._new_w, self._new_h))

    def _calc_hist(self, img: np.ndarray) -> np.ndarray:
        """ヒストグラムを計算
        Args:
            img (ndarray): 画像情報(3チャンネル)

        Returns:
            hist (ndarray): ヒストグラム(1チャンネル)6
        """
        img = self._resize_frame(img)
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist

    def _extract_keyframes(self, threshold: float = 0.5) -> list:
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
        keyframes.append(frame)  # 1フレーム目は必ずキーれフレーム
        self._keyframes_num += 1
        prev_hist = self._calc_hist(frame)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
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

    def generate_synth_keyframe(self) -> None:
        """合成キーフレーム画像を生成"""
        synth_img = None
        for frames in self._extract_keyframes():
            if synth_img is None:
                synth_img = cv2.hconcat(frames)
            elif len(frames) == 0:
                break
            else:
                if len(frames) != self._synth_frame_columns:
                    #[NEW]　内包表記
                    frames += [
                        np.zeros((self._new_h, self._new_w, 3), dtype=np.uint8)
                        for _ in range(self._synth_frame_columns - len(frames))
                    ]
                synth_img = cv2.vconcat([synth_img, cv2.hconcat(frames)])

        cv2.imwrite(self._video_name + ".jpg", synth_img)


class VideoDownloader(VideoProcessor):
    def __init__(self, video_url: str, save_dir: str) -> None:
        """
        Args:
            video_url (str): ダウンロードしたい映像ファイルのurl
            save_dir (str): 保存先ディレクトリ
        """

        video_name = video_url.split("/")[-1]
        video_path = save_dir + video_name + ".mp4"

        # 保存ディレクトリ作成
        os.makedirs(save_dir, exist_ok=True)

        super().__init__(video_name, video_path)  # 親クラスのイニシャライザをオーバーライド
        self._video_url = video_url

    def __call__(self) -> None:
        if not os.path.exists(self._video_path):
            ydl_opts = {"format": "best", "outtmpl": self._video_path}  # 親クラスの変数を使用
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self._video_url])


# テスト用コード
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="コマンドライン引数")
    parser.add_argument(
        "--save_dir", type=str, default="./videos/", help="ダウンロードしたファイルを保存するディレクトリ"
    )
    parser.add_argument(
        "--video_url", default=("https://youtu.be/lgKjhlmTqek",), help="ダウンロードしたい動画のURL"
    )
    args = parser.parse_args()

    for url in args.video_url:
        vd = VideoDownloader(url, args.save_dir)
        vd()
        vd.generate_synth_keyframe()
