import os.path

from libs.classes.configure import Config

CONTENTS_CS: str = os.path.join('.', '_gen', 'contents_cheatsheet.tex')
CONTENTS_NB: str = os.path.join('.', '_gen', 'contents_notebook.tex')

CONFIG: Config = Config(os.path.join('.', 'config.yml'))

CLEAN_EXT_NAME: list[str] = ['.aux', '.bbl', '.blg', '.dvi', 'fdb_latexmk', '.fls', '.log', '.nav', '.out', '.snm',
                             '.synctex.gz', '.toc', '.vrb', '.xdv']
