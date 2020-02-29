import src.token as tok

class Ast(object):
    pass

class BinOp(Ast):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op
        
    def __repr__(self):
        return f"{tok.token_name(self.op)}({self.left}, {self.right})"

class UnaryOp(Ast):
    def __init__(self, expr, op):
        self.expr = expr
        self.op = op
    def __repr__(self):
        return f"NEG({self.expr})"

class NoOp(Ast):
    def __init__(self):
        pass
    def __repr__(self):
        return f"NOP()"


class Variable(Ast):
    def __init__(self, token):
        self.token = token
        self.value = token.value
    def __repr__(self):
        return f"VAR({self.value})"

class Proposition(Ast):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"PROP({self.expr})"
