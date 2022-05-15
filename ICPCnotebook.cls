%-*- coding: utf-8 -*-

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ICPCnotebook}[2022/05/15 v0.1 Template class of Tifa's ICPC Notebook]

\LoadClass[a4paper,10pt,dvipsnames,svgnames,x11names]{report}

\RequirePackage[centering,scale=0.8]{geometry}
\RequirePackage{longtable}
\RequirePackage{multirow}
\RequirePackage{multicol}
\RequirePackage{pdflscape}
\RequirePackage[titles]{tocloft}

\RequirePackage{xcolor}
\RequirePackage{algorithm}
\RequirePackage{algpseudocode}
\RequirePackage{amsfonts}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{amsthm}
\RequirePackage{bm}
\RequirePackage{bigdelim}
\RequirePackage{bigstrut}
\RequirePackage{bookmark}
\RequirePackage{booktabs}
\RequirePackage[scale=2]{ccicons}
\RequirePackage{cprotect}
\RequirePackage[UTF8]{ctex}
\RequirePackage{extpfeil}
\RequirePackage{fancyhdr}
\RequirePackage{hyperref}
\RequirePackage{ifthen}
\RequirePackage{subcaption}
\RequirePackage{tabularx}
\RequirePackage{tikz}
\RequirePackage{url}
\RequirePackage{xspace}
\RequirePackage{mathtools}
\RequirePackage{pgfplots}
\usepgfplotslibrary{dateplot}


% Throrem
\newtheorem{theorem}{定理}[section]
\newtheorem{corollary}{推论}[theorem]
\newtheorem{lemma}[theorem]{引理}

\theoremstyle{definition}
\newtheorem{definition}{定义}[section]

\theoremstyle{remark}
\newtheorem*{remark}{注意}

\renewcommand\qedsymbol{$\blacksquare$}


% Font setting
\RequirePackage{eulervm}
\RequirePackage{fontspec}
\setsansfont{Fira Sans}
\setmonofont{Fira Code}[Contextuals=Alternate]
% \setsansfont[BoldFont={FiraSans-Bold.ttf}]{FiraSans-Light.ttf}
% \setmonofont{FiraMono-Regular.ttf}

% User defined math command
\newcommand{\lcm}{\operatorname{lcm}}
\newcommand{\nequiv}{~{\equiv}\llap{/\,}~}
\newcommand{\subjectto}{~s.t.~}


% Code style
\RequirePackage{listings}
\RequirePackage{lstfiracode}
\lstdefinestyle{common}{
    style=FiraCodeStyle,
    belowcaptionskip=1\baselineskip,
    breaklines=true,
    xleftmargin=\parindent,
    showstringspaces=true,
    numbers=left,
    numberstyle=\ttfamily\small,
    basicstyle=\ttfamily,
    stepnumber=1,
    frame=single
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
