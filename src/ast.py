import src.token as tok


class Ast(object):      
    def to_infix(self, current_l, level) -> list:
        pass


class BinOp(Ast):
    def __init__(self, left, right, op):
        
        self.left = left
        self.right = right
        self.op = op
        
    def infix_str(self) -> str:
        return f"{self.left.infix_str()} {token_op(self.op)} {self.right.infix_str()}"
        
    def to_infix(self, current_l, level):
        current_l += 1
        if current_l == level:
            return [self.infix_str()]
        infix_l = [self.infix_str()] 
        if not isinstance(self.left, Variable):
            infix_l += self.left.to_infix(current_l, level)
        if not isinstance(self.right, Variable):
            infix_l += self.right.to_infix(current_l, level)
        return infix_l

    def __repr__(self):
        return f"{tok.token_name(self.op)}({self.left}, {self.right})"


class UnaryOp(Ast):
    def __init__(self, expr, op):
        
        self.expr = expr
        self.op = op
        
    def infix_str(self):
        return f"¬{self.expr.infix_str()}"
        
    def to_infix(self, current_l, level):

        return f"~{self.expr.to_infix(current_l, level)}"

    def __repr__(self):
        return f"NEG({self.expr})"


class NoOp(Ast):
    def __init__(self):
        pass
        
    def to_infix(self):
        return " "

    def __repr__(self):
        return f"NOP()"


class Variable(Ast):
    def __init__(self, token):
        
        self.token = token
        self.value = token.value
    
    def infix_str(self):
        return self.value
        
    def to_infix(self, current_l, level):
        return self.infix_str()

    def __repr__(self):
        return f"VAR({self.value})"


class Proposition(Ast):
    def __init__(self, expr):
        self.expr = expr
        
    def infix_str(self):
        return self.expr.infix_str()
        
    def infix_list_until(self, level):
        
        infix_list = list()
        infix_list += self.expr.to_infix(0, level)
        return infix_list[::-1]

    def __repr__(self):
        return f"PROP({self.expr})"
        
def token_op(t: int) -> str:
    token_str = ['↔', '→', '∨', '∧']
    return token_str[t - 2]
