#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
import random
import subprocess

import click
import coloredlogs

from libs.classes.section import Section
from libs.consts import CONFIG, CLEAN_EXT_NAME, CONTENTS_CS, CONTENTS_DIR, CONTENTS_NB
from libs.decorator import withlog
from libs.latex_utils import latex_input, latex_chapter, latex_section, latex_listing_code, PathLaTeX, NameLaTeX, \
    LATEX_COMPILE_COMMAND_GROUP
from libs.utils import get_full_filenames, file_preprocess, execute_if_file_exist, scandir_dir_merge, \
    scandir_file_merge, parse_filename, unique


@click.group()
@click.option('-l', '--level', type=click.Choice(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']), help='log level',
              default='INFO')
def cli(level: str):
    coloredlogs.install(level=level,
                        fmt='%(asctime)s %(levelname)s %(programname)s::%(name)s [%(process)d] %(message)s',
                        field_styles={'asctime': {'color': 'green'},
                                      'hostname': {'color': 'red'},
                                      'levelname': {'bold': True, 'color': 'magenta'},
                                      'name': {'faint': True, 'color': 'blue'},
                                      'programname': {'bold': True, 'color': 'cyan'},
                                      'process': {'faint': True, 'color': 'green'},
                                      'username': {'color': 'yellow'}},
                        level_styles={'critical': {'bold': True, 'color': 'red'},
                                      'debug': {'color': 'cyan'},
                                      'error': {'color': 'red'},
                                      'info': {'bright': True, 'color': 'white'},
                                      'notice': {'color': 'magenta'},
                                      'spam': {'color': 'green', 'faint': True},
                                      'success': {'bold': True, 'color': 'green'},
                                      'verbose': {'color': 'blue'},
                                      'warning': {'bright': True, 'color': 'yellow'}})


@cli.command('clean')
def _clean():
    """Clean files"""

    @withlog
    def clean(logger: logging.Logger):
        for fullFilename in get_full_filenames(['.'], CLEAN_EXT_NAME):
            os.remove(fullFilename)
            logger.info(rf"{fullFilename} removed successfully")

    clean()


@cli.command('gen-nb')
def _gen_nbc():
    """Generate notebook contents"""

    @withlog
    def generate_notebook_contents(logger: logging.Logger):
        if not os.access(CONTENTS_DIR, os.R_OK):
            os.makedirs(CONTENTS_DIR)
        with open(CONTENTS_NB, 'w', encoding='utf8') as f:
            f.write('%-*- coding: utf-8 -*-\n')
            chapters = file_preprocess(CONFIG.get_chapter_key(),
                                       scandir_dir_merge(CONFIG.get_code_dir(), CONFIG.get_doc_dir()), logger)
            logger.info(rf"{len(chapters)} chapter(s) found")
            logger.debug('Which are:\n\t' + '\n\t'.join(chapters))
            logger.debug('Will include in listed order')

            for chapter in chapters:
                f.writelines(latex_chapter(NameLaTeX(CONFIG.get_chapter_title(chapter))))

                sections: list[Section] = CONFIG.get_sections_by_chapter(chapter)
                logger.info(f"{len(sections)} section(s) found in config")

                logger.debug(f"Getting section from existing files")
                _sections_generated: list[Section] = []
                _partitioned_code_filename = load_from(os.path.join(CONFIG.get_code_dir(), chapter))
                _partitioned_doc_filename = load_from(os.path.join(CONFIG.get_doc_dir(), chapter))
                __dict: dict[str, str] = dict(_partitioned_code_filename)
                if CONFIG.enable_test():
                    _partitioned_test_filename = load_from(os.path.join(CONFIG.get_test_dir(), chapter))
                    for k, v in _partitioned_test_filename:
                        try:
                            _sections_generated.append(Section(chapter, k, k, __dict.pop(k), v))
                        except KeyError as e:
                            logger.error(f"Test file '{k}.{v}' found, while code file is not")
                            raise e
                __null_ext_name: str = f"{random.randint(0, 114514)}.null"
                for k, v in _partitioned_doc_filename:
                    _sections_generated.append(Section(chapter, k, k, __dict.pop(k, __null_ext_name), __null_ext_name))
                for k, v in __dict.items():
                    _sections_generated.append(Section(chapter, k, k, v, __null_ext_name))
                logger.info(f"{len(_sections_generated)} section(s) generated from existing files")

                sections = unique(sections + _sections_generated, lambda x: x.name)
                logger.info(f"{len(sections)} section(s) in total")

                for section in sections:
                    f.writelines(latex_section(NameLaTeX(section.title)))
                    code_filepath, doc_filepath, test_filepath = section.get_filenames(CONFIG.get_code_dir(),
                                                                                       CONFIG.get_doc_dir(),
                                                                                       CONFIG.get_test_dir())
                    execute_if_file_exist(doc_filepath, lambda x: f.writelines(latex_input(PathLaTeX(x))))
                    execute_if_file_exist(code_filepath, lambda x: f.writelines(
                        latex_listing_code(PathLaTeX(x), CONFIG.get_code_style(section.code_ext))))
                    if CONFIG.generate_test_in_notebook():
                        execute_if_file_exist(test_filepath, lambda x: f.writelines(
                            latex_listing_code(PathLaTeX(x), CONFIG.get_code_style(section.test_ext))))

    @withlog
    def load_from(dir_name: str, **kwargs) -> list[tuple[str, str]]:
        filename_in_dir: list[str] = scandir_file_merge(CONFIG.get_all_code_ext_names(), dir_name)
        kwargs.get('logger').info(rf"{len(filename_in_dir)} file(s) found")
        if len(filename_in_dir):
            kwargs.get('logger').debug('Which are:\n\t' + '\n\t'.join(filename_in_dir))

        _partitioned_filename: list[tuple[str, str]] = [parse_filename(filename) for filename in filename_in_dir]
        if len(set([k for k, v in _partitioned_filename])) != len(_partitioned_filename):
            kwargs.get('logger').error(f'File with duplicate name found in dir: {dir_name}')
            kwargs.get('logger').info(
                'Each filenames in the same folder should not be the same after removing the ext names')
            raise FileExistsError()

        return _partitioned_filename

    generate_notebook_contents()


@cli.command('gen-cs')
def _gen_csc():
    """Generate cheatsheet contents"""

    @withlog
    def generate_cheatsheet_contents(logger: logging.Logger):
        if not os.access(CONTENTS_DIR, os.R_OK):
            os.makedirs(CONTENTS_DIR)
        with open(CONTENTS_CS, 'w', encoding='utf8') as f:
            f.write('%-*- coding: utf-8 -*-\n')
            files: list[str] = file_preprocess([f'{f}.tex' for f in CONFIG.get_cheatsheets()],
                                               scandir_file_merge(['tex'], CONFIG.get_cheatsheet_dir()), logger)
            files = [os.path.join(CONFIG.get_cheatsheet_dir(), item) for item in files]
            logger.info(rf"{len(files)} file(s) found:")
            logger.debug('Which are:\n\t' + '\n\t'.join(files))
            logger.debug('Will include in listed order')

            f.writelines(latex_chapter(NameLaTeX('Cheatsheet')))
            for file in files:
                f.writelines(
                    latex_section(NameLaTeX(CONFIG.get_cheatsheet_name(file.removeprefix(CONFIG.get_cheatsheet_dir())
                                                                       .removeprefix('/')
                                                                       .removeprefix('\\')
                                                                       .removesuffix('.tex')))))
                f.writelines(latex_input(PathLaTeX(file)))

    generate_cheatsheet_contents()


@cli.command('run')
@click.option('--no-fmt', is_flag=True, help='Do not reformat codes before compile')
@click.option('--no-gen', is_flag=True, help='Do not generate content before compile')
@click.option('--no-clean', is_flag=True, help='Do not clean files after compile')
def _compile(no_fmt: bool, no_gen: bool, no_clean: bool):
    """Compile notebook"""

    @withlog
    def compile_all(_no_fmt: bool, _no_gen: bool, _no_clean: bool, **kwargs):
        cnt: int = 0
        for procedure in LATEX_COMPILE_COMMAND_GROUP:
            now_proc: list[str] = procedure(CONFIG.get_notebook_file())
            cnt += 1
            kwargs.get('logger').info(f'Step {cnt} / {len(LATEX_COMPILE_COMMAND_GROUP)}' + '\n' + '-' * 80)
            subprocess.run(now_proc, encoding='utf8', check=True)

        kwargs.get('logger').info('Finished')

    if not no_fmt:
        for code_style in CONFIG.get_all_code_styles():
            _format.callback(code_style)

    if not no_gen:
        _gen_nbc.callback()
        _gen_csc.callback()

    compile_all(no_fmt, no_gen, no_clean)

    if not no_clean:
        _clean.callback()


@cli.command('fmt')
@click.option('-t', '--code-type', help='Code type, default: cpp', default='cpp')
def _format(code_type: str):
    """Reformat all codes"""

    @withlog
    def reformat_all_codes(_code_type: str, **kwargs):
        filepaths: list[str] = get_full_filenames([CONFIG.get_code_dir(), CONFIG.get_test_dir()],
                                                  CONFIG.get_ext_names_by_code_style(_code_type))
        kwargs.get('logger').info(f"{len(filepaths)} file(s) found")
        for filepath in filepaths:
            cmd: list[str] = CONFIG.get_formatting_command(_code_type, filepath)
            subprocess.run(cmd, encoding='utf8', check=True)

        kwargs.get('logger').info('finished')

    reformat_all_codes(code_type)


@cli.command('new')
@click.option('-c', '--chapter-name', type=str, prompt='Chapter name', help='Chapter name (key)')
@click.option('-f', '--file-name', type=str, prompt='File name (without ext name)', help='File name to be added')
@click.option('-s', '--section-title', type=str, prompt='Section title', help='Section title in notebook')
@click.option('-e', '--code-ext-name', type=str, prompt='Ext name of code file', help='Ext name of code file',
              default='hpp')
@click.option('-t', '--test-ext-name', type=str, prompt='Ext name of test file', help='Ext name of test file',
              default='cpp')
def _new_note(chapter_name: str, file_name: str, section_title: str, code_ext_name: str,
              test_ext_name: str):
    """Add new note"""

    @withlog
    def add_new_note(_chapter_name: str, _file_name: str, _section_title: str,
                     _code_ext_name: str, _test_ext_name: str, **kwargs):
        section: Section = Section(_chapter_name, _file_name, _section_title, _code_ext_name, _test_ext_name)

        section.open(CONFIG.get_code_dir(), CONFIG.get_doc_dir(), CONFIG.get_test_dir(), 'x')
        kwargs.get('logger').info('Created')

        _code, _doc, _test = section.get_filenames(CONFIG.get_code_dir(), CONFIG.get_doc_dir(), CONFIG.get_test_dir())
        kwargs.get('logger').info(f"Code: {os.path.join(os.curdir, _code)}")
        kwargs.get('logger').info(f"Doc: {os.path.join(os.curdir, _doc)}")
        kwargs.get('logger').info(f"Test: {os.path.join(os.curdir, _test)}")

        CONFIG.append_section(section)
        kwargs.get('logger').info('Config updated')

    add_new_note(chapter_name, file_name, section_title, code_ext_name, test_ext_name)


# TODO
# @cli.command('test')
def _tester():
    pass


if __name__ == '__main__':
    cli()
