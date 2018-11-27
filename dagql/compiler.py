import os

from .visitor import *
from .environment import Env
from .ast import *
from dagql.backend import Backend, Node, TraversalOrder
from dagql.backends.camflow import CamFlowBackend

BINOPS = {
        '*': (lambda x, y: x * y),
        '/': (lambda x, y: x / y),
        '+': (lambda x, y: x + y),
        '-': (lambda x, y: x - y),
        'AND': (lambda x, y: x and y),
        'OR': (lambda x, y: x or y),
        '||': (lambda x, y: x + y)
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
        self.globals = Env()
        self.locals = Env()
        BASIC_MSGBUF = os.path.join(os.path.dirname(__file__), "..", "test", "inputs", "basic.txt")
        self.graph = CamFlowBackend(open(BASIC_MSGBUF, 'rb'))
    def compile(self, statements):
        for _ in self.graph.walk_nodes(TraversalOrder.DFS):
            print(_)
        for statement in statements:
            print(statement)
            self.visit(statement)
        
    def enter_scope(self):
        if self.current_fn is not None:
            self.locals = Env(self.locals)
        else:
            self.globals = Env(self.globals)
    def exit_scope(self):
        if self.current_fn is not None:
            self.locals = self.locals.parent
        else:
            self.globals = self.globals.parent
    def visit_Select(self, node):
        raise NotImplementedError
    def visit_Where(self, node):
        raise NotImplementedError
    def visit_Limit(self, node):
        raise NotImplementedError
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        if (node.op == "AND" or node.op == "OR") and type(left) is not bool:
            raise Exception("Boolean expected")
        elif node.op == "AND" and left == False:
            return False
        elif node.op == "OR" and left == True:
            return True
        right = self.visit(node.right)
        if node.op in ('AND', 'OR') and type(right) is not bool:
            raise Exception("Boolean expected")
        elif node.op in ('*', '/', '+', '-') and (type(left) is not float or type(left) is not float):
            raise Exception("Number expected")
        elif node.op == '||' and (type(left) is not str or type(right) is not str):
            raise Exception("String expected")
        op = BINOPS.get(node.op)
        assert(op)
        return op(left, right)
    def visit_UnOp(self, node):
        expr = self.visit(node.expr)
        if type(expr) is not float:
            raise Exception("Number expected")
        op = UNOPS.get(node.op)
        assert(op)
        return op(expr)
    def visit_Var(self, node):
        raise NotImplementedError
    def visit_String(self, node):
        assert(type(node.value) is str)
        return node.value
    def visit_Boolean(self, node):
        assert(type(node.value) is bool)
        return node.value
    def visit_Number(self, node):
        assert(type(node.value) is float)
        return node.value
