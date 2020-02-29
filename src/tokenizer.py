import src.token as tok

class Tokenizer:
    def __init__(self, prop):
        self.proposition = prop
        
        self.parenthesis = 0
        
        # Indice del token actual.
        self.index = -1 
        self.char = ""
        self.peek = self.proposition[self.index + 1]
        self.tokens = list()
        
        self.tokenize()

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
            # Escribiría una clase para simular un switch, pero PEP8 Y bla bla
            if self.char.isspace():
                continue
            t = tok.Token()
            if self.char.isalpha():
                t.start = self.index
                var = self.char
                while self.peek.isalpha():
                    var += self.get_char()
                t.type = tok.VARIABLE
                t.value = var
            
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
                    self.get_char()

            elif self.char == '<' and self.get_char() == '=':
                if self.peek == '>':
                    t.type = tok.OP_BICOND
                self.get_char()
                    
            else:
                t.value += self.char
                t.start = self.index
                while (
                        self.peek and
                        not self.peek.isspace() and 
                        self.peek not in ('(', ')') and
                        not self.peek.isalpha()
                      ):
                    t.value += self.get_char()
                    
            t.end = self.index

            self.tokens.append(t)
        self.tokens.append(tok.Token(tok.EOI))
    
    
    def show_tokens(self):
        for i in self.tokens:
            print(i)
