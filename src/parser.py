import src.token as tok
import src.ast as ast

class ReadableObject:
    def __init__(self, string):
        if string == "":
            string = " "
        self.string = iter(string)

    def read(self):
        try:
            return next(self.string)
        except StopIteration:
            return ''

class Parser:
    # TODO: Arreglar esta CFG para que sea asociativa por la derecha, no la izquierda. Esto es relevante más que nada
    # para la implicación material, que por definición asocia por la derecha. a -> b -> c = a -> (b -> c). También, ya
    # que este es un LR, no puede manejar left recursion.
    """
    prop = bicond_expr;
    bicond_expr = impl_expr, {"<->", impl_expr};
    impl_expr = disj_expr, {"->", disj_expr};
    disj_expr = conj_expr, {"|", conj_expr};
    conj_expr = neg_expr, {"&", neg_expr};
    neg_expr = "¬", neg_expr
             | prop_primaria;
    prop_primaria = variable
                  | "(", prop, ")";
                  | epsilon
    variable = [a-zA-Z];
    """

    def __init__(self, tokens):
        self.tokens = ReadableObject(tokens)
        self.current_token = self.tokens.read()

    def _bin_op(self, token_type, function):
        node = function()
        while self.current_token.type == token_type:
            token = self.current_token
            self.consume(token_type)
            node = ast.BinOp(node, function(), token_type)
        return node

    def consume(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.tokens.read()
        else:
            # Reemplazar con un recolector de errores
            raise Exception(f"{self.current_token.end} | Expected {tok.token_name(token_type)} Got: {tok.token_name(self.current_token.type)}")

    def parse(self):
        node = ast.Proposition(self.prop())
        return node

    def prop(self):
        return self.bicond_expr()

    def bicond_expr(self):
        return self._bin_op(tok.OP_BICOND, self.impl_expr)

    def impl_expr(self):
        return self._bin_op(tok.OP_IMPL, self.disj_expr)

    def disj_expr(self):
        return self._bin_op(tok.OP_DISJ, self.conj_expr)

    def conj_expr(self):
        return self._bin_op(tok.OP_CONJ, self.neg_expr)

    def neg_expr(self):
        token = self.current_token
        node = None
        if token.type == tok.OP_NEG:
            self.consume(tok.OP_NEG)
            return ast.UnaryOp(self.neg_expr(), tok.OP_NEG)
        else:
            node = self.prop_primaria()
            return node

    def prop_primaria(self):
        token = self.current_token
        if token.type == tok.VARIABLE:
            node = ast.Variable(token)
            self.consume(tok.VARIABLE)
        elif token.type == tok.L_PAR:
            self.consume(tok.L_PAR)
            node = self.prop()
            self.consume(tok.R_PAR)
        else:
            if token.type == tok.UNKNOWN:
                self.consume(tok.UNKNOWN)
            node = ast.NoOp()
        return node
