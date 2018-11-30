class Env(object):
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent
    def __len__(self):
        if self.parent is None:
            return len(self.vars)
        else:
            return len(self.vars) + len(self.parent)
    def __contains__(self, var: str):
        return var in self.vars
    def __getitem__(self, var: str):
        return self.vars[var]
    def __setitem__(self, key, value):
        self.vars[key] = value
    def decl_var(self, var: str):
        self.vars[var] = len(self)
