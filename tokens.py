from enum import Enum

def auto():
    num = 0
    while True:
        yield num
        num += 1

class TokenTypes(Enum):
    # keywords
    KW   = auto() # SELECT, FROM, EDGES, NODES, TRAVERSE, BY, DEPTH, BREADTH, WHERE, LIMIT
    
    # parentheses
    LPAR = auto()
    RPAR = auto()

    # operators
    OP   = auto() # AND, OR, NOT, >, <, >=, <=, =, <>, +, -, /, *, ||
    
    # types and identifiers
    BOOL = auto()
    NUM  = auto()
    STR  = auto()
    ID   = auto()
    
    # end of line / end of file
    EOL  = auto()
    EOF  = auto()

class Token(object):
    def __init__(self, token_type: TokenTypes, token_value: any, line: int):
        self.type = token_type
        self.value = token_value
        self.line = line
    def __eq__(self, other):
        return self.type == other.type and self.value == other.value and self.line == other.line
    def __str__(self) -> str:
        return "Token(%s, %s)" % (self.type, repr(self.value))
    __repr__ = __str__
