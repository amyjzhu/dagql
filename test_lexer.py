from lexer import Lexer
from tokens import TokenTypes, Token




def test_all():
    l = Lexer("SELECT FROM EDGES NODES TRAVERSE BY DEPTH BREADTH WHERE LIMIT TRUE FALSE AND OR NOT > < >= <= = <> + - * / ||")
    t = l.lex() 
    assert(t == [
      Token(TokenTypes.KW, "SELECT", 1),
      Token(TokenTypes.KW, "FROM", 1),
      Token(TokenTypes.KW, "EDGES", 1),
      Token(TokenTypes.KW, "NODES", 1),
      Token(TokenTypes.KW, "TRAVERSE", 1),
      Token(TokenTypes.KW, "BY", 1),
      Token(TokenTypes.KW, "DEPTH", 1),
      Token(TokenTypes.KW, "BREADTH", 1),
      Token(TokenTypes.KW, "WHERE", 1),
      Token(TokenTypes.KW, "LIMIT", 1),
      Token(TokenTypes.BOOL, True, 1),
      Token(TokenTypes.BOOL, False, 1),
      Token(TokenTypes.OP, "AND", 1),
      Token(TokenTypes.OP, "OR", 1),
      Token(TokenTypes.OP, "NOT", 1),
      Token(TokenTypes.OP, ">", 1),
      Token(TokenTypes.OP, "<", 1),
      Token(TokenTypes.OP, ">=", 1),
      Token(TokenTypes.OP, "<=", 1),
      Token(TokenTypes.OP, "=", 1),
      Token(TokenTypes.OP, "<>", 1),
      Token(TokenTypes.OP, "+", 1),
      Token(TokenTypes.OP, "-", 1),
      Token(TokenTypes.OP, "*", 1),
      Token(TokenTypes.OP, "/", 1),
      Token(TokenTypes.OP, "||", 1),
    ])

def test_comment():
    l = Lexer("-- This is a simple query\nSELECT * FROM NODES")
    t = l.lex()
    assert(t == [
      Token(TokenTypes.KW, "SELECT", 2),
      Token(TokenTypes.OP, "*", 2),
      Token(TokenTypes.KW, "FROM", 2),
      Token(TokenTypes.KW, "NODES", 2),
    ])
