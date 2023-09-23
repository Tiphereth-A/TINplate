from libs.decorator import withlog


class TextLaTeXBase:
    def __init__(self, s: str):
        self._str: str = s
        self._str.removesuffix('\n')

    def get(self) -> str:
        return self._str

    def get_label_name(self) -> str:
        return self._str.casefold() \
            .replace(' ', '-') \
            .replace('_', '-') \
            .replace('\\', '')


class PathLaTeX(TextLaTeXBase):
    def __init__(self, path: str):
        super().__init__(path)
        self._str = self._str.replace('\\', '/')

    def get_label_name(self) -> str:
        return super().get_label_name() \
            .replace('/', '-') \
            .replace('.', '-')


class NameLaTeX(TextLaTeXBase):
    def __init__(self, path: str):
        super().__init__(path)
        self._str = self._str.replace(r'_', r' ')


@withlog
def xelatex(file: str, **kwargs) -> list:
    return ['xelatex', "-synctex=1", "-interaction=nonstopmode", "-file-line-error", file + '.tex']


@withlog
def bibtex(file: str, **kwargs) -> list:
    return ['bibtex', file]


@withlog
def latexmk(file: str, **kwargs) -> list:
    return ['latexmk', '-cd', '-xelatex', '-file-line-error', '-halt-on-error', '-interaction=nonstopmode',
            '-synctex=1', '-outdir=_pdf_out', '-time', file + '.tex']


LATEX_COMPILE_COMMAND_GROUP: list = [latexmk]
# LATEX_COMPILE_COMMAND_GROUP: list = [xelatex, bibtex, xelatex, xelatex]


def __latex_command_(command: str, *args) -> str:
    return rf"\{command}{{" + '}{'.join(args) + '}\n'


def __latex_command_with_option_(command: str, option: str, *args) -> str:
    return rf"\{command}[{option}]{{" + '}{'.join(args) + '}\n'


@withlog
def latex_input(path: PathLaTeX, **kwargs) -> list[str]:
    return [__latex_command_('input', path.get()),
            '\n']


@withlog
def latex_label(prefix: str, name: TextLaTeXBase, **kwargs) -> list[str]:
    return [__latex_command_('label', f"{prefix}:{name.get_label_name()}")]


@withlog
def latex_chapter(name: NameLaTeX, **kwargs) -> list[str]:
    return [__latex_command_('chapter', name.get())] + latex_label('ch', name) + ['\n']


@withlog
def latex_section(name: NameLaTeX, **kwargs) -> list[str]:
    return ['\n', __latex_command_('section', name.get())] + latex_label('sec', name)


@withlog
def latex_listing_code(path: PathLaTeX, code_style: str, **kwargs) -> list[str]:
    return [__latex_command_('vspace', '0.3cm'),
            __latex_command_('lstset', f"style={code_style}"),
            __latex_command_with_option_('lstinputlisting', f"label={{lst:{path.get_label_name()}}}",
                                         path.get()),
            __latex_command_('vspace', '0.3cm'),
            '\n']
