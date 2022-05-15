%-*- coding: utf-8 -*-

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ICPCnotebook}[2022/05/15 v0.1 Template class of Tifa's ICPC Notebook]

\LoadClass[10pt]{report}

\RequirePackage{algorithm}
\RequirePackage{algpseudocode}
\RequirePackage{amsfonts}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{amsthm}
\RequirePackage{fancyhdr}
\RequirePackage[centering,scale=0.8]{geometry}
\RequirePackage{hyperref}
\RequirePackage{multicol}
\RequirePackage{listings}
\RequirePackage{pdflscape}
\RequirePackage{tikz}
\RequirePackage{tocloft}
\RequirePackage{xcolor}

\lstdefinestyle{common}{
    belowcaptionskip=1\baselineskip,
    breaklines=true,
    xleftmargin=\parindent,
    showstringspaces=false,
    basicstyle=\fontsize{5.5}{6}\ttfamily,
}
\lstdefinestyle{cpp}{
    style=common,
    language=C++,
    keywordstyle=\bfseries\color{green!40!black},
    commentstyle=\itshape\color{red!80!black},
    identifierstyle=\color{blue},
    stringstyle=\color{purple!40!black},
}
\lstdefinestyle{c}{
    style=common,
    language=C,
    keywordstyle=\bfseries\color{green!40!black},
    commentstyle=\itshape\color{red!80!black},
    identifierstyle=\color{blue},
    stringstyle=\color{purple!40!black},
}
