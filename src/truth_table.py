from prettytable import PrettyTable


class TruthTable:
    def __init__(self, ast, st, nfields):
        self.ast = ast
        self.sym_t = st
        self.table = PrettyTable()
        
        fields = list()
        for sym in self.sym_t.symbols:
            fields.append(sym.symbol)
        fields += self.ast.infix_list_until(nfields)
        self.table.field_names = fields
              
    def show(self):
        print(self.table)