from enum import Enum

def auto():
    num = 0
    while True:
        yield num
        num += 1

class TokenTypes(Enum):
    # keywords
    SELECT   = auto()
    FROM     = auto()
    EDGES    = auto()
    NODES    = auto()
    TRAVERSING = auto()
    BY       = auto()
    DEPTH    = auto()
    TOPOLOGICAL = auto()
    WHERE    = auto()
    LIMIT    = auto()
    
    # booleans
    TRUE     = auto()
    FALSE    = auto()

    # parentheses
    LPAR     = auto()
    RPAR     = auto()

    # logical operators
    NOT  = auto()
    
    # other operators
    GT    = auto()  # >
    LT    = auto()  # <
    GTEQ  = auto()  # >=
    LTEQ  = auto()  # <=
    EQ    = auto()  # = 
    LTGT  = auto()  # <>
    PLUS  = auto()  # +
    MINUS = auto()  # -
    STAR  = auto()  # *
    SLASH = auto()  # /
    DBAR  = auto()  # ||
 
    # types and identifiers
    NUM    = auto()
    STR    = auto()
    ID     = auto()
    
    # end of line / end of file
    EOL    = auto()
    EOF    = auto()

class Token(object):
    def __init__(self, token_type: TokenTypes, token_value: any, line: int):
        self.type = token_type
        self.value = token_value
        self.line = line
    def __str__(self) -> str:
        return "Token(%s, %s)" % (self.type, repr(self.value))
    __repr__ = __str__
