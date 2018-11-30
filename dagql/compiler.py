import os

from .visitor import *
from .environment import Env
from .ast import *
from dagql.backend import Backend, Node, TraversalOrder
from dagql.backends.camflow import CamFlowBackend

BINOPS = {
        '*': (lambda x, y: x * y),
        '/': (lambda x, y: x / y),
        '%': (lambda x, y: x % y),
        '+': (lambda x, y: x + y),
        '-': (lambda x, y: x - y),
        'AND': (lambda x, y: x and y),
        'OR': (lambda x, y: x or y),
        '||': (lambda x, y: str(x) + str(y)),
        '=': (lambda x, y: x == y),
        '<>': (lambda x, y: x != y),
        '>': (lambda x, y: x > y),
        '<': (lambda x, y: x < y),
        '>=': (lambda x, y: x >= y),
        '<=': (lambda x, y: x <= y),
        }
UNOPS = {
        '+': (lambda x: +x),
        '-': (lambda x: -x)
        }

###############################################################################
#                                                                             #
#  COMPILER                                                                   #
#                                                                             #
###############################################################################

class Compiler(NodeVisitor):
    def __init__(self):
        BASIC_MSGBUF = os.path.join(os.path.dirname(__file__), "..", "test", "inputs", "basic.txt")
        self.graph = CamFlowBackend(open(BASIC_MSGBUF, 'rb'))
    def compile(self, statements):
        for statement in statements:
            self.visit(statement, {})
    def visit_SelectEdge(self, node, env):
        subquery = self.visit(node.subquery, {})
        local = {
            'edge': node.edge,
            'start': node.start,
            'end': node.end
        }
        for s in subquery(node.traversal_order):
            edge, start, end = s
            local['$edge'] = edge
            local['$start'] = start
            local['$end'] = end
            for expr in node.exprs:
                result = self.visit(expr, local)
                print(result, end=' ')
            print('')
    def visit_SelectNode(self, node, env):
        subquery = self.visit(node.subquery, {})
        local = {
            'node': node.node
        }
        for s in subquery(node.traversal_order):
            local['$node'] = s
            for expr in node.exprs:
                result = self.visit(expr, local)
                print(result, end=' ')
            print('')
    def visit_SearchEdge(self, node, env):
        subquery = self.visit(node.subquery, {})
        if node.where and node.limit:
            def f(order):
                local = {
                    'edge': node.edge,
                    'start': node.start,
                    'end': node.end
                }
                limit = self.visit(node.limit, {})
                for s in subquery(order):
                    if limit <= 0: break
                    local['$edge'] = edge
                    local['$start'] = start
                    local['$end'] = end
                    if self.visit(node.where, local):
                        limit -= 1
                        yield s
            return f
        if node.where:
            def f(order):
                local = {
                    'edge': node.edge,
                    'start': node.start,
                    'end': node.end
                }
                for s in subquery(order):
                    local['$edge'] = edge
                    local['$start'] = start
                    local['$end'] = end
                    if self.visit(node.where, local):
                        yield s
            return f
        if node.limit:
            def f(order):
                limit = self.visit(node.limit, {})
                for s in subquery(order):
                    if limit <= 0: break
                    limit -= 1
                    yield s
            return f
        return subquery
    def visit_SearchNode(self, node, env):
        subquery = self.visit(node.subquery, {})
        if node.where and node.limit:
            def f(order):
                local = {
                    'node': node.node
                }
                limit = self.visit(node.limit, {})
                for s in subquery(order):
                    if limit <= 0: break
                    local['$node'] = s
                    if self.visit(node.where, local):
                        limit -= 1
                        yield s
            return f
        if node.where:
            def f(order):
                local = {
                    'node': node.node
                }
                for s in subquery(order):
                    local['$node'] = s
                    if self.visit(node.where, local):
                        yield s
            return f
        if node.limit:
            def f(order):
                limit = self.visit(node.limit, {})
                for s in subquery(order):
                    if limit <= 0: break
                    limit -= 1
                    yield s
            return f
        return subquery
    def visit_Nodes(self, node, env):
        return self.graph.walk_nodes
    def visit_Edges(self, node, env):
        return self.graph.walk_edges
    def visit_BinOp(self, node, env):
        left = self.visit(node.left, env)
        if (node.op.value == "AND" or node.op.value == "OR") and type(left) is not bool:
            raise Exception("Boolean expected")
        elif node.op.value == "AND" and left == False:
            return False
        elif node.op.value == "OR" and left == True:
            return True
        right = self.visit(node.right, env)
        if node.op.value in ('AND', 'OR') and type(right) is not bool:
            raise Exception("Boolean expected")
        elif node.op.value in ('*', '/', '+', '-') and (type(left) is not float or type(left) is not float):
            raise Exception("Number expected")
        op = BINOPS.get(node.op.value)
        assert(op)
        return op(left, right)
    def visit_UnOp(self, node, env):
        expr = self.visit(node.expr)
        if type(expr) is not float:
            raise Exception("Number expected")
        op = UNOPS.get(node.op)
        assert(op)
        return op(expr)
    def visit_Var(self, node, env):
        if '$node' in env:
            if env['node'].value == node.var.value:
                return env['$node'][node.attr.value]
        else:
            if env['start'].value == node.var.value:
                return env['$start'][node.attr.value]
            elif env['end'].value == node.var.value:
                return env['$end'][node.attr.value]
            elif env['edge'].value == node.var.value:
                return env['$edge'][node.attr.value]
        raise Exception("invalid id")
    def visit_String(self, node, env):
        assert(type(node.value) is str)
        return node.value
    def visit_Boolean(self, node, env):
        assert(type(node.value) is bool)
        return node.value
    def visit_Number(self, node, env):
        assert(type(node.value) is float)
        return node.value
