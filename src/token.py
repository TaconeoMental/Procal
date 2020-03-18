# Token types enumeration
(
    UNKNOWN,
    VARIABLE,
    OP_BICOND,
    OP_IMPL,
    OP_DISJ,
    OP_CONJ,
    OP_NEG,
    L_PAR,
    R_PAR,
    EOI
) = range(10)


class Token:
    def __init__(self, type=0, start=None, end=None):
        self.type = type

        # ¿Será necesario guardar el valor teniendo los índices y considerando que es una cadena pequeña?
        self.value: str = ""

        self.start = start
        self.end = end

    def __str__(self):
        if not self.value:
            return f"Token: {token_name(self.type):<13} {self.start: >5}:{self.end}"
        return f"Token: {token_name(self.type):<13} {self.start:>5}:{self.end} {self.value:>5}"


# NOTE: Could be implemented as a data class method of Token
def token_name(t: int) -> str:
    token_str = ['UNKNOWN', 'VARIABLE', 'BICONDITIONAL',
                 'IMPL', 'DISJ', 'CONJ', 'NEG', 'L_PAR', 'R_PAR', 'EOI']
    return token_str[t]
    
def token_op(t: int) -> str:
    token_str = ['↔', '→', '∨', '∧']
    return token_str[t - 2]
    
def eval_bin(op, left, right):
    funcs = {
            OP_BICOND: lambda x, y: 1 if x == y else 0, # XNOR
            OP_IMPL: lambda x, y: 0 if x and not y else 1,
            OP_DISJ: lambda x, y: x or y,
            OP_CONJ: lambda x, y: x and y
            }
    return funcs[op](left, right)

