import re

from libs.classes.configure import Config

CONFIG: Config = Config(r'./config.yml')
CLEAN_EXT_NAME: list[str] = ['.aux', '.bbl', '.blg', '.log', '.nav', '.out', '.snm', '.synctex.gz', '.toc', '.vrb']
CONTENTS_CS: str = r'.\_gen\contents_cheatsheet.tex'
CONTENTS_NB: str = r'.\_gen\contents_notebook.tex'
REGEX_ENDSWITH_MULTI_SLASH = re.compile(r'(?:\\+|/+)$')
REGEX_STARTSWITH_MULTI_SLASH = re.compile(r'^(?:\\+|/+)')
