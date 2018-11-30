class NodeVisitor:
    def visit(self, node, env):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, env)
    def generic_visit(self, node, env):
        raise Exception("No visit_%s method: %s" % (type(node).__name__, node))
