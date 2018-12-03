from dagql.lexer import Lexer
from dagql.tokens import TokenTypes, Token


def test_all():
    l = Lexer("SELECT FROM TRAVERSE BY DEPTH BREADTH WHERE LIMIT TRUE FALSE AND OR NOT > < >= <= = <> + - * / ||")
    t = l.lex() 
    assert(t == [
      Token(TokenTypes.KW, "SELECT", 1),
      Token(TokenTypes.KW, "FROM", 1),
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
    l = Lexer("-- This is a simple query\nSELECT a")
    t = l.lex()
    assert(t == [
      Token(TokenTypes.KW, "SELECT", 2),
      Token(TokenTypes.ID, "a", 2),
    ])

def test_string():
    l = Lexer("'this is a string' || 'so is this'")
    t = l.lex()
    assert(t == [
      Token(TokenTypes.STR, "this is a string", 1),
      Token(TokenTypes.OP, "||", 1),
      Token(TokenTypes.STR, "so is this", 1),
    ])

def test_num():
    l = Lexer("10 10. 10.0 0.5 .5 1.5")
    t = l.lex()
    assert(t == [
      Token(TokenTypes.NUM, 10.0, 1),
      Token(TokenTypes.NUM, 10.0, 1),
      Token(TokenTypes.NUM, 10.0, 1),
      Token(TokenTypes.NUM, 0.5, 1),
      Token(TokenTypes.NUM, 0.5, 1),
      Token(TokenTypes.NUM, 1.5, 1),
    ])

def test_id():
    l = Lexer("SELECT a LIMIT 10")
    t = l.lex()
    assert(t == [
      Token(TokenTypes.KW, "SELECT", 1),
      Token(TokenTypes.ID, "a", 1),
      Token(TokenTypes.KW, "LIMIT", 1),
      Token(TokenTypes.NUM, 10.0, 1),
    ])
     
