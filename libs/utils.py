import logging
import os
from typing import Iterable

from libs.decorator import withlog


def get_full_filenames(_dirs: list[str], valid_extname: list[str]) -> list[str]:
    files: list[str] = []
    for _dir in _dirs:
        for filepath, _, filenames in os.walk(_dir):
            files.extend([os.path.join(filepath, filename) for filename in
                          filter(lambda f: [True for ext in valid_extname if f.endswith(ext)], filenames)])
    return files


def unique(seq: list, hash_func=lambda x: x) -> list:
    visited: dict = {}
    result: list[tuple[int, any]] = []
    for item in seq:
        marker = hash_func(item)
        if marker in visited:
            continue
        visited[marker] = 1
        result.append(item)
    return result


def get_difference(total_elements: set, seq: list) -> dict[int, any]:
    result: dict[int, any] = {}
    now_index: int = -1
    for item in seq:
        now_index += 1
        if item in total_elements:
            continue
        result[now_index] = item

    return result


def file_preprocess(files_in_config: list[str], files_exist: list[str], logger: logging.Logger) -> list[str]:
    """
    append `files_in_config` and `files_exist` and then unique,
    items in `files_in_config` but not in `files_exist` will be removed from the results
    """

    file_c: list[str] = files_in_config.copy()

    not_exist_config: dict[int, str] = get_difference(set(files_exist), file_c)
    if not_exist_config:
        logger.warning(rf"{len(not_exist_config)} config(s) are not exist:" + '\n\t' + '\n\t'.join(
            [f'{i}: {v}' for i, v in not_exist_config.items()]))
        file_c = list(filter(lambda x: x not in set(not_exist_config.items()), file_c))

    return_filelist: list[str] = unique(file_c + files_exist)

    return return_filelist


@withlog
def execute_if_file_exist(filepath: str, func, **kwargs):
    if os.access(filepath, os.F_OK):
        return func(filepath)
    else:
        kwargs.get('logger').warning(f"{filepath} is inaccessible, skipped")


@withlog
def scandir_merge_filter(filter_func, *paths: str, **kwargs) -> list[str]:
    result: list[os.DirEntry] = []
    for path in paths:
        _scandir = execute_if_file_exist(path, os.scandir)
        if not _scandir:
            continue
        result += filter(filter_func, _scandir)
    return unique([f.name for f in result])


@withlog
def scandir_file_merge(valid_ext_name: Iterable[str], *paths: str, **kwargs) -> list[str]:
    return scandir_merge_filter(lambda x: x.is_file() and x.name.partition('.')[-1] in valid_ext_name, *paths)


@withlog
def scandir_dir_merge(*paths: str, **kwargs) -> list[str]:
    return scandir_merge_filter(lambda x: x.is_dir(), *paths)


@withlog
def parse_filename(filename: str, **kwargs) -> tuple[str, str]:
    """return [filename without ext, ext name]"""

    _ = filename.partition('.')
    return _[0], _[-1]
