import sys
from ply import lex
from ply import yacc
# expresiones regulares
error = False
reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'print' : 'PRINT',
   'program': 'PROGRAM',
   'var' : 'VAR',
   'int' : 'INT' ,
   'float' : 'FLOAT'
}

tokens = [
  'CTEI', 'CTEF', 'CTESTRING',
  'ID', 'PLUS', 'MINUS',
  'MULTIPLY', 'EQUALS', 'DIVIDE',
  'RIGHTPAR', 'LEFTPAR', 'DOT',
  'SEMICOLON', 'COLON', 'LEFTCURL',
  'RIGHTCURL', 'GREATER', 'LESS',
  'DIFFERENT'
] + list(reserved.values())

t_PLUS = r'\+'
t_DIVIDE = r'\/'
t_EQUALS = r'\='
t_RIGHTPAR = r'\)'
t_LEFTPAR = r'\('
t_DOT = r'\.'
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_LEFTCURL = r'\{'
t_RIGHTCURL = r'\}'
t_GREATER = r'\>'
t_LESS = r'\<'
t_DIFFERENT = r'\<>'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_CTESTRING = r'\".*\"'

t_ignore = r' '

def t_CTEF(t):
  r'[-+]?(\d*\.\d*)'
  t.value = float(t.value)
  return t

def t_CTEI(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value, 'ID')
  return t

def t_error(t):
  print("Illegal characters")
  print(t)
  t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

lexer = lex.lex()
start = 'programa'

# gramatica regular 

def p_estatuto(p):
  '''
  estatuto : asignacion 
           | condicion
           | escritura
  '''

def p_condicion(p):
  '''
  condicion : condicion_aux bloque SEMICOLON 
            | condicion_aux bloque ELSE bloque SEMICOLON
  '''

def p_condicion_aux(p):
  '''
  condicion_aux : IF LEFTPAR expresion RIGHTPAR
  '''

def p_asignacion(p):
  '''
  asignacion : ID EQUALS expresion SEMICOLON
  '''

def p_expresion(p):
  '''
  expresion : exp comp 
            | exp
  '''

def p_comp(p):
  '''
  comp : LESS exp 
       | GREATER exp
       | DIFFERENT exp
  '''

def p_exp(p):
  '''
  exp : termino op 
      | termino
  '''

def p_op(p):
  '''
  op : PLUS exp 
     | MINUS exp
  '''
def p_termino(p):
  '''
  termino : factor 
          | factor termino_aux
  '''

def p_termino_aux(p):
  '''
  termino_aux : MULTIPLY termino 
              | DIVIDE termino
  '''

def p_factor(p):
  '''
  factor : LEFTPAR expresion RIGHTPAR 
         | factor_aux
  '''

def p_factor_aux(p):
  '''
  factor_aux : PLUS varcte 
             | MINUS varcte 
             | varcte
  '''

def p_varcte(p):
  '''
  varcte : ID 
         | CTEI 
         | CTEF
  '''

def p_tipo(p):
  '''
  tipo : INT
       | FLOAT
  '''

def p_escritura(p):
  '''
  escritura : PRINT LEFTPAR aux_escritura RIGHTPAR SEMICOLON
  '''

def p_aux_escritura(p):
  '''
  aux_escritura : expresion
                | expresion DOT aux_escritura
                | CTESTRING DOT aux_escritura
                | CTESTRING
  '''
def p_vars(p):
  '''
  vars : VAR aux_var
  '''

def p_aux_var(p):
  '''
  aux_var : ID COLON tipo SEMICOLON
          | ID COLON tipo SEMICOLON aux_var
          | ID COLON aux_var
  '''

def p_programa(p): 
  '''
  programa : PROGRAM ID COLON vars bloque
           | PROGRAM ID COLON bloque 
  '''

def p_bloque(p):
  '''
  bloque : LEFTCURL aux_bloque RIGHTCURL

  '''
def p_aux_bloque(p):
  '''
  aux_bloque : estatuto
             | estatuto aux_bloque
  '''
def p_error(p): 
  global error
  error = True
  #print("ERROR {}".format(p), error)

def p_empty(p):
  '''
  empty : 
  '''
  p[0] = None

parser = yacc.yacc()

if __name__ == '__main__':
  try:
    arch_name = 'prueba-2.txt'
    arch = open(arch_name,'r')
    print("Nombre de archivo " + arch_name)
    archivo = arch.read()
    arch.close()
    yacc.parse(archivo)
    # #print(lexer.input(archivo))
    # while True:
    #   tok = lexer.token()
    #   if not tok:
    #       break      # No more input
    #   print(tok)

    if error: 
      print("hay errores de sintaxis")
    else:
      print("apropiado")  


  except EOFError:
    print(EOFError)