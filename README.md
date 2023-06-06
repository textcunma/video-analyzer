# video-analyzer
指定した動画を分析するプログラム

## 概要
指定した動画(ローカル、インターネット)を画像処理によって分析

## 内容

* 並行処理、並列処理
* 無名関数
* 型判定
* 高速化
* ユニットテスト

SphinxでPython docstringからドキュメントを自動生成する


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
python -m black video_analyzer
```

## コード型チェック
```
mupy {file name}
```

## Anaconda環境出力
```
conda env export --no-builds > env.yml
```

## Anaconda環境生成
```
conda env create --file env.yml
```