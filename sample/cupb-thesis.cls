% =============================================================================
%  中国石油大学（北京）本科生毕业设计(论文) LaTeX 模板
%  严格遵循《中国石油大学（北京）本科生毕业设计（论文）写作指南》
%  使用 XeLaTeX 编译
% =============================================================================
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cupb-thesis}[2026/05/11 v1.0 CUPB Undergraduate Thesis]

% ---------------------------------------------------------------------------
%  选项处理
% ---------------------------------------------------------------------------
\newif\if@printmode\@printmodetrue
\DeclareOption{draft}{\@printmodefalse}
\ProcessOptions\relax

% ---------------------------------------------------------------------------
%  基础类: ctexbook 提供中文支持
%  cs4size 选项: 小四号=12pt 正文
% ---------------------------------------------------------------------------
\LoadClass[zihao=-4,a4paper,UTF8,linespread=1.25]{ctexbook}

% ---------------------------------------------------------------------------
%  所需宏包
% ---------------------------------------------------------------------------
\RequirePackage{geometry}       % 页面设置
\RequirePackage{fancyhdr}       % 页眉页脚
\RequirePackage{titletoc}       % 目录格式
\RequirePackage{tocloft}        % 目录控制
\RequirePackage{caption}        % 图表标题
\RequirePackage{amsmath,amssymb}% 数学公式
\RequirePackage{graphicx}       % 插图
\RequirePackage{booktabs}       % 三线表
\RequirePackage{longtable}      % 长表格
\RequirePackage{array}          % 表格增强
\RequirePackage{enumitem}       % 列表环境
\RequirePackage{xcolor}         % 颜色
\RequirePackage{etoolbox}       % 工具宏
\AtEndPreamble{%                % hyperref 必须最后加载
  \RequirePackage[unicode,bookmarksnumbered]{hyperref}
}

% ---------------------------------------------------------------------------
%  页面布局 — 写作指南第九条
%  页边距: 上下左右 3.0cm, 左侧装订 1.0cm
% ---------------------------------------------------------------------------
\geometry{
  paper      = a4paper,
  top        = 3.0cm,
  bottom     = 3.0cm,
  left       = 3.0cm,
  right      = 3.0cm,
  bindingoffset = 1.0cm,
  headheight = 0.7cm,
  headsep    = 0.5cm,
  footskip   = 1.0cm,
}

% ---------------------------------------------------------------------------
%  行距 — 多倍行距 1.25
%  cs4size 已设置 linespread=1.25, 再通过 setspace 微调确保
% ---------------------------------------------------------------------------
\RequirePackage{setspace}
\setstretch{1.25}

% ---------------------------------------------------------------------------
%  字体设置
%  正文: 宋体小四号(12pt)
%  页眉: 黑体五号(10.5pt)
%  页码: Arial 五号
%  一级标题: 黑体三号(16pt)
%  二级标题: 黑体四号(14pt)
%  三级标题: 黑体小四号(12pt)
% ---------------------------------------------------------------------------

% 正文字体已由 cs4size + ctexbook 设为 宋体小四号
% 覆盖一些细节以确保一致性
\renewcommand{\normalsize}{\zihao{-4}}    % 小四号

% 章节标题字体
\ctexset{
  chapter = {
    nameformat   = {\heiti\zihao{3}},       % 黑体三号
    titleformat  = {\heiti\zihao{3}},
    numberformat = {\heiti\zihao{3}},
    format       = {\heiti\zihao{3}\centering},
    afterskip    = {18pt plus 2pt minus 2pt},
    beforeskip   = {24pt plus 3pt minus 3pt},
    name         = {第,章},
  },
  section = {
    nameformat   = {\heiti\zihao{4}},
    titleformat  = {\heiti\zihao{4}},
    numberformat = {\heiti\zihao{4}},
    format       = {\heiti\zihao{4}\raggedright},
    afterskip    = {12pt plus 2pt minus 2pt},
    beforeskip   = {18pt plus 2pt minus 2pt},
  },
  subsection = {
    nameformat   = {\heiti\zihao{-4}},
    titleformat  = {\heiti\zihao{-4}},
    numberformat = {\heiti\zihao{-4}},
    format       = {\heiti\zihao{-4}\raggedright},
    afterskip    = {8pt plus 1pt minus 1pt},
    beforeskip   = {12pt plus 1pt minus 1pt},
  },
  subsubsection = {
    nameformat   = {\heiti\zihao{-4}},
    titleformat  = {\heiti\zihao{-4}},
    numberformat = {\heiti\zihao{-4}},
    format       = {\heiti\zihao{-4}\raggedright},
    afterskip    = {6pt plus 1pt minus 1pt},
    beforeskip   = {8pt plus 1pt minus 1pt},
  },
}

% ---------------------------------------------------------------------------
%  章节编号深度 (四级以内)
%  一级: 第1章  二级: 1.1  三级: 1.1.1  四级: 1.1.1.1
% ---------------------------------------------------------------------------
\setcounter{secnumdepth}{4}
\setcounter{tocdepth}{3}

% 让 subsubsection 也参与编号
\ctexset{
  subsubsection = {
    numbering = true,
  },
}

% ---------------------------------------------------------------------------
%  页眉页脚 — 写作指南第九条第1项
%  奇数页: 黑体五号居中 "中国石油大学（北京）本科生毕业设计(论文)"
%  偶数页: 黑体五号居中 "章节标题"
%  页码: Arial 五号居中于页脚
%  前置部分: 罗马数字 (I, II, ...), 宋体五号
%  正文部分: 阿拉伯数字, Arial 五号
% ---------------------------------------------------------------------------
\pagestyle{fancy}
\fancyhf{}

% 奇数页页眉
\fancyhead[CO]{\heiti\zihao{5}中国石油大学（北京）本科生毕业设计(论文)}
% 偶数页页眉 = 当前章标题
\fancyhead[CE]{\heiti\zihao{5}\leftmark}

% 页脚页码
\fancyfoot[C]{\zihao{5}\fontspec{Arial}\thepage}

% 页眉页脚线
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

% 前置部分页眉页脚 — 罗马数字页码
\fancypagestyle{frontmatter}{
  \fancyhf{}
  \fancyhead[CO]{\heiti\zihao{5}中国石油大学（北京）本科生毕业设计(论文)}
  \fancyhead[CE]{\heiti\zihao{5}\leftmark}
  \fancyfoot[C]{\zihao{5}\fontspec{Times New Roman}\romanpage}
  \renewcommand{\headrulewidth}{0.4pt}
}

% plain 风格用于章节首页
\fancypagestyle{plain}{
  \fancyhf{}
  \fancyfoot[C]{\zihao{5}\fontspec{Arial}\thepage}
  \renewcommand{\headrulewidth}{0pt}
}

% 前置部分 plain 风格
\fancypagestyle{plain-front}{
  \fancyhf{}
  \fancyfoot[C]{\zihao{5}\fontspec{Times New Roman}\romanpage}
  \renewcommand{\headrulewidth}{0pt}
}

% ---------------------------------------------------------------------------
%  罗马数字页码命令
% ---------------------------------------------------------------------------
\newcommand{\romanpage}{\Roman{page}}

% ---------------------------------------------------------------------------
%  标题格式 — 由 ctexset 全权处理 (一级标题居中, 其他靠左)
% ---------------------------------------------------------------------------

% ---------------------------------------------------------------------------
%  目录格式 — 写作指南第五条
%  目录中的标题编排到三级
% ---------------------------------------------------------------------------
\renewcommand{\cfttoctitlefont}{\heiti\zihao{3}\centering}
\renewcommand{\cftaftertoctitle}{\hfill}
\renewcommand{\contentsname}{目\hspace{2em}录}

% 章节目录格式
\titlecontents{chapter}[0pt]
  {\heiti\zihao{-4}\vspace{6pt}}
  {\thecontentslabel\hspace{1em}}
  {}
  {\titlerule*[4pt]{.}\contentspage}

\titlecontents{section}[1.5em]
  {\songti\zihao{-4}\vspace{3pt}}
  {\thecontentslabel\hspace{1em}}
  {}
  {\titlerule*[4pt]{.}\contentspage}

\titlecontents{subsection}[3.5em]
  {\songti\zihao{-4}\vspace{3pt}}
  {\thecontentslabel\hspace{1em}}
  {}
  {\titlerule*[4pt]{.}\contentspage}

% ---------------------------------------------------------------------------
%  图表标题 — 写作指南第七条
%  图序号及图名: 居中置于图的下方
%  表序号及表名: 置于表的上方
%  编号: 阿拉伯数字分章编号 (如 图1-1, 表2-3)
% ---------------------------------------------------------------------------
\captionsetup[figure]{
  font        = small,
  labelsep    = quad,
  justification = centering,
  position    = bottom,
}

\captionsetup[table]{
  font        = small,
  labelsep    = quad,
  justification = centering,
  position    = top,
}

% 图/表编号: 章-序号
\numberwithin{figure}{chapter}
\numberwithin{table}{chapter}
\numberwithin{equation}{chapter}

\renewcommand{\thefigure}{\arabic{chapter}-\arabic{figure}}
\renewcommand{\thetable}{\arabic{chapter}-\arabic{table}}
\renewcommand{\theequation}{\arabic{chapter}-\arabic{equation}}

% ---------------------------------------------------------------------------
%  公式编号 — 用括号括起, 写在公式末端
% ---------------------------------------------------------------------------
\renewcommand\tagform@[1]{\maketag@@@{#1}}

% ---------------------------------------------------------------------------
%  列表环境格式
% ---------------------------------------------------------------------------
\setlist{nosep,itemsep=2pt,topsep=4pt}
\setlist[enumerate,1]{label=(\arabic*)}
\setlist[enumerate,2]{label=\textcircled{\arabic*}}
\setlist[enumerate,3]{label=\alph*.}

% ---------------------------------------------------------------------------
%  参考文献 — GB/T 7714-2005 顺序编码制
%  使用 gbt7714 宏包 (需安装: tlmgr install gbt7714)
%  如未安装, 可改用 basic 方式: \RequirePackage[sort&compress,super,square]{natbib}
% ---------------------------------------------------------------------------
\IfFileExists{gbt7714.sty}{%
  \RequirePackage[super,square,comma]{gbt7714}
  \bibliographystyle{gbt7714-2005}
}{%
  \RequirePackage[sort&compress,super,square]{natbib}
  \bibliographystyle{unsrt}
}

% ---------------------------------------------------------------------------
%  封面信息命令 (使用 thesi- 前缀避免与标准 LaTeX 命令冲突)
% ---------------------------------------------------------------------------
\newcommand{\@thesiunitcode}{11414}
\newcommand{\@thesistudentid}{}
\newcommand{\@thesicollege}{}
\newcommand{\@thesimajor}{}
\newcommand{\@thesiauthor}{}
\newcommand{\@thesiadviser}{}
\newcommand{\@thesifinishdate}{}
\newcommand{\@thesititle}{}
\newcommand{\@thesientitle}{}

\newcommand{\thesiunitcode}[1]{\renewcommand{\@thesiunitcode}{#1}}
\newcommand{\thesistudentid}[1]{\renewcommand{\@thesistudentid}{#1}}
\newcommand{\thesicollege}[1]{\renewcommand{\@thesicollege}{#1}}
\newcommand{\thesimajor}[1]{\renewcommand{\@thesimajor}{#1}}
\newcommand{\thesiauthor}[1]{\renewcommand{\@thesiauthor}{#1}}
\newcommand{\thesiadviser}[1]{\renewcommand{\@thesiadviser}{#1}}
\newcommand{\thesifinishdate}[1]{\renewcommand{\@thesifinishdate}{#1}}
\newcommand{\thesititle}[1]{\renewcommand{\@thesititle}{#1}}
\newcommand{\thesientitle}[1]{\renewcommand{\@thesientitle}{#1}}

% 生成封面
\newcommand{\makecover}{%
  \thispagestyle{empty}
  \begin{center}
    \vspace*{2cm}

    {\heiti\zihao{1}\bfseries 中国石油大学（北京）}

    \vspace{1.5cm}

    {\heiti\zihao{1}\bfseries 本科生毕业设计(论文)}

    \vspace{2.5cm}

    \begin{spacing}{2.0}
      \heiti\zihao{3}
      \begin{tabular}{rl}
        单位代码：& \@thesiunitcode \\
        学\quad 号：& \@thesistudentid \\
        论文标志：& 中国石油大学本科生毕业设计(论文) \\
        论文题目：& \@thesititle \\
        学\quad 院：& \@thesicollege \\
        专\quad 业：& \@thesimajor \\
        学生姓名：& \@thesiauthor \\
        指导教师：& \@thesiadviser \\
        完成时间：& \@thesifinishdate \\
      \end{tabular}
    \end{spacing}

    \vfill
  \end{center}
  \newpage
}

% ---------------------------------------------------------------------------
%  声明页
% ---------------------------------------------------------------------------
\newcommand{\makestatement}{%
  \thispagestyle{empty}
  \vspace*{1cm}
  \begin{center}
    {\heiti\zihao{3}论文独创性声明}
  \end{center}
  \vspace{1cm}
  \songti\zihao{-4}
  本人郑重声明：所呈交的毕业设计(论文)是我个人进行的研究工作及取得的研究成果。尽我所知，除了文中特别加以标注和致谢的地方外，论文中不包含其他人已经发表或撰写过的研究成果，也不包含为获得中国石油大学（北京）或其它教育机构的学位或证书而使用过的材料。与我一同工作的同志对本研究所做的任何贡献均已在论文中做了明确的说明并表示了谢意。

  \vspace{2cm}
  \begin{flushright}
    签名：\underline{\hspace{3cm}}\quad 日期：\underline{\hspace{3cm}}
  \end{flushright}

  \vspace{3cm}
  \begin{center}
    {\heiti\zihao{3}关于论文使用授权的说明}
  \end{center}
  \vspace{1cm}

  本人完全了解中国石油大学（北京）有关保留、使用学位论文的规定。即：学校有权保留送交论文的复印件，允许论文被查阅和借阅；学校可以公布论文的全部或部分内容，可以采用影印、缩印或其他复制手段保存论文。

  \vspace{2cm}
  \begin{flushright}
    签名：\underline{\hspace{3cm}}\quad 日期：\underline{\hspace{3cm}}
  \end{flushright}
  \newpage
}

% ---------------------------------------------------------------------------
%  中文摘要环境
% ---------------------------------------------------------------------------
\newenvironment{cnabstract}{%
  \chapter*{摘\hspace{2em}要}
  \thispagestyle{plain-front}
  \pagestyle{frontmatter}
  \pagenumbering{Roman}
  \setcounter{page}{1}
  \songti\zihao{-4}
}{%
  \par
  \vspace{1em}
  \noindent\textbf{关键词：}\@cnkeywords
  \newpage
}

\newcommand{\@cnkeywords}{}
\newcommand{\cnkeywords}[1]{\renewcommand{\@cnkeywords}{#1}}

% ---------------------------------------------------------------------------
%  英文摘要环境
% ---------------------------------------------------------------------------
\newenvironment{enabstract}{%
  \chapter*{\bfseries\zihao{3} Abstract}
  \thispagestyle{plain-front}
  \songti\zihao{-4}
}{%
  \par
  \vspace{1em}
  \noindent\textbf{Keywords:} \@enkeywords
  \newpage
}

\newcommand{\@enkeywords}{}
\newcommand{\enkeywords}[1]{\renewcommand{\@enkeywords}{#1}}

% ---------------------------------------------------------------------------
%  前言环境
% ---------------------------------------------------------------------------
\newenvironment{preface}{%
  \chapter*{前\hspace{2em}言}
  \addcontentsline{toc}{chapter}{前言}
  \thispagestyle{plain-front}
  \songti\zihao{-4}
}{%
  \newpage
}

% ---------------------------------------------------------------------------
%  结论环境 (论文最后一章)
% ---------------------------------------------------------------------------
\newenvironment{conclusion}{%
  \chapter*{结\hspace{2em}论}
  \addcontentsline{toc}{chapter}{结论}
  \songti\zihao{-4}
}{%
  \newpage
}

% ---------------------------------------------------------------------------
%  主要符号表
% ---------------------------------------------------------------------------
\newenvironment{symbollist}{%
  \chapter*{主要符号表}
  \addcontentsline{toc}{chapter}{主要符号表}
  \songti\zihao{-4}
  \begin{tabular}{ll}
}{%
  \end{tabular}
  \newpage
}

% ---------------------------------------------------------------------------
%  致谢
% ---------------------------------------------------------------------------
\newenvironment{acknowledgement}{%
  \chapter*{致\hspace{2em}谢}
  \addcontentsline{toc}{chapter}{致谢}
  \songti\zihao{-4}
  致谢对象限于在学术方面对论文的完成有较重要帮助的人士和团体，感情要诚挚，限300字。

  \bigskip
}{%
  \newpage
}

% ---------------------------------------------------------------------------
%  参考文献环境
% ---------------------------------------------------------------------------
\newcommand{\makereference}[1]{%
  \chapter*{参考文献}
  \addcontentsline{toc}{chapter}{参考文献}
  \begingroup
  \songti\zihao{5}
  \bibliography{#1}
  \endgroup
  \newpage
}

% ---------------------------------------------------------------------------
%  附录
% ---------------------------------------------------------------------------
\newenvironment{theappendix}{%
  \appendix
  \renewcommand{\thechapter}{\Alph{chapter}}
  \ctexset{chapter/name={附录}}
  \titlecontents{chapter}[0pt]
    {\heiti\zihao{-4}\vspace{6pt}}
    {附录\thecontentslabel\hspace{1em}}
    {}
    {\titlerule*[4pt]{.}\contentspage}
}{}

% ---------------------------------------------------------------------------
%  正文开始命令 (切换到阿拉伯页码)
% ---------------------------------------------------------------------------
\newcommand{\mainmatterstart}{%
  \cleardoublepage
  \pagenumbering{arabic}
  \setcounter{page}{1}
  \pagestyle{fancy}
}

% ---------------------------------------------------------------------------
%  前置部分开始
% ---------------------------------------------------------------------------
\AtBeginDocument{%
  \pagestyle{empty}
}

\endinput
