import os.path
import re

from libs.classes.configure import Config

CONFIG: Config = Config(r'./config.yml')
CLEAN_EXT_NAME: list[str] = ['.aux', '.bbl', '.blg', '.dvi', 'fdb_latexmk', '.fls', '.log', '.nav', '.out', '.snm',
                             '.synctex.gz', '.toc', '.vrb', '.xdv']
CONTENTS_CS: str = os.path.join('.', '_gen', 'contents_cheatsheet.tex')
CONTENTS_NB: str = os.path.join('.', '_gen', 'contents_notebook.tex')
REGEX_ENDSWITH_MULTI_SLASH = re.compile(r'(?:\\+|/+)$')
REGEX_STARTSWITH_MULTI_SLASH = re.compile(r'^(?:\\+|/+)')
