import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'PLUS', 'MINUS', 'COMMA',
    'NUMBER', 'OPEN', 'CLOSE',
)

t_PLUS      = r'\+'
t_MINUS     = r'-'
t_COMMA     = r','
t_OPEN      = r'\['
t_CLOSE     = r'\]'
t_NUMBER    = r'\-?\d+'

t_ignore    = ' '

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

mode = None
intervals = []
def p_mode(t):
    '''mode : PLUS intervals
            | MINUS intervals'''
    intervals.reverse()
    for i in range(0, len(intervals)):
        if t[1] == '-':
            if intervals[i][2] >= 0:
                raise Exception(f"Error: Interval is invalid ({str(intervals[i])})")

        if i > 0:
            if ((t[1] == '-' and intervals[i-1][1] <= intervals[i][0]) 
               or (t[1] == '+' and intervals[i-1][1] >= intervals[i][0])):
                raise Exception("Error: Intervals are not in sequence " + str(intervals[i-1]) + " -> " + str(intervals[i]))

def p_intervals(t):
    '''intervals : interval intervals
                 | interval'''
    intervals.append(t[1])

def p_interval(t):
    'interval : OPEN NUMBER COMMA NUMBER CLOSE'
    t[0] = [int(t[2]), int(t[4]), int(t[4]) - int(t[2])]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()

while True:
    mode = None
    intervals = []
    try:
        s = input('$ ')
    except EOFError as e:
        print(e)
        break
    try:
        parser.parse(s)
    except Exception as e:
        print(e)