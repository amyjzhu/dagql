class AST:
    pass

class SelectEdge(AST):
    def __init__(self, exprs, edge, start, end, subquery, traversal_order):
        self.exprs = exprs
        self.edge = edge
        self.start = start
        self.end = end
        self.subquery = subquery
        self.traversal_order = traversal_order

class SelectNode(AST):
    def __init__(self, exprs, node, subquery, traversal_order):
        self.exprs = exprs
        self.node = node
        self.subquery = subquery
        self.traversal_order = traversal_order

class SearchEdge(AST):
    def __init__(self, subquery, edge, start, end, where, limit):
        self.subquery = subquery
        self.edge = edge
        self.start = start
        self.end = end
        self.where = where
        self.limit = limit

class SearchNode(AST):
    def __init__(self, subquery, node, where, limit):
        self.subquery = subquery
        self.node = node
        self.where = where
        self.limit = limit

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
    def __init__(self, var, attr):
        self.var = var
        self.attr = attr

class Edges(AST):
    def __init__(self):
        pass

class Nodes(AST):
    def __init__(self):
        pass


