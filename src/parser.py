import src.token as tok
import src.ast as ast
from src.error_collector import Error


class ReadableObject:
    def __init__(self, string):
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
    PROP          -> BICOND_EXPR
    BICOND_EXPR   -> IMPL_EXPR ["<->" IMPL_EXPR]
    IMPL_EXPR     -> DISJ_EXPR ["->" DISJ_EXPR]
    DISJ_EXPR     -> CONJ_EXPR ["|" CONJ_EXPR]
    CONJ_EXPR     -> NEG_EXPR ["&" NEG_EXPR]
    NEG_EXPR      -> "~" NEG_EXPR
                   | PROP_PRIMARIA
    PROP_PRIMARIA -> VARIABLE
                   | "(" [PROP] ")"
    """


    def __init__(self, tokenizer, err_coll):
        self.tokens = ReadableObject(tokenizer.tokenize())
        self.current_token = self.tokens.read()
        self.err_coll = err_coll

    def _bin_op(self, token_type, function):
        node = function()
        while self.current_token.type == token_type:
            self.consume(token_type)
            node = ast.BinOp(node, function(), token_type)
        return node

    def consume(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.tokens.read()

        # TODO: Evitar que se añada el mismo error varias veces en proposiciones como
        # "((((((" y reemplazarlo por un mensaje de error de parentesis no balanceados
        elif self.current_token.type == tok.EOI:
            self.err_coll.add_error(
                Error(self.current_token, f"Unexpected EOI"))
        else:
            self.err_coll.add_error(Error(
                self.current_token, f"Expected {tok.token_name(token_type)} Got: {tok.token_name(self.current_token.type)}"))

    def parse(self):
        node = ast.Proposition(self.prop())
        return node

    def prop(self):
        return self.bicond_expr()

    def bicond_expr(self):
        return self._bin_op(tok.OP_BICOND, self.impl_expr)

    def impl_expr(self):
        node = self.disj_expr()
        while self.current_token.type == tok.OP_IMPL:
            self.consume(tok.OP_IMPL)
            # Solución floja, pero funciona. Debería modificar la CFG.
            node = ast.BinOp(self.disj_expr(), node, tok.OP_IMPL)
        return node

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
            self.consume(tok.VARIABLE)
            node = ast.Variable(token)
        elif token.type == tok.L_PAR:
            self.consume(tok.L_PAR)
            node = self.prop()
            self.consume(tok.R_PAR)
        else:
            if token.type == tok.UNKNOWN:
                self.consume(tok.UNKNOWN)
                node = self.prop_primaria()
            node = ast.NoOp()
        return node
