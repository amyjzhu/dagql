from .lexer import Lexer, LexerError
from .parser import Parser, ParserError
from .interpreter import Interpreter, InterpreterError
import sys

def main():
    compiler = Interpreter()
    while True:
        try:
            text = input("DAGQL> ")
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer.lex())
        statements = parser.parse() # = Interpreter(parser)
        result = compiler.compile(statements)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    else:
        assert(len(sys.argv) == 2)
        text = open(sys.argv[1]).read() #TODO: make more general, so file can be located anywhere
        try:
            statements = Parser(Lexer(text).lex()).parse()
            compiler = Interpreter()
            compiler.compile(statements)
        except (LexerError, ParserError, InterpreterError) as e:
            print(e)
