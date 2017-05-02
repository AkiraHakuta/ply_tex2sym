# tex2sym_lexer.py   Author: Akira Hakuta, Date: 2017/05/02
# python.exe tex2sym_lexer.py

from ply import lex

# List of token names.
tokens = ('EXPONENT', 'FACTORIAL', 'MULT', 'DIV', 'PLUS', 'MINUS',
        'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN','UB', 'LBRACKET','RBRACKET',
        'LPIPE', 'RPIPE',
        'PI', 'IMAGINARY_UNIT', 'NAPIER_CONSTANT', 
        'NN_FLOAT', 'GREEK_CH', 'DX','NN_INTEGER','ALPHABET',
        'LIM', 'INFTY', 'TO', 'DIFF',       
        'F_FRAC', 'F_SQRT',  'F_TRIG','F_TRIG_CAR', 'F_LOG','F_LOG_UB','F_SUM', 'F_INT', 'F_SEQ_TERM',
        'COMBI_PERMU',
        'EQUAL', 'RELATION',)

# Define `t_ignore` to ignore unnecessary characters between tokens, such as whitespaces.
t_ignore = " \t"
  

# Define functions representing regular expression rules for each token.
# The name of functions must be like `t_<token_name>`.
# All tokens defined by functions are added in the same order as they appear in the lexer file.

def t_EXPONENT(t):
    r'\^'
    return t
 
def t_FACTORIAL(t):
    r'!'
    return t    

def t_MULT(t):
    r'\*|\\times|\\cdot'
    return t

def t_DIV(t):
    r'\\div'
    return t  
    
def t_PLUS(t):
    r'\+' 
    return t

def t_MINUS(t):
    r'\-'
    return t


def t_LBRACE(t):
    r'\{'
    return t

def t_RBRACE(t):
    r'\}'
    return t
   
    
def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_LBRACKET(t):
    r'\['
    return t

def t_RBRACKET(t):
    r'\]'
    return t

def t_LPIPE(t):
    r'\\left\|'
    return t
    
def t_RPIPE(t):
    r'\\right\|'
    return t    
    
    
def t_PI(t):
    r'\\ppi'
    return t
    
def t_IMAGINARY_UNIT(t):
    r'\\ii'
    return t
    
def t_NAPIER_CONSTANT(t):
    r'\\ee'
    return t  
    
def t_GREEK_CH(t):
    r'aalpha|bbeta|ggamma|ttheta|oomega'
    return t

def t_DX(t):
    r'daalpha|dbbeta|dggamma|dttheta|doomega|d[a-z]'
    return t
    
def t_NN_FLOAT(t):
    r'\d*\.\d+'
    return t
    
def t_NN_INTEGER(t):
    r'\d+'
    return t  
      
def t_F_SEQ_TERM(t):
    r'[a-z]_'
    return t
    
def t_ALPHABET(t):
    r'[a-zABCXYZ]'
    return t
    

   
def t_DIFF(t):
    r'\\frac\{d\}'
    return t    
 
def t_F_FRAC(t):
    r'\\frac'
    return t
         
def t_F_SQRT(t):
    r'\\sqrt'
    return t
        
def t_F_TRIG_CAR(t):
    r'\\sin\^|\\cos\^|\\tan\^'
    return t
    
def t_F_TRIG(t):
    r'\\sin|\\cos|\\tan'
    return t
    
def t_F_LOG_UB(t):
    r'\\log_'
    return t
    
def t_F_LOG(t):
    r'\\log'
    return t
    
def t_UB(t):
    r'_'
    return t   
    
def t_F_SUM(t):
    r'\\sum'
    return t

def t_LIM(t):
    r'\\lim'
    return t

def t_INFTY(t):
    r'\\infty'
    return t
    
def t_TO(t):
    r'\\to'
    return t
 
    
def t_F_INT(t):
    r'\\int'
    return t
    
def t_COMBI_PERMU(t):
    r'\\C|\\P'
    return t
    
    


def t_EQUAL(t):
    r'='
    return t
    
def t_RELATION(t):
    r'>|<|\\geq|\\leq'
    return t
    



# To count correct line number
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    # return None, so this newlines will not be in the parsed token list.


# Special function for error handling
def t_error(t):
    print("illegal character '%s'" % (t.value[0]))
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

def test_lexer(input_string):
    lexer.input(input_string)
    result = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        result = result + [(tok.value,tok.type)]
    return result

if __name__ == '__main__':
    print(test_lexer(r'123.456'))
    print(test_lexer(r'2^3'))
    print(test_lexer(r'0.5 \times 3 \cdot 4 \div 5'))
    print(test_lexer(r'2*a*b^2*c^3'))
    print(test_lexer(r'2ab^2c^3'))
    print(test_lexer(r'\sqrt{3x}'))
    print(test_lexer(r'\frac{2}{3}'))
    print(test_lexer(r'\sin {\ppi x}'))
    print(test_lexer(r'\sin {x} \cos {x} \tan {x}'))
    print(test_lexer(r'\sin {x} + \cos {x} + \tan {x}'))
    print(test_lexer(r'\sin^{2}{x} \cos^{2}{x} \tan^{2}{x}'))#\sin^k x, \cos^{10} x bad 
    print(test_lexer(r'\sin^{3}{x} + \cos^{3}{x} + \tan^{3}{x}'))  
    print(test_lexer(r'\log{\ee^3}'))#\log \ee^3 bad
    print(test_lexer(r'\log_{2}{8}'))#\log_2 8 bad 
    print(test_lexer(r'\frac{d}{dx}{x^3}'))
    print(test_lexer(r'\int{\sin^{2}{x} dx}'))
    print(test_lexer(r'\int_{1}^{3}{(x-1)(x-3)^2 dx}')) 
    print(test_lexer(r'\sum_{k=1}^{n}{k^3}'))
    print(test_lexer(r'\lim_{x \to -\infty}{(\sqrt{x^2+3x}+x)}'))
    print(test_lexer(r'12a_{n+1}-35a_{n}'))
    print(test_lexer(r'2x^2+3x+4=0'))
    print(test_lexer(r'x^2-3x-4 \leq 0'))
    print(test_lexer(r'\left| \left| 3-\ppi \right|-1\right|'))
    print(test_lexer(r'10!'))
    print(test_lexer(r'_{5}\C_{2}'))
    print(test_lexer(r'_{5}\P_{2}'))    
     
    