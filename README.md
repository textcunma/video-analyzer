# video-analyzer
指定した動画を分析するプログラム

## 概要
指定した動画(ローカル、インターネット:YouTubeのみ)からキーフレーム抽出によって合成画像を生成

![トップ画像](./assets/video_analyzer.jpg)


## 実行方法
1. 仮想環境を構築
    ```
    conda env create --file env.yml
    ```

2. 仮想環境を有効化
    ```
    conda activate video-analyzer
    ```

3. ディレクトリ移動
    ```
    cd ./video-analyzer
    ```

4. 実行コマンド(オプション指定可能)
    ```
    python -m video_analyzer

    # オプション指定例
    python -m video_analyzer --max_workers 10 --mode thread
    ```

    | オプション名 | デフォルト値 |
    | ------ | ------ | 
    | --download_flg   | [cfg.yml](./cfg.yml)に記載   | 
    | --video_urls   | [cfg.yml](./cfg.yml)に記載   |
    | --video_paths   | [cfg.yml](./cfg.yml)に記載   | 
    | --download_save_dir   | "./videos/"  |
    | --result_save_dir   | "./result/"  |
    | --max_workers   | 5  |
    | --mode   | default  |

    ※`--mode`オプションは, `default`は逐次実行, `thread`はスレッドベースの非同期実行, `process`はプロセスベースの非同期実行

    オプションが多い場合は、[cfg.yml](./cfg.yml)に引数を指定すると便利です

## ファイル構造
```
video-analyzer
|
├─assets    # 説明用画像フォルダ
├─docs      # Sphinxによるドキュメント
├─tests      # テストコードフォルダ
|
├─env.yml   # 仮想環境ファイル
├─cfg.yml   # コマンドライン引数を指定する設定ファイル
├─mypy.ini  # mypyの設定ファイル
│
└─video_analyzer            # ソースコードフォルダ
    │  utils.py             # ユーティリティ関数など
    │  video_processor.py   # 主な関数、クラス
    │  __init__.py          # 初期化用
    └──  __main__.py        # エントリーポイント
```
## ドキュメント
クラスや関数の引数、返り値を記載（Sphinxによって自動生成）\
https://textcunma.github.io/video-analyzer/


## 開発環境
Windows10上で開発、仮想環境はAnacondaを使用。

| ライブラリ等 | バージョン |
| ------ | ------ | 
| Python   | 3.10   | 
| Numpy   | 1.23.5   |
| OpenCV   | 4.6.0   | 
| yt-dlp   | 2023.3.4  |
詳細は[env.yml](./env.yml)に記載

### その他: 開発時に利用したコマンド
```
# blackによるコード整形
python -m black video_analyzer
```

```
# mypyによるコード型チェック
mupy {file name}
```

```
# 仮想環境出力
conda env export --no-builds > env.yml
```

```
# プロファイラ実行
python -m cProfile {file path}
```

```
# reSTファイルの生成
sphinx-apidoc -F -H video-analyzer -o unbuild_docs video_analyzer

# HTML形式のドキュメントを生成
sphinx-build unbuild_docs docs
```

```
# pytestによるユニットテスト実行
pytest tests/
```