"""
コマンドライン引数の処理
"""

import argparse
parser = argparse.ArgumentParser(description='')
parser.add_argument('--train_meta_path', type=str, default='./data/train.csv')

global args
args = parser.parse_args()
