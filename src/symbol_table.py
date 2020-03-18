# ¿Y si lo implemento como un diccionario nomás? :(
class Symbol:
    def __init__(self, tok):
        self.value = None
        self.symbol = tok.value
        
    def __str__(self):
        return f"Sym({self.symbol} = {self.value})"
        
    def __repr__(self):
        return f"Sym({self.symbol})"

# No es una symbol table en teoría, pero suena bacán y no
# se me ocurre otro nombre
class SymbolTable:
    def __init__(self):
        self.symbols = dict()
        self.number_sym = 0
        
    def add_symbol(self, sym):
        if sym.symbol in self.symbols:
            return
        self.symbols[sym.symbol] = sym.value
        self.number_sym += 1
    
    def show_symbols(self):
        for s in self.symbols:
            print(s)