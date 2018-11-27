class AST:
    pass

class SelectEdge(AST):
    def __init__(self, edge, start, end, subquery, traversal_order):
        self.edge = edge
        self.start = start
        self.end = end
        self.subquery = subquery
        self.traversal_order = traversal_order

class SelectNode(AST):
    def __init__(self, node, subquery, traversal_order):
        self.node = node
        self.subquery = subquery
        self.traversal_order = traversal_order

class Where(AST):
    def __init__(self, query, cond):
        self.query = query
        self.cond = cond

class Limit(AST):
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

