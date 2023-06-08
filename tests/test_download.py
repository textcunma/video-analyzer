import os

from video_analyzer.video_processor import VideoDownloader

def test_set_save_dir():
    """set_save_dir関数が正しく動くかテスト"""
    VideoDownloader.set_save_dir("./videos/")
    assert os.path.exists("./videos/")
    assert VideoDownloader.download_save_dir == "./videos/"

def test_init():
    """イニシャライザが正しく動くかテスト"""
    VideoDownloader.set_save_dir("./videos/")
    Vd = VideoDownloader("https://youtu.be/R9JBN_x9zFQ")
    assert Vd.video_path == "./videos/R9JBN_x9zFQ.mp4"

def test_get_video_path():
    """get_video_path関数が正しく動くかテスト"""
    VideoDownloader.set_save_dir("./videos/")
    Vd = VideoDownloader("https://youtu.be/R9JBN_x9zFQ")
    assert Vd.get_video_path() == "./videos/R9JBN_x9zFQ.mp4"

def test_type_call():
    """call関数がboolを返すかテスト"""
    VideoDownloader.set_save_dir("./videos/")
    Vd = VideoDownloader("https://youtu.be/R9JBN_x9zFQ") 
    assert type(Vd()) == bool

def test_is_valid_link():
    """YouTube動画の場合のみ正しく値を返すかテスト"""
    assert True == VideoDownloader.is_valid_link("https://youtu.be/R9JBN_x9zFQ") # youtube
    assert False == VideoDownloader.is_valid_link("https://www.nicovideo.jp/watch/sm42181872")   # niconico

def test_exist_url_call():
    """存在する・しないURLの場合正しく値を返すかテスト"""
    VideoDownloader.set_save_dir("./videos/")
    Vd = VideoDownloader("https://youtu.be/R9JBN_x9zFQ") # 存在するURL
    assert True == Vd()

    Vd2 = VideoDownloader("https://youtu.be/R9JB") # 存在しないURL
    assert False == Vd2()
