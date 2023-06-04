# video-analyzer
指定した動画を分析するプログラム

## 概要
指定した動画(ローカル、インターネット)を画像処理によって分析

## 内容

* 並列処理
* 無名関数
* 型判定
* 高速化
* テスト

## ライブラリ
* mypy
* black
* Numba

## 仮想環境
```
conda activate movie-analyzer
```

## コード整形
```
python -m black {source_file_or_directory}
```

## Anaconda環境出力
```
conda env export --no-builds > env.yml
```

## Anaconda環境生成
```
conda env create --file env.yml
```