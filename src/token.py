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

# TODO: Reescribir Token como una clase para definir start con el mismo
# valor de end con el fin de evitar indices como None:int
class Token:
    def __init__(self, type = 0, start = None, end = None):
        self.type = type 

        # ¿Será necesario guardar el valor teniendo los índices y considerando que es una cadena pequeña?
        self.value: str = ""

        self.start = start 
        self.end = end

    def __str__(self):
        if not self.value:
            return f"Token: {token_name(self.type)} {self.start}:{self.end}"
        return f"Token: {token_name(self.type)}, '{self.value}' {self.start}:{self.end}"

# Returns a string representation of a tokens type
# NOTE: Could be implemented as a data class method of Token
def token_name(t: int) -> str:
    token_str = ['UNKNOWN', 'VARIABLE', 'BICONDITIONAL', 'IMPL', 'DISJ', 'CONJ', 'NEG', 'L_PAR', 'R_PAR', 'EOI']
    return token_str[t]
