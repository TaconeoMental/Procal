import dataclasses

# Token types enumeration
(
    VARIABLE,
    OP_BICOND,
    OP_IMPL,
    OP_DISJ,
    OP_CONJ,
    OP_NEG,
    L_PAR,
    R_PAR,
    EOI
) = range(9)

# Returns a string representation of a tokens type
# NOTE: Could be implemented as a data class method of Token
def token_name(t: Token) -> str:
    token_str = ['VARIABLE', '<->', '->', '|', '&', '~', 'L_PAR', 'R_PAR', 'EOI']
    return token_str[t.type]

@dataclasses.dataclass
class Token:
    type: int
    value: str = ""
