import argparse
from src.tokenizer import Tokenizer
from src.parser import Parser
from src.error_collector import ErrorCollector

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("prop", help="Propositional statement")
    arg_parser.add_argument("--tokens", "-t", action="store_true")
    arg_parser.add_argument("--ast", "-a", action="store_true")
    args = arg_parser.parse_args()
    
    error_collector = ErrorCollector(args.prop)

    tokenizer = Tokenizer(args.prop, error_collector)
    tokenizer.tokenize()

    parser = Parser(tokenizer.tokens, error_collector)
    ast = parser.parse()

    if error_collector.has_errors():
        error_collector.show_errors()
        return

    if args.ast:
        print(ast)

    if args.tokens:
        tokenizer.show_tokens()

if __name__ == '__main__':
    main()
