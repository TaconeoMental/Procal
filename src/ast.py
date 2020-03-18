import src.token as tok


class Ast(object):
    def infix_str(self):
        pass
    def to_infix(self, current_l, level):
        pass
    def eval(self, env):
        pass


class BinOp(Ast):
    def __init__(self, left, right, op):
        
        self.left = left
        self.right = right
        self.op = op
        
    def infix_str(self) -> str:
        return f"{self.left.infix_str()} {tok.token_op(self.op)} {self.right.infix_str()}"
        
    def to_infix(self, current_l, level):
        current_l += 1
        if current_l == level:
            return [self]
        infix_l = [self] 
        if not isinstance(self.left, Variable):
            if isinstance(self.left, UnaryOp):
                infix_l += self.left.to_infix(current_l, level)
            else:
                infix_l += [self.left.to_infix(current_l, level)]
        if not isinstance(self.right, Variable):
            if isinstance(self.right, UnaryOp):
                infix_l += self.right.to_infix(current_l, level)
            else:
                infix_l += [self.right.to_infix(current_l, level)]
        return infix_l
       
    def eval(self, env):
        return tok.eval_bin(self.op, self.left.eval(env), self.right.eval(env))

    def __repr__(self):
        return f"{tok.token_name(self.op)}({self.left}, {self.right})"


class UnaryOp(Ast):
    def __init__(self, expr, op):
        
        self.expr = expr
        self.op = op
        
    def infix_str(self):
        if isinstance(self.expr, Variable):
            return f"¬{self.expr.infix_str()}"
        return f"¬({self.expr.infix_str()})"
        
    def to_infix(self, current_l, level):
        current_l += 1
        infix_l = [self]
        if current_l == level:
            return infix_l
        if isinstance(self.expr, BinOp):
            infix_l += self.expr.to_infix(current_l, level)
        elif isinstance(self.expr, Variable):
            pass
        else:
            infix_l += [self.expr]
        return infix_l
        
    def eval(self, env):
        return not self.expr.eval(env)

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
        
    def eval(self, env):
        return env[self.value]

    def __repr__(self):
        return f"VAR({self.value})"


class Proposition(Ast):
    def __init__(self, expr):
        self.expr = expr
        
    def infix_str(self):
        return self.expr.infix_str()
        
    def infix_list_until(self, level):
        infix_l = self.expr.to_infix(0, level)
        return infix_l[::-1]

    def __repr__(self):
        return f"PROP({self.expr})"
