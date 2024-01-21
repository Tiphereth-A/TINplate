import os

import yaml

from libs.classes.section import Section
from libs.decorator import withlog


class Config:
    def __init__(self, conf_path: str):
        self.__conf_path = conf_path
        self._config: dict = {}
        self.reload()

    def __str__(self) -> str:
        return str(self._config)

    def reload(self):
        if not os.access(self.__conf_path, os.R_OK):
            raise PermissionError(f"{self.__conf_path} is inaccessible")
        with open(self.__conf_path, 'r', encoding='utf8') as f:
            self._config = yaml.safe_load(f)

    def output(self):
        if not os.access(self.__conf_path, os.W_OK):
            raise PermissionError(f"{self.__conf_path} is inaccessible")
        with open(self.__conf_path, 'w', encoding='utf8') as f:
            yaml.dump(self._config, f, sort_keys=False, allow_unicode=True)

    def items(self, *args: str):
        result = self._config
        for arg in args:
            result = result[arg]
        return result

    def _get_chapters_raw(self) -> dict[str, str]:
        return self.items('notebook', 'chapters')

    def _get_sections_raw(self) -> dict:
        return self.items('notebook', 'sections')

    def _get_cheatsheet_raw(self) -> dict[str, str]:
        return self.items('cheatsheets')

    def _get_src_dir_raw(self) -> str:
        return self.items('src_dir')

    def _get_code_dir_raw(self) -> str:
        return self.items('notebook_code_dir')

    def _get_doc_dir_raw(self) -> str:
        return self.items('notebook_doc_dir')

    def _get_cheatsheet_dir_raw(self) -> str:
        return self.items('cheatsheet_dir')

    def _get_test_dir_raw(self) -> str:
        return self.items('test_dir')

    def _get_notebook_file_raw(self) -> str:
        return self.items('notebook_file')

    def _get_export_testcode_in_notebook_raw(self) -> bool:
        return self.items('export_testcode_in_notebook')

    def _get_default_code_style_raw(self) -> str:
        return self.items('default_code_style')

    def _get_code_styles_raw(self) -> dict[str, str]:
        return self.items('code_styles')

    def _get_test_commands_raw(self) -> dict[str, list[str]]:
        return self.items('test_commands')

    def _get_formatting_commands_raw(self) -> dict[str, list[str]]:
        return self.items('formatting_commands')

    @withlog
    def get_src_dir(self, **kwargs) -> str:
        return self._get_src_dir_raw()

    @withlog
    def get_code_dir(self, **kwargs) -> str:
        return os.path.join(self.get_src_dir(), self._get_code_dir_raw())

    @withlog
    def get_doc_dir(self, **kwargs) -> str:
        return os.path.join(self.get_src_dir(), self._get_doc_dir_raw())

    @withlog
    def get_cheatsheet_dir(self, **kwargs) -> str:
        return os.path.join(self.get_src_dir(), self._get_cheatsheet_dir_raw())

    @withlog
    def get_test_dir(self, **kwargs) -> str:
        return os.path.join(self.get_src_dir(), self._get_test_dir_raw())

    @withlog
    def get_notebook_file(self, **kwargs) -> str:
        return self._get_notebook_file_raw()

    @withlog
    def get_chapter_key(self, **kwargs) -> list[str]:
        return list(self._get_chapters_raw().keys())

    @withlog
    def get_chapter_title(self, chapter: str, **kwargs) -> str:
        try:
            return self._get_chapters_raw()[chapter]
        except KeyError:
            kwargs.get('logger').warning(
                rf"title name of chapter '{chapter}' is not found, use '{chapter}' instead")
            return chapter

    @withlog
    def get_sections_by_chapter(self, chapter: str, **kwargs) -> list[Section]:
        _result: list[dict] = self._get_sections_raw().get(chapter, [])
        result: list[Section] = []
        if _result:
            for item in _result:
                result.append(Section(chapter).parse_from_dict(item))
        else:
            kwargs.get('logger').warning(
                f"No section config found with chapter key '{chapter}'")
        return result

    @withlog
    def set_sections_by_chapter(self, chapter: str, sections: list[Section], **kwargs):
        try:
            self._get_sections_raw()[chapter]
        except KeyError:
            kwargs.get('logger').warning(
                f"chapter with key '{chapter}' is not found, try to generate one")
            self.append_chapter(chapter)

        self._get_sections_raw()[chapter] = [sec.get_dict()
                                             for sec in sections]

    @withlog
    def append_chapter(self, chapter: str, **kwargs):
        for item in self.get_chapter_key():
            if item == chapter:
                kwargs.get('logger').waining(
                    f"chapter with key '{item}' already exists, skipped")
                return
        self._get_chapters_raw().update({chapter: chapter})
        self._get_sections_raw().update({chapter: []})
        self.output()

    @withlog
    def append_section(self, section: Section, **kwargs):
        _sections: list[Section] = self.get_sections_by_chapter(
            section.chapter)
        for item in _sections:
            if item.name == section.name:
                kwargs.get('logger').waining(
                    f"section with key '{section.name}' already exists, skipped")
                return
        _sections.append(section)
        self.set_sections_by_chapter(section.chapter, _sections)
        self.output()

    @withlog
    def get_cheatsheets(self, **kwargs) -> list[str]:
        return list(self._get_cheatsheet_raw().keys())

    @withlog
    def get_cheatsheet_name(self, cheatsheet: str, **kwargs) -> str:
        try:
            return self._get_cheatsheet_raw()[cheatsheet]
        except KeyError:
            kwargs.get('logger').warning(
                rf"title name of cheatsheet section '{cheatsheet}' is not found, use '{cheatsheet}' instead")
            return cheatsheet

    @withlog
    def export_testcode_in_notebook(self, **kwargs) -> bool:
        return self._get_export_testcode_in_notebook_raw()

    @withlog
    def get_default_code_style(self, **kwargs) -> str:
        return self._get_default_code_style_raw()

    @withlog
    def get_code_style(self, extname: str, **kwargs) -> str:
        return self._get_code_styles_raw().get(extname, self.get_default_code_style())

    @withlog
    def get_all_code_styles(self, **kwargs) -> set[str]:
        return set(self._get_code_styles_raw().values())

    @withlog
    def get_all_code_ext_names(self, **kwargs) -> set[str]:
        return set(self._get_code_styles_raw().keys())

    @withlog
    def get_ext_names_by_code_style(self, code_style: str, **kwargs) -> list[str]:
        return [k for k, v in self._get_code_styles_raw().items() if v == code_style]

    @withlog
    def get_test_command(self, code_style: str, filepath: str, **kwargs) -> list[str]:
        try:
            result: list[str] = self._get_test_commands_raw()[code_style]
            result = [filepath if item ==
                      '${filename}' else item for item in result]
            return result
        except KeyError:
            kwargs.get('logger').warning(
                rf"test command of code style '{code_style}' is not found, return empty command")
            return []

    @withlog
    def get_formatting_command(self, code_style: str, filepath: str, **kwargs) -> list[str]:
        try:
            result: list[str] = self._get_formatting_commands_raw()[code_style]
            result = [filepath if item ==
                      '${filename}' else item for item in result]
            return result
        except KeyError:
            kwargs.get('logger').warning(
                rf"formatting command of code style '{code_style}' is not found, return empty command")
            return []
