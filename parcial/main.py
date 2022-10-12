import pandas as pd
import graphviz
from tokens import tokensLexer as tokens 
tokens.append({ 'type': '$',
    'lexeme': '$',
    'line': 1})

lista = [
  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
  'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'BA', 'CA', 'DA', 'EA', 'FA', 'GA', 'HA', 'IA', 'JA', 'KA', 'LA', 'MA', 'NA', 'OA',
  'PA', 'QA', 'RA', 'SA', 'TA', 'UA', 'VA', 'WA', 'XA', 'YA', 'ZA', 'AB', 'BB', 'CB', 'DB', 'EB', 'FB', 'GB', 'HB', 'IB', 'JB', 'KB', 'LB', 'MB', 'NB', 'OB',
  'PB', 'QB', 'RB', 'SB', 'TB', 'UB', 'VB', 'WB', 'XB', 'YB', 'ZB', 'AC', 'BC', 'CC', 'DC', 'EC', 'FC', 'GC', 'HC', 'IC', 'JC', 'KC', 'LC', 'MC', 'NC', 'OC',
  'PC', 'QC', 'RC', 'SC', 'TC', 'UC', 'VC', 'WC', 'XC', 'YC', 'ZC', 'AD', 'BD', 'CD', 'DD', 'ED', 'FD', 'GD', 'HD', 'ID', 'JD', 'KD', 'LD', 'MD', 'ND', 'OD',
  'PD', 'QD', 'RD', 'SD', 'TD', 'UD', 'VD', 'WD', 'XD', 'YD', 'ZD'
]  

counter = 0
syntax_table = pd.read_csv("compiladores.csv", index_col=0)
dot = graphviz.Digraph('hello')



def print_stack():
  print("\nStack:")
  for e in stack:
    print(e.symbol, "-", e.is_terminal)
  print()


def print_input():
  print("\nInput:")
  for t in tokens:
    print(t['type'], ",", t['lexeme'])
  print()


#----------------------------------------------------------------


#Clases ----------------------------------------------------------
class node_stack:

  def __init__(self, symbol, terminal, val):
    global counter
    self.id = counter
    self.symbol = symbol  # simbolo de la gramatica
    self.is_terminal = terminal  # para saber si es terminal
    self.val = val
    counter += 1


class node_parser:

  def __init__(self,
               node_st,
               lexeme=None,
               children=[],
               father=None,
               line=None):

    self.node_st = node_st
    self.lexeme = lexeme
    self.line = line
    self.children = children
    self.father = father

  def insert_arbol(self, val):
    self.children.insert(0, val)


#----------------------------------------------------------------
#Funciones ------------------------------------------------------

#retorna nodo no terminal 
# simbol coincid ey tiene hijos en 0 
# sym no coincide y tiene hujos en cero
def find_node(node, val):
  stack = [node]

  while len(stack) != 0:

    if stack[0].node_st.symbol == val and len(stack[0].children) == 0:
      return stack[0]
      break

    if stack[0].node_st.symbol != val and len(stack[0].children) == 0:
      stack.pop(0)

    if len(stack[0].children) > 0:

      temp = stack[0].children

      stack.pop(0)
      for i in temp:
        stack.insert(0, i)
  return None


def print_arbol(root):
  stack = [root]
  
  while len(stack) != 0:
    
    if len(stack[0].children) > 0:
      print(stack[0].node_st.symbol)

      temp = stack[0].children
      stack.pop(0)

      for i in temp:
        stack.insert(0, i)
    else:
      print(stack[0].node_st.symbol)
      stack.pop(0)


#----------------------------------------------------------------
#Update stack ---------------------------------------------------
# busca en la tabla la produccipon
def update_stack(stack, token_type):
  production = syntax_table.loc[stack[0].symbol][token_type]

  if str(production) == 'nan':
    return False
  else:
    elementos = production.split(" ")
    elementos.pop(0) #eliminas valores que no interesa
    elementos.pop(0)

    # eliminar el ultimo elemento de la pila
    find = find_node(root, stack[0].symbol)

    temp = stack[0].val
    #guardo en temp y  elimino
    stack.pop(0)

    if elementos[0] == "''":
      symbol = node_stack('Ɛ', True, lista[counter - 1])
      new = node_parser(symbol, father=find, children=[])
      
      dot.node(symbol.val, 'Ɛ') # crea
      dot.edge(temp, symbol.val)# une temp + actuañ
      
      find.insert_arbol(new)
      return True

    # insertar production a la stack
    rever = list(reversed(elementos))
    
    # val de cada uno de los symbolos
    symbols = []
    
    for i in rever:

      bool = i.isupper()
      symbol = node_stack(i, not bool, lista[counter - 1])
      new = node_parser(symbol, father=find, children=[])
      symbols.append(symbol)

      find.insert_arbol(new)

      stack.insert(0, symbol)

    for i in range(len(symbols)-1, -1, -1):
      
      dot.node(symbols[i].val, symbols[i].symbol)
      dot.edge(temp, symbols[i].val)
    
    return True


#----------------------------------------------------------------

stack = []
symbol_1 = node_stack('$', True, '')
symbol_2 = node_stack('PROGMAIN', False, 'A')
stack.insert(0, symbol_1)
stack.insert(0, symbol_2)

dot.node(lista[counter - 2], stack[0].symbol)
# ('A', 'E')
root = node_parser(symbol_2)



#Si el $ es igual q $
while True:
  print("ITERATION ...")
  print_stack()
  print_input()
  if stack[0].symbol == '$' and tokens[0]['type'] == '$':
    print("Todo bien!")
    break

  # cuando son terminales
  if stack[0].is_terminal:
    print("terminales ...")
    if stack[0].symbol == tokens[0]['type']:
      stack.pop(0)
      tokens.pop(0)
    else:
      print("ERROR sintáctico")
      break

  # cuando reemplazar en la pila, según tabla sintáctica
  else:
    if not update_stack(stack, tokens[0]['type']):
      print("ERROR sintáctico")
      break
  
      
      
dot.format = 'svg'

dot.render(directory='doctest-output').replace('\\', '/')
'doctest-output/hello.gv.svg'