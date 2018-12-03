from dagql.backend import TraversalOrder
from .tokens import TokenTypes, Token
from .ast import *

###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class ParserError(Exception):
    pass

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
        raise ParserError("Error:Expected %s in line %s, got `%s`." % \
            (token_type, self.current_token.line, self.current_token))
    def eat(self, token_type):
        if self.current_token.type is token_type:
            result = self.current_token
            self.advance()
            return result
        else:
            self.error(token_type)
    def eat_kw(self, *args):
        if self.current_token.type is TokenTypes.KW and self.current_token.value in args:
            result = self.current_token
            self.advance()
            return result
        else:
            if len(args) == 1:
                self.error('`' + args[0] + '`')
            else:
                msg = "one of "
                for i in args:
                    msg += '`' + i + '`, '
                self.error(msg.strip(', '))
    def program(self):
        return self.select()
    def select(self):
        self.eat_kw("SELECT")
        exprs = []
        exprs.append(self.expr())
        while self.current_token.type is not TokenTypes.KW and self.current_token.value != "FROM":
            self.eat(TokenTypes.COMMA)
            exprs.append(self.expr())
        self.eat_kw("FROM")
        subquery = self.subquery()
        self.eat_kw("AS")
        node = self.eat(TokenTypes.ID)
        start, end = None, None
        if self.current_token.type is TokenTypes.LPAR:
            self.eat(TokenTypes.LPAR)
            start = self.eat(TokenTypes.ID)
            self.eat(TokenTypes.COMMA)
            end = self.eat(TokenTypes.ID)
            self.eat(TokenTypes.RPAR)
        if start and end and (isinstance(subquery, SearchNode) or isinstance(subquery, Nodes)):
            raise Exception("Expected subquery over edges and got subquery over nodes")
        if not start and not end and (isinstance(subquery, SearchEdge) or isinstance(subquery, Edges)):
            raise Exception("Expected subquery over nodes and got subquery over edges")
        traversal_order = None
        if self.current_token.type is TokenTypes.KW and self.current_token.value == "TRAVERSE":
            self.eat_kw("TRAVERSE")
            self.eat_kw("BY")
            traversal_order = self.eat_kw("DEPTH", "BREADTH")
            if traversal_order.value == "DEPTH":
                traversal_order = TraversalOrder.DFS
            else:
                traversal_order = TraversalOrder.BFS
        if start and end:
            return SelectEdge(exprs, node, start, end, subquery, traversal_order or TraversalOrder.DFS)
        else:
            return SelectNode(exprs, node, subquery, traversal_order or TraversalOrder.DFS)
    def subquery(self):
        if self.current_token.type is TokenTypes.LPAR:
            self.eat(TokenTypes.LPAR)
            self.eat_kw("SEARCH")
            subquery = self.subquery()
            cond = None
            start, end = None, None
            node = None
            limit = None
            if self.current_token.type is TokenTypes.KW and self.current_token.value == 'AS':
                self.eat_kw("AS")
                node = self.eat(TokenTypes.ID)
                start, end = None, None
                if self.current_token.type is TokenTypes.LPAR:
                    self.eat(TokenTypes.LPAR)
                    start = self.eat(TokenTypes.ID)
                    self.eat(TokenTypes.COMMA)
                    end = self.eat(TokenTypes.ID)
                    self.eat(TokenTypes.RPAR)
                if start and end and (isinstance(subquery, SearchNode) or isinstance(subquery, Nodes)):
                    raise Exception("Expected subquery over edges and got subquery over nodes")
                if not start and not end and (isinstance(subquery, SearchEdge) or isinstance(subquery, Edges)):
                    raise Exception("Expected subquery over nodes and got subquery over edges")
                self.eat_kw("WHERE")
                cond = self.expr()
            if self.current_token.type is TokenTypes.KW and self.current_token.value == 'LIMIT':
                self.eat_kw("LIMIT")
                limit = self.expr()
            self.eat(TokenTypes.RPAR)
            if isinstance(subquery, SearchEdge) or isinstance(subquery, Edges):
                return SearchEdge(subquery, node, start, end, cond, limit)
            else:
                return SearchNode(subquery, node, cond, limit)
        subquery = self.eat_kw("NODES", "EDGES")
        if subquery.value == "NODES":
            return Nodes()
        elif subquery.value == "EDGES":
            return Edges()
    def select_edge(self):
        self.eat_kw("SELECT")
        name = self.eat(TokenTypes.ID)
        self.eat(TokenTypes.LPAR)
        start = self.eat(TokenTypes.ID)
        self.eat(TokenTypes.COMMA)
        end = self.eat(TokenTypes.ID)
        self.eat(TokenTypes.RPAR)
        subquery = None
        if self.current_token.type is TokenTypes.KW and self.current_token.value == "FROM":
            self.eat_kw("FROM")
            if self.current_token.type is TokenTypes.LPAR:
                self.eat(TokenTypes.LPAR)
                subquery = self.select_edge()
                self.eat(TokenTypes.RPAR)
            else:
                subquery = self.select_edge()
        traversal_order = None
        if self.current_token.type is TokenTypes.KW and self.current_token.value == "TRAVERSE":
            self.eat_kw("TRAVERSE")
            self.eat_kw("BY")
            traversal_order = self.eat_kw("DEPTH", "BREADTH")
        cond = None
        if self.current_token.type is TokenTypes.KW and self.current_token.value == "WHERE":
            self.eat_kw("WHERE")
            self.cond = self.expr()
        limit = None
        if self.current_token.type is TokenTypes.KW and self.current_token.value == "LIMIT":
            self.eat_kw("LIMIT")
            self.limit = self.expr()
        tmp = SelectEdge(edge, start, end, subquery, traversal_order)
        if cond:
            tmp = Where(tmp, cond)
        if limit:
            tmp = Limit(tmp, limit)
        return tmp
    def select_node(self):
        self.eat_kw("SELECT")
        name = self.eat(TokenTypes.ID)
        subquery = None
        if self.current_token.type is TokenTypes.KW and self.current_token.value == "FROM":
            self.eat_kw("FROM")
            if self.current_token.type is TokenTypes.LPAR:
                self.eat(TokenTypes.LPAR)
                subquery = self.select_node()
                self.eat(TokenTypes.RPAR)
            else:
                subquery = self.select_node()
        traversal_order = None
        if self.current_token.type is TokenTypes.KW and self.current_token.value == "TRAVERSE":
            self.eat_kw("TRAVERSE")
            self.eat_kw("BY")
            traversal_order = self.eat_kw("DEPTH", "BREADTH")
        cond = None
        if self.current_token.type is TokenTypes.KW and self.current_token.value == "WHERE":
            self.eat_kw("WHERE")
            self.cond = self.expr()
        limit = None
        if self.current_token.type is TokenTypes.KW and self.current_token.value == "LIMIT":
            self.eat_kw("LIMIT")
            self.limit = self.expr()
        tmp = SelectNode(name, subquery, traversal_order)
        if cond:
            tmp = Where(tmp, cond)
        if limit:
            tmp = Limit(tmp, limit)
        return tmp
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
        while self.current_token.type is TokenTypes.OP and self.current_token.value in ("*", "/", "%"):
            op = self.eat(TokenTypes.OP)
            curr = BinOp(op, curr, self.unop())
        return curr
    def unop(self):
        if self.current_token.type is TokenTypes.OP and self.current_token.value in ("-", "+"):
            op = self.eat(TokenTypes.OP)
            return UnOp(op, self.unop())
        return self.literal()
    def literal(self):
        if self.current_token.type is TokenTypes.LPAR:
            self.eat(TokenTypes.LPAR)
            expr = self.expr()
            self.eat(TokenTypes.RPAR)
            return expr
        elif self.current_token.type is TokenTypes.ID:
            var = self.eat(TokenTypes.ID)
            self.eat(TokenTypes.DOT)
            attr = self.eat(TokenTypes.ID)
            return Var(var, attr)
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
        return statements
