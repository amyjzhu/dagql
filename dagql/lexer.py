from .tokens import TokenTypes, Token

ESCCHARS = {
    "n":  "\n",
    "t":  "\t",
    "\\": "\\",
    "'": "'",
    "r":  "\r",
}

RESERVED_WORDS = {
    "SELECT",
    "FROM",
    "TRAVERSE",
    "BY",
    "DEPTH",
    "BREADTH",
    "WHERE",
    "LIMIT",
}

class LexingError(Exception):
    pass

class Lexer:
    def __init__(self, text):
        self.text = text         # string input
        self.pos = 0             # self.pos is index into self.text
        self.line = 1            # current line
        self.current_char = self.text[0] # current char
        self.tokens = []         # tokens so far
    def _error(self, msg):
        raise LexingError("Error in line " + str(self.line) + ": " + msg)
    def _peek(self, lookahead=1):
        _peek_pos = self.pos + lookahead
        if _peek_pos >= len(self.text):
            return None
        else:
            return self.text[_peek_pos]
    def _advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
            if self.current_char == "\n":
                self.line += 1
        else:
            self.current_char = None
    def _eat_white_space(self):
        while self.current_char == " ": self._advance()
    def _add_token_1_char(self, token_type):
        self.tokens.append(Token(token_type, self.current_char, self.line))
        self._advance()
    def _add_token_2_char(self, token_type):
        self.tokens.append(Token(token_type, self.current_char + self._peek(), self.line))
        self._advance()
        self._advance()
    def _id(self):
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self._advance()
        if result == "TRUE": token = Token(TokenTypes.BOOL, True, self.line)
        elif result == "FALSE": token = Token(TokenTypes.BOOL, False, self.line)
        elif result in ("AND", "OR", "NOT"): token = Token(TokenTypes.OP, result, self.line)
        else: token = Token(TokenTypes.KW if result in RESERVED_WORDS else TokenTypes.ID, result, self.line)
        self.tokens.append(token)
        self._eat_white_space()
    def _str(self):
        result = ""
        while self.current_char is not None and self.current_char != "'":
            if self.current_char == "\\":
                escape_char = ESCCHARS.get(self._peek(), None)
                if escape_char is None:
                    self._error("invalid escape sequence")
                result += escape_char
                self._advance()
                self._advance()
            else:
                result += self.current_char
                self._advance()
        self._advance()
        token = Token(TokenTypes.STR, result, self.line)
        self.tokens.append(token)
        self._eat_white_space()
    def _num(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self._advance()
        if self.current_char == ".":
            result += self.current_char
            self._advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self._advance()
        token = Token(TokenTypes.NUM, float(result), self.line)
        self.tokens.append(token)
        self._eat_white_space()
    def lex(self):
        # tokenizer
        text = self.text
        while self.pos < len(text):
            while self.current_char in (" ", "\t", "\n"):
                self._advance()
            if self.pos >= len(text):
                self.tokens.append(Token(TokenTypes.EOF, None, self.line))
            elif self.current_char == "-" and self._peek() == "-": # inline comments
                while self.current_char != "\n" and self.current_char != None:
                    self._advance()
            elif self.current_char == "'": # strings
                self._advance()
                self._str()
            elif self.current_char.isdigit() or self.current_char == '.': # numbers
                self._num()
            elif self.current_char.isalnum() or self.current_char == "_": self._id()
            elif self.current_char == "(": self._add_token_1_char(TokenTypes.LPAR)
            elif self.current_char == ")": self._add_token_1_char(TokenTypes.RPAR)
            elif self.current_char == ",": self._add_token_1_char(TokenTypes.COMMA)
            elif self._peek() is not None and self.current_char + self._peek() in (">=", "<=", "<>", "||"): self._add_token_2_char(TokenTypes.OP)
            elif self.current_char == '.' and self._peek() and not self._peek().isnum():
                self._add_token_1_char(TokenTypes.DOT)
            elif self.current_char in (">", "<", "=", "+", "-", "/", "*"): self._add_token_1_char(TokenTypes.OP)
            else: self._error("unknown sequence")
        return self.tokens
