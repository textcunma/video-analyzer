import time

from typing import Any, Dict, Callable


def update_args(dict_from: Dict[str, Any], dict_to: Dict[str, Any]) -> None:
    """ymlファイルの内容に更新

    コマンドライン引数の値をymlファイルに記述された値に更新する

    Args:
        dict_from (Dict): ymlファイルに記述された値
        dict_to (Dict): 更新されるコマンドライン引数

    Note:
        Ref: https://github.com/salesforce/densecap/blob/5d08369ffdcb7db946ae11a8e9c8a056e47d28c2/data/utils.py#L85
    
    """
    for key, value in dict_from.items():
        if isinstance(value, dict):
            update_args(dict_from[key], dict_to[key])
        elif value is not None:
            dict_to[key] = dict_from[key]


def print_time(func):
    """デコレーター：ログ出力"""

    def wrapper(*args, **kargs):
        start = time.time()
        func(*args, **kargs)
        end = time.time()
        print(f"処理時間：{str(round(end - start, 2))}[s]")

    return wrapper


def print_time_arg(
    process_name: str,
) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """引数のあるデコレーター用関数

    Args:
        process_name (str): プロセス名

    """


    def _print_time(func: Callable[..., None]) -> Callable[..., None]:
        def wrapper(*args, **kargs):
            start = time.time()
            func(*args, **kargs)
            end = time.time()
            print(f"{process_name}:処理時間：{str(round(end-start,2))}[s]")

        return wrapper

    return _print_time


def print_time_arg_return(
    process_name: str,
) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """引数、出力のあるデコレーター用関数

    Args:
        process_name (str): プロセス名

    """

    def _print_time(func: Callable[..., None]) -> Callable[..., None]:
        def wrapper(*args, **kargs):
            start = time.time()
            output = func(*args, **kargs)
            end = time.time()
            print(f"{process_name}:処理時間：{str(round(end-start,2))}[s]")
            return output

        return wrapper

    return _print_time
