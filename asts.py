class AST:
    pass

class SelectNode(AST):
    def __init__(self, args, subquery, traversal_order):
        self.args = args
        self.subquery = subquery
        self.traversal_order = traversal_order

class WhereNode(AST):
    def __init__(self, query, cond):
        self.query = query
        self.cond = cond

class LimitNode(AST):
    def __init__(self, query, limit):
        self.query = query
        self.limit = limit

class BinOp(AST):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class UnOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class String(AST):
    # STR
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Boolean(AST):
    # BOOL
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Number(AST):
    # NUM
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var(AST):
    # ID
    def __init__(self, token):
        self.token = token
        self.value = token.value

