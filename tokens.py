from enum import Enum

def auto():
    num = 0
    while True:
        yield num
        num += 1

class TokenTypes(Enum):
    MATCH    = auto()
    WHERE    = auto()
    OPTIONAL = auto()
    WITH     = auto()
    RETURN   = auto()
    ORDER    = auto()
    BY       = auto()
    CREATE   = auto()
    DELETE   = auto()
    SET      = auto()
    REMOVE   = auto()
    MERGE    = auto()
    
    LPAR     = auto()
    RPAR     = auto()
    LBRC     = auto()
    RBRC     = auto()
    LSQB     = auto()
    RSQB     = auto()

    COLON    = auto()
    RARR     = auto()
    DASH     = auto()
    DOT      = auto()
    COMMA    = auto()
 
    STR    = auto()
    ID     = auto()
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
