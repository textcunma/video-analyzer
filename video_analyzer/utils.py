from typing import Any
from typing import Dict


def update_args(dict_from: Dict[str, Any], dict_to: Dict[str, Any]) -> None:
    """ymlファイルの内容に更新

    コマンドライン引数の値をymlファイルに記述された値に更新する

    :param Dict dict_from: ymlファイルに記述された値
    :param Dict dict_to: 更新されるコマンドライン引数

    Ref: https://github.com/salesforce/densecap/blob/5d08369ffdcb7db946ae11a8e9c8a056e47d28c2/data/utils.py#L85
    """
    for key, value in dict_from.items():
        if isinstance(value, dict):
            update_args(dict_from[key], dict_to[key])
        elif value is not None:
            dict_to[key] = dict_from[key]
