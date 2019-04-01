from dataclasses import dataclass
from typing import List

# I am not (entirely) sure if this data class is really necessary
@dataclass
class ErrorPosition:
    column_number: int

@dataclass
class GeneralError:
    error_description: str

    # Should not really use this assuming that only one proposition
    # can be given at a time
    full_line: str
    position: ErrorPosition

    # TODO
    def __str__(self):
        pass

@dataclass
class ErrorCollector:
    errors: List[GeneralError]

    # TODO
    def add_error(err: GeneralError):
        pass

    def has_errors() -> bool:
        pass

    def show_errors():
        pass
