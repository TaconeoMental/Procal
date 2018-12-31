import sys
from collections import namedtuple
import json

VARIABLE, OP_BICOND, OP_IMPL, OP_DISJ, OP_CONJ, OP_NEG, L_PAR, R_PAR, EOI = range(9)
token_name = ['Variable', '<->', '->', '|', '&', '~', 'L_PAR', 'R_PAR', 'EOI']
Token = namedtuple('Token', ['tipo', 'valor'])

# Delimitadores
delim = {'(': L_PAR, ')': R_PAR}

# Operadores de un caracter
ops = {'|': OP_DISJ, '&': OP_CONJ, '¬': OP_NEG}


class ReadableObject:
    def __init__(self, string):
        self.string = iter(string)

    def read(self):
      try:
        return next(self.string)
      except StopIteration:
        return ''

class Lexer:
    def __init__(self, string):
        self.s = ReadableObject(string)
        self.char = None
        self.peek = None
        self.tokens = []

    def error(self):
        print('[-] ERROR: Caracter "{}" desconocido.'.format(self.char))
        sys.exit(1)

    def read_char(self):
        if self.char is None:
            self.char = self.s.read()
        else:
            self.char = self.peek
        self.peek = self.s.read()
        if self.char.isspace():
            self.read_char()
        return self.char

    def add_token(self, tipo, valor=None):
        self.tokens.append(Token(tipo, valor))

    def lex(self):
        while self.read_char() != '':
            c = self.char
            if c.isspace():
                continue
            elif c.isalpha():
                # Acá debería implementar alguna especie de tabla de valores.
                self.add_token(VARIABLE, c)
            elif c in delim:
                self.add_token(delim[c])
            elif c in ops:
                self.add_token(ops[c])
            elif c == '-':
                if self.peek == '>':
                    self.read_char()
                    self.add_token(OP_IMPL)
                else:
                    self.error()
            elif c == '<':
                self.read_char()
                if self.char == '-' and self.peek == '>':
                    self.read_char()
                    self.add_token(OP_BICOND)
                else:
                    self.error()
            else:
                self.error()
        self.add_token(EOI)
        return self.tokens


class Node:
    def to_dict(self):
        pass


class AstRoot(Node):
    def __init__(self, seq):
        self.seq = seq

    def to_dict(self):
        return {"AST": self.seq.to_dict()}

    def __str__(self):
        return str(self.seq)

# Probablemente necesite implementar el atributo "valor" en el futuro o, mejor aún, hacer una tabla de valores.
class Variable(Node):
    def __init__(self, id):
        self.id = id

    def to_dict(self):
        return {"ID": self.id}

    def __repr__(self):
        return self.id.upper()


class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def to_dict(self):
        return {token_name[self.op.tipo]:{"left": self.left.to_dict(), "right": self.right.to_dict()}}

    def __str__(self):
        return "({} {} {})".format(self.left, token_name[self.op.tipo], self.right)


# Only unary operation
class NegationOp(Node):
    def __init__(self, op, child):
        self.op = op
        self.child = child

    def to_dict(self):
        return {token_name[self.op.tipo]: self.child.to_dict()}

    def __repr__(self):
        return "{}{}".format(token_name[self.op.tipo], self.child)


class Parser:
    # TODO: Arreglar esta CFG para que sea asociativa por la derecha, no la izquierda. Esto es relevante más que nada
    # para la implicación material, que por definición asocia por la derecha. a -> b -> c = a -> (b -> c).
    """
    prop          = bicond_expr;
    bicond_expr   = impl_expr, {"<->", impl_expr};
    impl_expr     = disj_expr, {"->", disj_expr};
    disj_expr     = conj_expr, {"|", conj_expr};
    conj_expr     = neg_expr, {"&", neg_expr};
    neg_expr      = "¬", neg_expr
                  | prop_primaria;
    prop_primaria = variable
                  | "(", prop, ")";
    variable      = [a-zA-Z];
    """
    def __init__(self, tokens):
        self.tokens = ReadableObject(tokens)
        self.prev = None
        self.curr = None
        self.peek = self.tokens.read()

    def error(self):
        print('[-] ERROR: Error de syntax.')
        sys.exit()

    def es_final(self):
        return self.peek.tipo == EOI

    def read_token(self):
        if not self.es_final():
            self.prev = self.curr
            self.curr = self.peek
            self.peek = self.tokens.read()
        return self.curr

    def check(self, token_type):
        """ compara self.peek.tipo con token_type """
        if self.es_final():
            return False
        return self.peek.tipo == token_type

    def match(self, tokens):
        """ Compara self.peek con tokens y llama a self.read_token()
        si calza alguno
        """
        for token in tokens:
            if self.check(token):
                self.read_token()
                return True
        return False

    def prop(self):
        """
        prop = bicond_expr;
        """
        return self.bicond_expr()

    def bicond_expr(self):
        """
        bicond_expr   = impl_expr, {"<->", impl_expr};
        """
        node = self.impl_expr()
        while self.read_token().tipo in [OP_BICOND]:
            # print('OP: {}, CURR: {}'.format(token_name[self.prev.tipo], token_name[self.curr.tipo]))
            op = self.curr
            right = self.impl_expr()
            node = BinOp(op, node, right)
        return node

    def impl_expr(self):
        """
        impl_expr     = disj_expr, {"->", disj_expr};
        """
        node = self.disj_expr()
        while self.match((OP_IMPL,)):
            op = self.curr
            right = self.disj_expr()
            node = BinOp(op, node, right)
        return node

    def disj_expr(self):
        """
        disj_expr = conj_expr, {"|", conj_expr};
        """
        node = self.conj_expr()
        while self.match((OP_DISJ,)):
            op = self.curr
            right = self.conj_expr()
            node = BinOp(op, node, right)
        return node

    def conj_expr(self):
        """
        conj_expr = neg_expr, {"&", neg_expr};
        """
        node = self.neg_expr()
        while self.match((OP_CONJ,)):
            op = self.curr
            right = self.neg_expr()
            node = BinOp(op, node, right)
        return node

    def neg_expr(self):
        """
        neg_expr = "¬", neg_expr | prop_primaria;
        """
        if self.peek.tipo == OP_NEG:
            op = self.read_token()
            child = self.neg_expr()
            return NegationOp(op, child)
        return self.prop_primaria()

    def prop_primaria(self):
        """
        prop_primaria = variable | "(", prop, ")";
        """
        if self.match((VARIABLE,)):
            return Variable(self.curr.valor)
        elif self.match((L_PAR,)):
            expr = self.prop()
            if self.curr.tipo != R_PAR:
                self.error()
            return expr
        else:
            self.error()

    def parse(self):
        return AstRoot(self.prop())


if __name__ == '__main__':
    try:
        lexer = Lexer(sys.argv[1])
        tokens = lexer.lex()
        if '-l' in sys.argv:
            for i in tokens:
                print(token_name[i.tipo], i.valor)
        ast = Parser(tokens).parse()
        if '-p' in sys.argv:
            print(ast)
            print(json.dumps(ast.to_dict(), sort_keys=True, indent=4))
    except Exception as e:
        print(e)