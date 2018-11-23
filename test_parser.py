from lexer import Lexer
from dagql_parser import Parser
from tokens import TokenTypes, Token


def test_basic_select():
    input_program = """
    SELECT * FROM EDGES
    """

    ast = Parser(Lexer(input_program).lex()).parse()
    assert(ast[0].subquery == Token(TokenTypes.KW, "EDGES", 2))

def test_muti_statement_program():
    input_program = """
    SELECT * FROM EDGES
    SELECT * FROM NODES
    """

    ast = Parser(Lexer(input_program).lex()).parse()
    assert(ast[0].subquery == Token(TokenTypes.KW, "EDGES", 2))
    assert(ast[1].subquery == Token(TokenTypes.KW, "NODES", 3))

def test_nested_select():
    input_program = """
    SELECT a FROM (SELECT b FROM NODES)
    """

    ast = Parser(Lexer(input_program).lex()).parse()
    assert(ast[0].args[0].token == Token(TokenTypes.ID, 'a', 2))

def test_WHERE_WITH_TRUE():
    input_program = """
    SELECT a FROM EDGES WHERE TRUE
    """
    ast = Parser(Lexer(input_program).lex()).parse()

def test_WHERE_WITH_FALSE():
    input_program = """
    SELECT a FROM EDGES WHERE FALSE
    """
    ast = Parser(Lexer(input_program).lex()).parse()

def test_where_with_clause():
    input_program = """
    SELECT * FROM EDGES WHERE type = 'process_memory'
    """
    ast = Parser(Lexer(input_program).lex()).parse()

def test_where_with_not():
    input_program = """
    SELECT * FROM EDGES WHERE NOT type = 'process_memory'
    """
    ast = Parser(Lexer(input_program).lex()).parse()


def test_where_with_and():
    input_program = """
    SELECT * FROM EDGES WHERE type = 'process_memory' AND id = 24102
    """
    ast = Parser(Lexer(input_program).lex()).parse()

def test_where_with_or():
    input_program = """
    SELECT * FROM EDGES WHERE type = 'process_memory' OR type = 'task'
    """
    ast = Parser(Lexer(input_program).lex()).parse()

def test_traverse_by_depth():
    input_program = """
    SELECT a, b FROM NODES TRAVERSE BY DEPTH 
    """
    ast = Parser(Lexer(input_program).lex()).parse()

def test_traverse_by_breadth():
    input_program = """
    SELECT a, b FROM NODES TRAVERSE BY DEPTH 
    """
    ast = Parser(Lexer(input_program).lex()).parse()

def test_limit():
    input_program = """
    SELECT * FROM EDGES LIMIT 10
    """
    ast = Parser(Lexer(input_program).lex()).parse()
