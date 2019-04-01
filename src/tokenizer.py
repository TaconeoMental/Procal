import token
from error_collector import ErrorCollector

class Tokenizer:
    def __init__(prop: str, err_coll: ErrorCollector):
        self.proposition = prop
        self.error_collector = err_coll
