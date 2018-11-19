from parser import Parser
from lexer import Lexer



def test_basic_select():
    ast = Parser(Lexer("SELECT * FROM EDGES"))).parse()
    # assert(ast == [])

