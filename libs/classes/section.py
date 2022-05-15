import os
from typing import IO

from libs.decorator import withlog


class Section:
    def __init__(self, chapter: str, filename_without_ext: str = '', title: str = '', code_ext: str = '',
                 test_ext: str = ''):
        self.name = filename_without_ext
        self.title = title
        self.chapter = chapter
        self.code_ext = code_ext
        self.test_ext = test_ext

    @withlog
    def parse_from_dict(self, dict_section: dict, **kwargs):
        self.code_ext: str = dict_section.pop('code_ext')
        self.test_ext: str = dict_section.pop('test_ext')
        if len(dict_section) != 1:
            kwargs.get('logger').error(f"Invalid section config {dict_section}: zero or more than one file candidates")
            raise KeyError()

        self.name: str = list(dict_section.keys())[0]
        self.title: str = list(dict_section.values())[0]
        if not self.title:
            kwargs.get('logger').warning(rf"{self.name}'s title name not found, use '{self.name}' instead")
            self.title = self.name

        return self

    def get_dict(self) -> dict:
        return {self.name: self.title, 'code_ext': self.code_ext, 'test_ext': self.test_ext}

    def get_filenames(self, code_root_dir: str, doc_root_dir: str, test_root_dir: str) -> tuple[str, str, str]:
        _ch_code_dir: str = os.path.join(code_root_dir, self.chapter)
        _ch_doc_dir: str = os.path.join(doc_root_dir, self.chapter)
        _ch_test_dir: str = os.path.join(test_root_dir, self.chapter)

        if not os.path.exists(_ch_code_dir):
            os.mkdir(_ch_code_dir)
        if not os.path.exists(_ch_doc_dir):
            os.mkdir(_ch_doc_dir)
        if not os.path.exists(_ch_test_dir):
            os.mkdir(_ch_test_dir)

        return (os.path.join(_ch_code_dir, f"{self.name}.{self.code_ext}"),
                os.path.join(_ch_doc_dir, f"{self.name}.tex"),
                os.path.join(_ch_test_dir, f"{self.name}.{self.test_ext}"))

    def open(self, code_root_dir: str, doc_root_dir: str, test_root_dir: str, *args, **kwargs) -> tuple[IO, IO, IO]:
        """return IO of code file, doc file and test file"""

        _code, _doc, _test = self.get_filenames(code_root_dir, doc_root_dir, test_root_dir)

        f_code = open(_code, *args, **kwargs)
        f_doc = open(_doc, *args, **kwargs)
        f_test = open(_test, *args, **kwargs)
        return f_code, f_doc, f_test
