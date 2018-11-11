from tokens import TokenTypes, Token

###############################################################################
#                                                                             #
#   LEXER                                                                     #
#                                                                             #
###############################################################################

ESCCHARS = {
    "n":  "\n",
    "t":  "\t",
    "\\": "\\",
    "'": "'",
    "r":  "\r",
}

RESERVED_KEYWORDS = {
            "SELECT": lambda x: Token(TokenTypes.SELECT, "SELECT", x),
            "FROM": lambda x: Token(TokenTypes.FROM, "FROM", x),
            "EDGES": lambda x: Token(TokenTypes.EDGES, "EDGES", x),
            "NODES": lambda x: Token(TokenTypes.NODES, "NODES", x),
            "TRAVERSE": lambda x: Token(TokenTypes.TRAVERSE, "TRAVERSE", x),
            "BY": lambda x: Token(TokenTypes.BY, "BY", x),
            "DEPTH": lambda x: Token(TokenTypes.DEPTH, "DEPTH", x),
            "BREADTH": lambda x: Token(TokenTypes.BREADTH, "BREADTH", x),
            "WHERE": lambda x: Token(TokenTypes.WHERE, "WHERE", x),
            "LIMIT": lambda x: Token(TokenTypes.LIMIT, "LIMIT", x),
            "TRUE": lambda x: Token(TokenTypes.TRUE, True, x),
            "FALSE": lambda x: Token(TokenTypes.FALSE, False, x),
            "AND": lambda x: Token(TokenTypes.AND, "AND", x),
            "OR": lambda x: Token(TokenTypes.OR, "OR", x),
            "NOT": lambda x: Token(TokenTypes.NOT, "NOT", x),
}

class Lexer(object):
    def __init__(self, text):
        self.text = text         # string input
        self.pos = 0             # self.pos is index into self.text
        self.line = 1            # current line
        self.current_char = self.text[0] # current char
        self.tokens = []         # tokens so far
    def error(self, msg=""):
        raise Exception("LexingError, line %s: " + msg + "." % self.line)
    def peek(self, lookahead=1):
        peek_pos = self.pos + lookahead
        if peek_pos >= len(self.text):
            return None
        else:
            return self.text[peek_pos]
    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
            if self.current_char == "\n":
                self.line += 1
        else:
            self.current_char = None
    def _eat_white_space(self):
        while self.current_char == " ": self.advance()
    def _add_token1(self, token_type):
        self.tokens.append(Token(token_type, self.current_char, self.line))
        self.advance()
    def _add_token2(self, token_type):
        self.tokens.append(Token(token_type, self.current_char + self.peek(), self.line))
        self.advance()
        self.advance()
    def _id(self):
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self.advance()
        token = RESERVED_KEYWORDS.get(result, lambda x: Token(TokenTypes.ID, result, x))(self.line)
        self.tokens.append(token)
        self._eat_white_space()
    def _str(self):
        result = ""
        while self.current_char is not None and self.current_char != "'":
            if self.current_char == "\\":
                escape_char = ESCCHARS.get(self.peek(), None)
                if escape_char is None:
                    self.error("invalid escape sequence")
                result += escape_char
                self.advance()
                self.advance()
            else:
                result += self.current_char
                self.advance()
        self.advance()
        token = Token(TokenTypes.STR, result, self.line)
        self.tokens.append(token)
        self._eat_white_space()
    def _num(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == ".":
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        token = Token(TokenTypes.NUM, float(result), self.line)
        self.tokens.append(token)
        self._eat_white_space()
    def lex(self):
        # tokenizer
        text = self.text
        while self.pos < len(text):
            while self.current_char in (" ", "\t", "\n"):
                self.advance()
            if self.pos >= len(text):
                self.tokens.append(Token(TokenTypes.EOF, None, self.line))
            elif self.current_char == "-" and self.peek() == "-":   # inline comments
                while self.current_char != "\n" and self.current_char != None:
                    self.advance()
            elif self.current_char == "'":                          # strings
                self.advance()
                self._str()
            elif self.current_char.isdigit() or self.current_char == '.':                       # numbers
                self._num()
            elif self.current_char.isalnum() or self.current_char == "_": self._id()
            elif self.current_char == "(": self._add_token1(TokenTypes.LPAR)
            elif self.current_char == ")": self._add_token1(TokenTypes.RPAR)
            elif self.peek() is not None and self.current_char + self.peek() == ">=":
                self._add_token2(TokenTypes.GTEQ)
            elif self.peek() is not None and self.current_char + self.peek() == "<=":
                self._add_token2(TokenTypes.LTEQ)
            elif self.peek() is not None and self.current_char + self.peek() == "<>":
                self._add_token2(TokenTypes.NE)
            elif self.peek() is not None and self.current_char + self.peek() == "||":
                self._add_token2(TokenTypes.DBAR)
            elif self.current_char == ">": self._add_token1(TokenTypes.GT)
            elif self.current_char == "<": self._add_token1(TokenTypes.LT)
            elif self.current_char == "=": self._add_token1(TokenTypes.EQ)
            elif self.current_char == "+": self._add_token1(TokenTypes.PLUS)
            elif self.current_char == "-": self._add_token1(TokenTypes.MINUS)
            elif self.current_char == "/": self._add_token1(TokenTypes.SLASH)
            elif self.current_char == "*": self._add_token1(TokenTypes.STAR)
            else:
                self.error("unknown sequence.")
        return self.tokens
