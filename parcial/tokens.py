# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

# r'atring' -> r significa que la cadena es tradada sin caracteres de escape,
# es decir r'\n' seria un \ seguido de n (no se interpretaria como salto de linea)

# List of token names.   This is always required
reserved = {
  'si': 'if',
  'sino': 'else',
  'para': 'for',
  'mientras': 'while',
  'salir': 'break',
  'funcion': 'function',
  'retornar': 'return',
  'variable': 'var',
  'constante': 'const',
  'temporal': 'let',
  'y': 'and',
  'o': 'or',
  'verdadero': 'true',
  'falso': 'false'
}

tokens = [
  'number', 'plus', 'minus', 'multi', 'divide', 'lparen', 'rparen', 'equality',
  'assynament', 'lsb', 'rsb', 'lb', 'rb', 'greater', 'minor', 'greaterequal',
  'menorequal', 'string', 'id', 'distinct', 'comma', 'semicolon', 'power'
] + list(reserved.values())


def t_id(t):
  r'[a-za-z]+ ([a-za-z0-9]*)'
  t.type = reserved.get(t.value, 'id')
  return t

# regular expression rules for simple tokens
t_plus = r'\+'
t_minus = r'-'
t_multi = r'\*'
t_divide = r'/'
t_power = r'\*\*'

t_assynament = r'\='
t_equality = r'\=='
t_distinct = r'\!='

t_lparen = r'\('
t_rparen = r'\)'
t_lsb = r'\['
t_rsb = r'\]'
t_lb = r'\{'
t_rb = r'\}'
t_comma = r','
t_semicolon = r';'

t_greater = r'\>'  # mayor
t_minor = r'\<'  # menor
t_greaterequal = r'\>='  # mayor igual
t_menorequal = r'\<='  # menor igual

# t_TAB        = '\t'
# t_LINEBREAK  = '\n'

t_number = r'[-+]?([\d]+)(.[\d]+)?'


# A regular expression rule with some action code
def t_string(t):
  r'"([a-zA-Z0-9]*( )*)+"'
  t.value = str(t.value)  # guardamos el valor del lexema
  #print("se reconocio el numero")
  return t


def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Test it out
f = open('mientras.txt', 'r')
data = f.read()

# Give the lexer some input
lexer.input(data)
tokensLexer = []

# Tokenize
while True:
  tok = lexer.token()
  if not tok:
    break  # No more input
  #print(tok)
  tokensLexer.append({
    'type': tok.type,
    'lexeme': tok.value,
    'line': tok.lineno
  })
  print(tok.type, tok.value, tok.lineno, tok.lexpos)
f.close()
