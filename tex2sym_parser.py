# tex2sym_parser.py   Author: Akira Hakuta, Date: 2017/05/07
# python.exe tex2sym_parser.py

from ply import yacc
# Get the token map
from tex2sym_lexer import tokens, lexer

from sympy import *
var('a:z') 

# variable : a,b,...,z,A,B,C,X,Y,Z,\alpha,\beta,\gamma,\theta,\omega
# constant : pi --> \ppi, imaginary unit --> \ii, napier constant --> \ee

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('right', 'UPLUS', 'UMINUS'),  
    ('right', 'EXPONENT'),    
    )


# Parsing rules
# Functions should be start with `p_`.

# statement : expr
def p_statement(p):
    'statement : expr'
    p[0] = p[1]

# expr : expr^expr
def p_expr_exponent(p):
    'expr : expr EXPONENT expr'
    #p[0]  p[1] p[2]   p[3]
    p[0] = '({}) ** ({})'.format(p[1], p[3])
    
# expr : expr !
def p_expr_factorial(p):
    'expr : expr FACTORIAL'
    p[0] = 'factorial({})'.format(p[1])
    
    
# expr : expr*expr | expr \times expr | expr CDOT expr
def p_expr_mult(p):
    'expr : expr MULT expr'
    p[0] = '{}*{}'.format(p[1],p[3])
    
# expr : expr expr    
def p_expr_exprexpr(p):
    'expr : expr expr'
    p[0] = '{}*{}'.format(p[1],p[2])
              
# expr : expr \div expr
def p_expr_div(p):
    'expr : expr DIV expr'
    p[0] = '{}*(({})**(-1))'.format(p[1],p[3])
    

# expr : expr+expr
def p_expr_plus(p):
    'expr : expr PLUS expr'
    p[0] = '{} + {}'.format(p[1], p[3])


# expr : expr-expr
def p_expr_minus(p):
    'expr : expr MINUS expr'
    p[0] = '{} - {}'.format(p[1], p[3])
    
# expr : {expr}
def p_expr_brace(p):
    'expr : LBRACE expr RBRACE'
    p[0] = '({})'.format(p[2])

# expr :  (expr)
def p_expr_paren(p):
    'expr : LPAREN expr RPAREN'
    p[0] = '({})'.format(p[2])

# expr : [a-zABCXYZ]
def p_expr_symbol(p):
    'expr : ALPHABET'
    p[0] = p[1]
    
# expr : alpha|bbeta|ggamma|delta|epsilon|theta|sigma|omega
def p_expr_greek_ch(p):
    'expr : GREEK_CH'
    p[0] = p[1]

# expr : +expr
def p_expr_plus_expr(p):
    'expr : PLUS expr %prec UPLUS' # override precedence of PLUS by `%prec UPLUS`
    p[0] = p[2]

# expr : -expr
def p_expr_minus_expr(p):
    'expr : MINUS expr %prec UMINUS' # override precedence of MINUS by `%prec UMINUS`
    p[0] = '(-1)*({})'.format(p[2])
    
# expr : pi
def p_expr_pi(p):
    'expr : PI'
    p[0] = S.Pi
 
# expr : imaginary_unit    
def p_expr_imaginary_unit(p):
    'expr : IMAGINARY_UNIT'
    p[0] = S.ImaginaryUnit

# expr : napier_constant
def p_expr_napier_constant(p):
    'expr : NAPIER_CONSTANT'
    p[0] = S.Exp1    

# expr : infty
def p_expr_infty(p):
    'expr : INFTY'
    p[0] = 'oo'

# expr :  \d+  
def p_expr_integer(p):
    'expr : NN_INTEGER'
    p[0] = p[1]
 
# expr :  \d*\.\d+ 
def p_expr_float(p):
    'expr : NN_FLOAT'
    #p[0] = 'nsimplify(Rational({}))'.format(p[1])
    p[0] = 'nsimplify({})'.format(p[1])
        
# expr : \sqrt{expr}
def p_expr_sqrt1(p):
    'expr : F_SQRT LBRACE expr RBRACE'
    p[0] = 'sqrt({})'.format(p[3])    
    
# expr : \sqrt[expr]{expr}
def p_expr_sqrt2(p):
    'expr : F_SQRT LBRACKET expr RBRACKET LBRACE expr RBRACE'
    #p[0] = '(root(({}),({})))'.format(p[6],p[3])
    p[0] = '(({})**(({})**(-1)))'.format(p[6],p[3])

# expr : \frac{expr}{expr}
def p_expr_frac(p):
    'expr : F_FRAC LBRACE expr RBRACE LBRACE expr RBRACE'
    p[0] = '({}) * ({})**(-1)'.format(p[3], p[6])   

# expr : \sin{expr} | \cos{expr} | \tan{expr} 
def p_expr_f_trigonometric(p):
    'expr : F_TRIG LBRACE expr RBRACE'
    p[0] = '{}({})'.format(p[1][1:], p[3])
     
# expr : \log{expr}
def p_expr_f_log(p):
    'expr : F_LOG LBRACE expr RBRACE'
    p[0] = 'log({})'.format(p[3])

# expr : \sin^{expr}{expr} | \cos^{expr}{expr} | \tan^{expr}{expr} 
def p_expr_f_trigonometric_car(p):
    'expr : F_TRIG_CAR LBRACE expr RBRACE LBRACE expr RBRACE'
    p[0] = '({}({}))**({})'.format(p[1][1:4],p[6],p[3])  

# expr : \log_{expr}{expr}
def p_expr_f_log_ub(p):
    'expr : F_LOG_UB LBRACE expr RBRACE LBRACE expr RBRACE '
    p[0] = 'log({})*(log({})**(-1))'.format(p[6],p[3])
    
# expr : \sum_{k=expr}^{expr}{expr}
def p_expr_sum(p):
    'expr : F_SUM  UB LBRACE ALPHABET EQUAL expr  RBRACE EXPONENT LBRACE expr RBRACE LBRACE expr RBRACE'
    p[0] = 'summation({},({},{},{}))'.format(p[13],p[4],p[6],p[10])
 
# expr : \frac{d}{dx} {expr}
def p_expr_diff(p):
    'expr : DIFF LBRACE DX RBRACE LBRACE expr RBRACE'
    x=p[3][1:]    
    if x=='aalpha' or x=='bbeta' or x=='ggamma' or x=='ttheta' or x=='oomega':
        p[0] = 'diff({},{})'.format(p[6], p[3][1:])
    else:
        p[0] = 'diff({},{})'.format(p[6], p[3][1]) 
    
# expr : \int{expr dx}
def p_expr_int(p):
    'expr : F_INT LBRACE expr DX RBRACE'
    x=p[4][1:]
    if x=='aalpha' or x=='bbeta' or x=='ggamma' or x=='ttheta' or x=='oomega':
        p[0] = 'integrate({},{})'.format(p[3],p[4][1:])
    else:
        p[0] = 'integrate({},{})'.format(p[3],p[4][1])    

# expr : \int^{expr}_{expr}{expr dx}
def p_expr_definite_int(p):
    'expr : F_INT UB LBRACE expr RBRACE EXPONENT LBRACE expr RBRACE LBRACE expr DX RBRACE'
    x=p[8][1:]
    if x=='aalpha' or x=='bbeta' or x=='ggamma' or x=='ttheta' or x=='oomega':
        p[0] = 'integrate({},({},{},{}))'.format(p[11],p[12][1:],p[4],p[8])
    else:
        p[0] = 'integrate({},({},{},{}))'.format(p[11],p[12][1],p[4],p[8])
    
# expr : \lim_{expr->expr}{expr}
def p_expr_lim(p):
    'expr : LIM UB LBRACE expr TO expr RBRACE LBRACE expr RBRACE'
    p[0] = 'limit({}, {}, {})'.format(p[9],p[4],p[6])
    

F=Function('F')
# expr : a_{expr}
def p_expr_seq_term(p):
    'expr : F_SEQ_TERM LBRACE expr RBRACE'
    p[0] = 'F({})'.format(p[3]) 
          
# expr : _{expr}C_{expr} |  _{expr}P_{expr}
def p_expr_combi_or_permutation(p):
    'expr : UB LBRACE expr RBRACE COMBI_PERMU UB LBRACE expr RBRACE'
    if p[5] == r'\C':
        p[0] = 'binomial({},{})'.format(p[3],p[8])
    elif p[5] == r'\P':
        p[0] = 'ff({},{})'.format(p[3],p[8])
        
# expr : \left| expr \right|
def p_expr_abs(p):
    'expr : LPIPE expr RPIPE'
    p[0] = 'Abs({})'.format(p[2])        
       


# statement : expr = expr
def p_statement_equal_expr(p):
    'statement : expr EQUAL expr'
    p[0] = 'Eq({},{})'.format(p[1],p[3])
  

# statement : expr > expr | expr < expr | expr >= expr | expr <= expr |
def p_statement_relation_expr(p):
    'statement : expr RELATION expr'
    if p[2] == '>':
        p[0] = '{}>{}'.format(p[1],p[3])
    elif p[2] == '<':
        p[0] = '{}<{}'.format(p[1],p[3])
    elif p[2] == '\\geq':
        p[0] = '{}>={}'.format(p[1],p[3])
    elif p[2] == '\\leq':
        p[0] = '{}<={}'.format(p[1],p[3])   


# Rule for error handling
def p_error(t):
    print("syntax error at '%s'" % (t.value))


# Generating LALR tables
#parser = yacc.yacc()
parser=yacc.yacc(errorlog=yacc.NullLogger())# to completely silence warnings

import logging
logging.basicConfig(
    level=logging.INFO,
    filename="parselog.txt"
)


def tex2sym(texexpr):
    replace_list=[['~',''],['\,',''],['\:',''],['\;',''],['\!',''], [r'\{','('],[r'\}', ')'],[r'\left(','('],[r'\right)', ')'],        
        [r'\alpha','aalpha'],[r'\beta','bbeta'],[r'\gamma','ggamma'],[r'\omega','oomega'],[r'\theta','ttheta']]
    for le in replace_list:
        texexpr=texexpr.replace(le[0],le[1]) 
    lexer.input(texexpr)
    sympyexpr = parser.parse(texexpr, lexer=lexer)
    #parser.parse(texexpr, debug=logging.getLogger()) # debug!
    return sympyexpr
 

def mylatex(sympyexpr):
    texexpr = latex(sympyexpr)
    replace_list=[['aalpha', r'\alpha '],['bbeta',r'\beta '],['ggamma',r'\gamma '],['oomega',r'\omega '],['ttheta',r'\theta ']]
    for le in replace_list:
        texexpr=texexpr.replace(le[0],le[1]) 
    return texexpr
    
def mylatexstyle(texexpr):
    replace_list=[[r'\ii',' i'],[r'\ee',' e'],[r'\ppi',r'\pi '],[r'\C',r'\mathrm{C}'],[r'\P',r'\mathrm{P}']]
    for le in replace_list:
        texexpr=texexpr.replace(le[0],le[1]) 
    return texexpr
 
        
if __name__ == '__main__':
    print(tex2sym(r'2^3'))
    print(tex2sym(r'0.5 \times 3 \div 5 \cdot 4'))
    print(tex2sym(r'2*a*b^2*c^3'))
    print(tex2sym(r'2ab^2c^3'))
    print(tex2sym(r'2AB^2C^3'))
    print(tex2sym(r'\sqrt{3x}'))
    print(tex2sym(r'\frac{2}{3}'))
    print(tex2sym(r'\sin {\ppi x}'))#\sin \ppi x bad
    print(tex2sym(r'\sin {x} \cos {x} \tan {x}'))
    print(tex2sym(r'\sin {x} + \cos {x} + \tan {x}'))
    print(tex2sym(r'\sin^{2}{x} \cos^{2}{x} \tan^{2}{x}'))#\sin^k x, \cos^{10} x bad 
    print(tex2sym(r'\sin^{3}{x} + \cos^{3}{x} + \tan^{3}{x}'))  
    print(tex2sym(r'\log{\ee^3}'))#\log \ee^3 bad
    print(tex2sym(r'\log_{2}{8}'))#\log_2 8 bad 
    print(tex2sym(r'\frac{d}{dx}{x^3}'))
    print(tex2sym(r'\int{\sin^{2}{x} dx}'))
    print(tex2sym(r'\int_{1}^{3}{(x-1)(x-3)^2 dx}')) 
    print(tex2sym(r'\sum_{k=1}^{n}{k^3}'))
    print(tex2sym(r'\lim_{x \to -\infty}{(\sqrt{x^2+3x}+x)}'))
    print(tex2sym(r'12a_{n+1}-35a_{n}'))#35a_n bad
    print(tex2sym(r'2x^2+3x+4=0'))
    print(tex2sym(r'x^2-3x-4 \leq 0'))
    print(tex2sym(r'\left| \left| 3-\ppi \right|-1\right|'))#| | 3 - \ppi | -1 | bad
    print(tex2sym(r'10!'))
    print(tex2sym(r'_{5}\C_{2}'))#_5C_2 bad
    print(tex2sym(r'_{5}\P_{2}'))#_5P_2 bad
    print(tex2sym(r'-x^2'))
    print(tex2sym(r'\{a-2(b-c)\}^2'))
    print(tex2sym(r'\left\{a-2(b-c)\right\}^2'))
    print(tex2sym(r'\left\{A-2(B-C)\right\}^2'))
    
    
