import dataclasses

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

@dataclasses.dataclass
class Token:
    type: int = 0
    
    # ¿Será necesario guardar el valor teniendo los índices y considerando que es una cadena pequeña?
    value: str = ""
    
    start: int = None
    end: int = None
    
    def __str__(self):
        if not self.value:
            return f"Token: {token_name(self)} {self.start}:{self.end}"
        return f"Token: {token_name(self)}, '{self.value}' {self.start}:{self.end}"
    
# Returns a string representation of a tokens type
# NOTE: Could be implemented as a data class method of Token
def token_name(t: Token) -> str:
    token_str = ['N/a', 'VARIABLE', 'BICONDITIONAL', 'IMPL', 'DISJ', 'CONJ', 'NEG', 'L_PAR', 'R_PAR', 'EOI']
    return token_str[t.type]


