import argparse
from src.tokenizer import Tokenizer
from src.parser import Parser

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("prop", help="Propositional statement")
    arg_parser.add_argument("--tokens", "-t", action="store_true")
    arg_parser.add_argument("--ast", "-a", action="store_true")
    args = arg_parser.parse_args()

    tokenizer = Tokenizer(args.prop)
    
    if args.tokens:
        tokenizer.show_tokens()

    # Falla al generar una excepción en el método parse, pues
    # la variable ast nunca se asigna y no puede imprimirse después.
    # TODO: Escribir recolector de Errores
    try:
        parser = Parser(tokenizer.tokens)
        ast = parser.parse()
    except Exception as e:
        print(str(e))

    if args.ast:
        print(ast)

if __name__ == '__main__':
    main()
