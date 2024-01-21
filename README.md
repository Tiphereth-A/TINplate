# TINplate

![GitHub](https://img.shields.io/github/license/Tiphereth-A/TINplate?style=flat-square)

:notebook_with_decorative_cover: -> :thought_balloon: :bulb: :balloon: Template of ICPC Notebooks

## Usage

### Basic usage

1. Install dependencies:
   - [Python >= 3.9](https://www.python.org/)
   - [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/)
   - [ClangFormat](https://clang.llvm.org/docs/ClangFormat.html)
1. Install fonts

   Download font files then run `sudo cp -r /path/to/download/fonts /usr/share/fonts/truetype/ && fc-cache -f`

   - [Fira Code](https://fonts.google.com/specimen/Fira+Code)
   - [Fira Sans](https://fonts.google.com/specimen/Fira+Sans)
   - [Fira Mono](https://fonts.google.com/specimen/Fira+Mono)

   Run `fc-list | grep Fira` to check installation status

1. Clone this repo and then open it
1. Run `python -m pip install -r requirements.txt` to install requirements
1. Run `python manager.py run` to generate all the contents and compile notebook.tex

### Full usage

Run `python manager.py --help` to see all the commands.

## Configuration

All the configuration is in `config.yml`

```yaml
# The parent folder of `notebook_code_dir`, `notebook_doc_dir` and `cheatsheet_dir`
src_dir: src
# The folder contains all the codes which will be listed
notebook_code_dir: code
# The folder contains all the documentation
notebook_doc_dir: doc
# The folder contains all the cheatsheet documentation
cheatsheet_dir: cheatsheet

# The folder contains all the test codes
test_dir: test

# The name of the file that will be compiled
notebook_file: notebook

# Listing all test code before compiling if `true`
export_testcode_in_notebook: true

# Notebook config
notebook:
  # Chapters config, the content will be generated in the order of this field
  chapters:
    # Should be formed in: ${chapter_key}: ${title}
    # All the chapter is titled as ${title},
    # and all resources for the following sections of each chapters should be placed in these folders:
    # - code: ${src_dir}/${notebook_code_dir}/${chapter_key}
    # - documentation: ${src_dir}/${notebook_doc_dir}/${chapter_key}
    # - test code: ${test_dir}/${chapter_key}

    example: Example

  # Section config
  sections:
    # Config of sections following the chapter ${chapter_key}
    example:
      # Should be an array, the elements of which should be formed in:
      #    ${section_key}: ${title}
      #    code_ext: ${extension_name_of_code}
      #    test_ext: ${extension_name_of_test_code}
      # The relevant files should be in:
      # - code: ${src_dir}/${notebook_code_dir}/${chapter_key}/${section_key}.${extension_name_of_code}
      # - documentation: ${src_dir}/${notebook_doc_dir}/${chapter_key}/${section_key}.tex
      # - test code: ${test_dir}/${chapter_key}/${section_key}.${extension_name_of_test_code}

      - helloworld: Hello
        code_ext: hpp
        test_ext: cpp

# Cheatsheet config
cheatsheets:
  # Should be formed in: ${cheatsheet_key}: ${title}
  # The relevant files should be in: ${src_dir}/${cheatsheet_dir}/${cheatsheet_key}.tex
  example: Euler formula
  example2: A sequence

# Code style config, will be used in linting and compiling PDF
default_code_style: common
code_styles:
  # Should be formed in: ${extension_name}: ${code_style_name}
  C: cpp
  cc: cpp
  cp: cpp
  cpp: cpp
  CPP: cpp
  c++: cpp
  cxx: cpp
  H: cpp
  hh: cpp
  hp: cpp
  h++: cpp
  hpp: cpp
  HPP: cpp
  hxx: cpp

# Compiling test code command config, ${filename} is the name of file that will be compiled
test_commands:
  cpp:
  - g++
  - ${filename}

# Linting command config, ${filename} is the name of file that will be linted
formatting_commands:
  cpp:
    - clang-format
    - -style=file
    - -i
    - ${filename}
```
