# ply_tex2sym

ply_tex2sym parses LaTeX math expressions and converts it into the equivalent SymPy form by using PLY.  

Author:Akira Hakuta,  Date: 2017/06/11     

## Installation (windows)

TeX Live:  <http://www.tug.org/texlive/acquire-netinstall.html>

```
\texlive\2016\bin\win32\pythontex.exe
```

Python3: <https://www.python.org/downloads/windows/>  
SymPy : <http://www.sympy.org/en/index.html>  
PLY : <http://www.dabeaz.com/ply/>  
```
pip install sympy
pip install ply
```


## Usage
```
python.exe tex2sym_parser.py
   --> Generating LALR tables
   
variable : a,b,...,z,A,B,C,X,Y,Z,\\alpha,\\beta,\\gamma,\\theta,\\omega
constant : pi --> \\ppi, imaginary unit --> \\ii, napier constant --> \\ee

ply_tex2sym LaTeX expression style
\\sin{x}
\\cos^{2}{\theta}
\\log{\\ee}
\\log_{2}{8}
\\frac{d}{dx}{(x^3+x^2+x+1)}
\\int{(x^3+x^2+x+1) dx}
\\int_{1}^{3}{(x-1)(x-3)^2 dx}
\\lim_{x \\to -\\infty} {(\\sqrt{x^2+3x}+x)}
\\sum_{k=1}^{n}{k(k+1)^2}
\\left| 3 - \\ppi \\right|
a_{n}
\\{a-2(b-c)\\}^2  
_{10}\\P_{3}  
_{10}\\C_{3}  

pdflatex.exe -synctex=1 -interaction=nonstopmode example11.tex  
pythontex.exe example11.tex  
pdflatex.exe -synctex=1 -interaction=nonstopmode example11.tex  
```
## Examples

```
tex2sym: LaTeX math expression --> SymPy form

2^3 --> (2)**(3)
0.5 \\times 3 \\div 5 \\cdot 4 --> nsimplify(0.5)*3*((5)**(-1))*4
2*a*b^2*c^3 --> 2*a*(b)**(2)*(c)**(3)
2ab^2c^3 --> 2*a*(b)**(2)*(c)**(3)
2AB^2C^3 --> 2*A*(B)**(2)*(C)**(3)
\\sqrt{3x} --> sqrt(3*x)
\\frac{2}{3} --> (2) * (3)**(-1)
\\sin {\\ppi x} --> sin(pi*x)
\\sin {x} \\cos {x} \\tan {x} --> sin(x)*cos(x)*tan(x)
\\sin {x} + \\cos {x} + \\tan {x} --> sin(x)+cos(x)+tan(x)
\\sin^{2}{x} \\cos^{2}{x} \\tan^{2}{x} --> (sin(x))**(2)*(cos(x))**(2)*(tan(x))**(2)
\\sin^{3}{x} + \\cos^{3}{x} + \\tan^{3}{x} --> (sin(x))**(3)+(cos(x))**(3)+(tan(x))**(3)
\\log{\\ee^3} --> log((E)**(3))
\\log_{2}{8} --> log(8)*(log(2)**(-1))
\\frac{d}{dx}{x^3} --> diff((x)**(3),x)
\\int{\\sin^{2}{x} dx} --> integrate((sin(x))**(2),x)
\\int_{1}^{3}{(x-1)(x-3)^2 dx} --> integrate((x-1)*((x-3))**(2),(x,1,3))
\\sum_{k=1}^{n}{k^3} --> summation((k)**(3),(k,1,n))
\\lim_{x \\to -\\infty}{(\\sqrt{x^2+3x}+x)} --> limit((sqrt((x)**(2)+3*x)+x), x, (-1)*(oo))
12a_{n+1}-35a_{n} --> 12*F(n+1)-35*F(n)
2x^2+3x+4=0 --> Eq(2*(x)**(2)+3*x+4,0)
x^2-3x-4 \\leqq 0 --> (x)**(2)-3*x-4<=0
\\left| \\left| 3-\\ppi \\right|-1\\right| --> Abs(Abs(3-pi)-1)
10! --> factorial(10)
_{5}\\C_{2} --> binomial(5,2)
_{5}\\P_{2} --> ff(5,2)
-x^2 --> (-1)*((x)**(2))
\\{a-2(b-c)\\}^2 --> ((a-2*(b-c)))**(2)
\\left\\{a-2(b-c)\\right\\}^2 --> ((a-2*(b-c)))**(2)
\\left\\{A-2(B-C)\\right\\}^2 --> ((A-2*(B-C)))**(2)
```


### in japanese

#### ply_tex2sym は LaTeX の数式コードを解析して、SymPy のコード変換する Python のプログラムツールです。  
すでに、antlr4 で作られたLaTeX2SymPy <https://github.com/augustt198/latex2sympy> があります。  
今回、Python の構文解析ライブラリ PLY で作ってみました。  

### 各ソフトのインスツール   
#### TexLive  
<https://www.tug.org/texlive/acquire-netinstall.html>  
install-tl-windows.exe でインスツールする。  
\texlive\2016\bin\win32の中にpythontex.exeがあります。  
これを使う！  

#### Python3  
まず、<https://www.python.org/downloads/windows/> に入って、  
Python3 の好きなバージョン、32bit、64bitを選び、インスツールして下さい。  
コマンドプロンプトで   
pip install sympy  
と打ち込む。Successfully installed ...　と表示されればOK!    
\Python34\Lib\site-packagesのなかにパッケージのフォルダができる。    
PLY も使うので、pip install ply  
当方は Python 3.4.4 で動作を確認しています。  

### 使い方  
python.exe tex2sym_parser.py  
を実行。出力を見ると  
tex2sym_parser.tex2sym(texexpr)  
でどんな変換ができるか、分かると思います。    

更に  
```
pdflatex.exe -synctex=1 -interaction=nonstopmode example11.tex
pythontex.exe example11.tex
pdflatex.exe -synctex=1 -interaction=nonstopmode example11.tex
```
を実行すると、example11.pdf が作成できます。  

### 各ファイルの説明  
### tex2sym_lexer.py 
ply.lex.lex() は字句解析機を構築します。  
これを用いて、文字列をtokenの並びへと変換します。  
python.exe tex2sym_lexer.py  
を実行して下さい。  
どんな単語をtokenとして認識しているのかが分かります。  
tokenの定義する方法は２つあります。  
例えば、非負整数のtokenの名前を'NN_INTEGER'とします。  
```
t_NN_INTEGER(t)= r'\d+'

def t_NN_INTEGER(t):
	r'\d+'
    return t
```
どちらでもtokenを定義できるのですが、  
関数で定義すると、定義された順に高い優先度を与えられます。  
例えば、  
```
def t_NN_INTEGER(t):
    r'\d+'
    return t
    
def t_NN_FLOAT(t):
    r'\d*\.\d+'
    return t
```
の順序で定義すると、  
'123.456'は  
[('123', 'NN_INTEGER'), ('.456', 'NN_FLOAT')] のように２つのtokenと認識してしまいます。  
定義の順序を入れ替えると   
[('123.456', 'NN_FLOAT')]となります。  
このように、順序に気を付けながらtokenを定義します。  

### tex2sym_parser.py   
ply.yacc.yacc() は 構文解析器を構築します。  
これを用いて、定義されたルールに従って、LaTex の数式コードを SymPy のコード変換します。  
```
# expr : expr^expr
def p_expr_exponent(p):
    'expr : expr EXPONENT expr'
    # p[0]  p[1]  p[2]    p[3]
    p[0] = '({}) ** ({})'.format(p[1], p[3])
```
で tex2sym(r'2^3') --> (2) ** (3) となります。  
’expr : expr EXPONENT expr' は意味のある文字列で、  
上記コメントのように、配列pの各要素とシンボル expr,EXPONENT の値が対応しています。  
二重根号、繁分数式 等が正しく処理できるように、必要なp_ 関数を定義していきます。  
高校数学レベルの数式を対象としました。  

関数 mylatex(sympyexpr),mylatexstyle(texexpr) で  
変数 : \alpha,\beta,\gamma,\theta,\omega  
定数 : pi --> \ppi, imaginary unit --> \ii, napier constant --> \ee  
を使えるようにしています。  

絶対値の記号 |expr| は曖昧な記号です。  
次の式は2通りに解釈できます。  
```
| 2|-3+4|-5 | = | 2-5 | = 3
| 2|-3+4|-5 | = 2 - 3 + 20 = 19
```
\left| expr \right| で定義をすることにします。  

### example11.tex  
pythontex について  

\begin{pycode}  
code  
\end{pycode}  

codeの部分にPythonのコードを書き込みます。    

\pyc{code}  

はcodeを実行するコマンド。複数のコマンドを実行するのであれば、; を間に入れる。    
pyはpython、cはcommandの意味。  

\py{value}  

は、valueを可能ならば文字列に変えて出力するコマンドのようです。  
\py{'text'}と\pyc{print('text')} は共に、文字列 text を出力します。  

tex2sym_parser.mylatex(sympyexpr), tex2sym_parser.mylatexstyle(texexpr)   
で一部のギリシャ文字と &pi;, i, e が使える用に、置き換えをしています。  

error となる可能性があるため、   
\py{'$\displaystyle {}={}$'.format(mylatexstyle(texexpr),mylatex(result))} を   
\py{'$\displaystyle {:s}={:s}$'.format(mylatexstyle(texexpr),mylatex(result))}   
に変更しました。(2017/04/24)   

### example12.tex 
具体的な使用例です。  
多段組enumerateをtabularxで実現しています。  
LaTeXのコードをr'\\frac{1}{2}'で渡すと



### モジュールのimport    
他のモジュールと同様に、    
from tex2sym_parser import tex2sym, mylatex, mylatexstyle   
だけで import できるようにするには、    
まず、ダウンロードしたフォルダー ply_tex2sym-master を、Python35\Lib\site-packages にコピーまたは移動し,   
Python34\Lib\site-packages に、例えば、  
ply_tex2sym-master  
の1行だけのファイル ply_tex2sym-master.pth を作ります。    
Pythonは .pth の付いたファイルを読み込んで path を設定します。絶対path でもOK。    


#### 修正情報
2017/04/26  
```
 tex2sym(r'-x^2') --> (((-1)*(x))) ** (2)  
 となる不具合を修正  
 tex2sym_parser.py
 precedence の順序    
    ('right', 'EXPONENT'),  
    ('right', 'UPLUS', 'UMINUS'),  
  としました。  
```

2017/05/01  
```
underbar を '_' に統一  
LaTeX の数式コード 中括弧 { } が使用できるように変更
```  

2017/05/02  
```
tex2sym_lexer.py を次のように変更  

変数として、ABCXYZ が使えるように  
def t_ALPHABET(t):
    r'[a-zABCXYZ]'
    return t      

tex2sym_parser.py を次のように変更  

warnings が表示されないように  
parser=yacc.yacc(errorlog=yacc.NullLogger())

float の変換を  
p[0] = 'nsimplify({})'.format(p[1])  

順列、組合せの様式を  
_{10}\P_{3}
_{10}\C_{3}  
```  


2017/05/07  

```
example2.tex を追加  
```  






