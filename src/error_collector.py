from dataclasses import dataclass, field
from typing import List

from src.token import Token


class Error:
    def __init__(self, token, descrip):
        self.error_description = descrip
        
        # Todo este lío debería haber sido resuelto en Token
        if token.start is None:
            self.start = token.end
        else:
            self.start = token.start
        
        self.end = token.end
        
        self.length = self.end - self.start + 1
            

    # TODO
    def __str__(self):
        return self.error_description

@dataclass
class ErrorCollector:
    proposition: str
    
    errors: List[Error] = field(default_factory=list)

    # TODO
    def add_error(self, err: Error):
        self.errors.append(err)

    def has_errors(self) -> bool:
        if not self.errors:
            return False
        return True

    def show_errors(self):
        for err in self.errors:
            print("Error:", err)
            print(self.proposition)
            print(' ' * err.start + '^' * err.length)
