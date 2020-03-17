import src.token as tok
from src.error_collector import Error
from src.symbol_table import Symbol

# TODO: implementar usando ReadableObject


class Tokenizer:
    def __init__(self, err_coll, sym_t):
        self.proposition = err_coll.proposition
        self.err_coll = err_coll
        self.sym_t = sym_t

        self.parenthesis = 0

        # Indice del token actual.
        self.index = -1
        self.char = ""
        self.peek = self.proposition[self.index + 1]
        self.tokens = list()

    def get_char(self):
        self.index += 1
        self.char = self.peek

        # Un poco penca, pero ñee funciona
        try:
            self.peek = self.proposition[self.index + 1]
        except IndexError:
            self.peek = ""

        return self.char

    def tokenize(self):
        while self.get_char():
            end = self.index
            # Escribiría una clase para simular un switch, pero PEP8 Y bla bla
            if self.char.isspace():
                continue
            t = tok.Token(start=self.index)
            if self.char.isalpha():
                var = self.char
                while self.peek.isalpha():
                    var += self.get_char()
                    end += 1
                t.type = tok.VARIABLE
                t.value = var
                t.end = end
                self.sym_t.add_symbol(Symbol(t))

            elif self.char == '(':
                t.type = tok.L_PAR
                self.parenthesis += 1
            elif self.char == ')':
                t.type = tok.R_PAR
                self.parenthesis -= 1

            elif self.char == '&':
                t.type = tok.OP_CONJ

            elif self.char == '|':
                t.type = tok.OP_DISJ

            elif self.char == '~':
                t.type = tok.OP_NEG

            elif self.char == '-':
                if self.peek == '>':
                    t.type = tok.OP_IMPL
                    end = self.index + 1
                    self.get_char()

            elif self.char == '<' and self.get_char() == '=':
                if self.peek == '>':
                    t.type = tok.OP_BICOND
                self.get_char()
                end += 2

            else:
                t.value += self.char
                while (
                    self.peek and
                    not self.peek.isspace() and
                    self.peek not in ('(', ')') and
                    not self.peek.isalpha()
                ):
                    t.value += self.get_char()
                end = self.index

            t.end = end

            if t.type == tok.UNKNOWN:
                self.err_coll.add_error(
                    Error(t, f"Operator '{self.proposition[t.start : t.end + 1]}' not recognized"))

            self.tokens.append(t)
        self.tokens.append(
            tok.Token(tok.EOI, start=self.index, end=self.index))
        return self.tokens

    def show_tokens(self):
        for i in self.tokens:
            print(i)
