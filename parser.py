from tokens import TokenTypes, Token
from ast import *

###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0]
        #self.next_token = self.self.tokens[1]
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TokenTypes.EOF, None, self.tokens[-1].line)
        #self.next_token = self.tokens[self.pos]
    def error(self,token_type=None):
        raise Exception("Expected %s Token in line %s, got %s" % \
            (token_type, self.current_token.line, self.current_token.type))
    def eat(self, token_type):
        print(self.current_token)
        if self.current_token.type is token_type:
            result = self.current_token
            self.advance()
            return result
        else:
            self.error(token_type)
    def program(self):
        return self.select()
    def expr(self):
        """ Precedence Table for operators (tightest to loosest)
           + - (unary)
           * /
           + - (binary)
           ||
           = <> < > <= >=
           NOT
           AND
           OR
        """
        return self.or_expr()
    def or_expr(self):
        curr = self.and_expr()
        while self.current_token.type is TokenTypes.OP and self.current_token.value == "OR":
            op = self.eat(TokenTypes.OP)
            curr = BinOp(op, curr, self.and_expr())
        return curr
    def and_expr(self):
        curr = self.not_expr()
        while self.current_token.type is TokenTypes.OP and self.current_token.value == "AND":
            op = self.eat(TokenTypes.OP)
            curr = BinOp(op, curr, self.not_expr())
        return curr
    def not_expr(self):
        if self.current_token.type is TokenTypes.OP and self.current_token.value == "NOT":
            op = self.eat(TokenTypes.OP)
            return UnOp(op, self.not_expr())
        return self.comparator()
    def comparator(self):
        curr = self.concat()
        while self.current_token.type is TokenTypes.OP and self.current_token.value in ("=", "<>", "<", ">", "<=", ">="):
            op = self.eat(TokenTypes.OP)
            curr = BinOp(op, curr, self.concat())
        return curr
    def concat(self):
        curr = self.add()
        while self.current_token.type is TokenTypes.OP and self.current_token.value == "||":
            op = self.eat(TokenTypes.OP)
            return BinOp(op, curr, self.concat())
        return curr
    def add(self):
        curr = self.multiply()
        while self.current_token.type is TokenTypes.OP and self.current_token.value in ("+", "-"):
            op = self.eat(TokenTypes.OP)
            curr = BinOp(op, curr, self.multiply())
        return curr
    def multiply(self):
        curr = self.unop()
        while self.current_token.type is TokenTypes.OP and self.current_token.value in ("*", "/"):
            op = self.eat(TokenTypes.OP)
            curr = BinOp(op, curr, self.unop())
        return curr
    def unop(self):
        if self.current_token.type is TokenTypes.OP and self.current_token.value in ("-", "+"):
            op = self.eat(TokenTypes.OP)
            return UnOp(op, self.unop())
        return self.literal()
    def literal(self):
        if self.current_token.type is TokenTypes.LPAREN:
            self.eat(TokenTypes.LPAREN)
            expr = self.expr()
            self.eat(TokenTypes.RPAREN)
            return expr
        elif self.current_token.type is TokenTypes.ID:
            var = self.eat(TokenTypes.ID)
            return Var(var)
        elif self.current_token.type is TokenTypes.STR:
            string = self.eat(TokenTypes.STR)
            return String(string)
        elif self.current_token.type is TokenTypes.NUM:
            integer = self.eat(TokenTypes.NUM)
            return Number(integer)
        elif self.current_token.type is TokenTypes.BOOL:
            boolean = self.eat(TokenTypes.BOOL)
            return Boolean(boolean)
    def parse(self):
        statements = []
        while self.current_token.type is not TokenTypes.EOF:
            statements.append(self.program())
        for statement in statements: print(statement)
        return statements
