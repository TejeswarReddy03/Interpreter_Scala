INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
REM = 'REM'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
LCURL = 'LCURL'
RCURL = 'RCURL'
ID = 'ID'
ASSIGN = 'ASSIGN'
SEMI = 'SEMI'
DOT = 'DOT'
OBJECT = 'OBJECT'
VAR = 'VAR'
COLON = 'COLON'
COMMA = 'COMMA'
EOF = 'EOF'
DEF = 'def'
IF = 'IF'
ELSE = 'ELSE'
TRUE = 'TRUE'
FALSE = 'FALSE'
OBJECT = 'OBJECT'
DO = 'DO'
WHILE = 'WHILE'
INT = 'INT'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'IF': Token('IF', 'IF'),
    'ELSE': Token('ELSE', 'ELSE'),
    'TRUE': Token('TRUE', 'TRUE'),
    'FALSE': Token('FALSE', 'FALSE'),
    'VAR': Token('VAR', 'VAR'),
    'OBJECT': Token('OBJECT', 'OBJECT'),
    'DO': Token('DO', 'DO'),
    'WHILE': Token('WHILE', 'WHILE'),
    'INT': Token('INT','INT')
}


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != '/' or self.peek() != '*':
            self.advance()
        self.advance()
        self.advance()

    def number(self):
        """Return a (multidigit) integer  consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

            token = Token('INTEGER', int(result))

        return token

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result.upper(), Token(ID, result))
        return token

    # need to implement if ,else methods.

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char == '{':
                self.advance()
                return Token('LCURL', '{')

            elif self.current_char == '*' and self.peek() == '/':
                self.advance()
                self.advance()
                self.skip_comment()
                continue
            elif self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('LEQUAL', '<=')
            elif self.current_char == '<':
                self.advance()
                return Token('LESSTHAN', '<')
            elif self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('GEQUAL', '>=')

            elif self.current_char == '>':
                self.advance()
                return Token('GREATHAN', '<')
            elif self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('DEQUAL', '==')
            elif self.current_char == '=':
                self.advance()
                return Token('ASSIGN', '=')


            # in scala the starting char of the variable should not be a digit.
            elif self.current_char.isalpha():
                return self._id()

            elif self.current_char.isdigit():
                return self.number()

            elif self.current_char == ';':
                self.advance()
                return Token('SEMI', ';')
            elif self.current_char == '\n':
                self.advance()
                return Token('EOL', '\n')

            elif self.current_char == '+':
                self.advance()
                return Token('PLUS', '+')

            elif self.current_char == '-':
                self.advance()
                return Token('MINUS', '-')

            elif self.current_char == '*':
                self.advance()
                return Token('MUL', '*')

            elif self.current_char == '/':
                self.advance()
                return Token('DIV', '/')

            elif self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')

            elif self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')

            elif self.current_char == ':':
                self.advance()
                return Token('COLON', ':')

            elif self.current_char == '}':
                self.advance()
                return Token('RCURL', '}')

            elif self.current_char == '%':
                self.advance()
                return Token('REM', '%')

            self.error()

        return Token(EOF, None)

    def checking(self):

        currenttoken = None
        while self.current_char is not None:
            currenttoken = self.get_next_token()
            print(currenttoken.type, " ", currenttoken.value)


class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Body(AST):
    """Represents a 'BEGIN ... END' block"""

    def __init__(self):
        self.children = []


class Assign_stmt(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Declaration(AST):
    def __init__(self, var_node, type_node, op, val):
        self.var_node = var_node
        self.type_node = type_node
        self.token = self.op = op
        self.val = val
        
class Cond_stmt(AST):
    def __init__(self, leftexpr, comp_op, rightexpr):
        self.leftexpr = leftexpr
        self.comp_op = comp_op
        self.rightexpr = rightexpr


class Var(AST):
    """The Var node is constructed out of ID token."""

    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Program(AST):
    def __init__(self, name, body):
        self.name = name
        self.body = body


class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Cond_stmt(AST):
    def __init__(self, left, comp_op, right):
        self.left = left
        self.comp_op = comp_op
        self.right = right


class If_stmt(AST):
    def __init__(self, condition, body, else_block):
        self.condition = condition
        self.body = body
        self.else_block = else_block


class DO_stmt(AST):
    def __init__(self, while_condition, do_body):
        self.condition = while_condition
        self.do_body = do_body

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def skip(self):
        self.current_token = self.lexer.get_next_token()

    def program(self):

        """program : OBJECT variable '{' stmt_list '}' """

        self.eat(OBJECT)
        var_node = self.id()
        prog_name = var_node.value
        print(prog_name)
        print(self.current_token)
        body_node = self.body()
        program_node = Program(prog_name, body_node)

        return program_node

    def body(self):
        """body :  { statement_list }"""
        print("body")
        print(self.current_token)
        self.eat(LCURL)
        nodes = self.stmt_list()
        self.eat(RCURL)
        print("RCURL")
        root = Body()
        for node in nodes:
           root.children.append(node)
        return root

    def stmt_list(self):
        """stmt_list : stmt [[SEMI] stmt_list]"""
        print("stmtlist")
        print(self.current_token)
        node = self.stmt()
        results = [node]
        while self.current_token.type != RCURL and self.current_token.type != EOF:
            results.append(self.stmt())
        return results

    def stmt(self):
        """
        statement : assign_stmt
                    | stmt1
                    | empty
        """
        print("stmt")
        if self.current_token.type == ID:
            node = self.assign_stmt()
        elif self.current_token.type == VAR:
            node = self.decl_stmt()
        else:
            node = self.stmt1()
        if (self.current_token.type == SEMI):
            self.eat(SEMI)

        return node

    def assign_stmt(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        print("assign_stmt")
        left = self.id()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign_stmt(left, token, right)

        return node
    
    def decl_stmt(self):
        
        print("decleration stmt")
        self.eat(VAR)
        print("var eaten")
        var_node = self.current_token
        print(self.current_token)
        self.eat(ID)
        print(self.current_token)
        self.eat(COLON)
        print("done")
        type_node = self.type_spec()
        print("done")
        print(self.current_token)
        self.eat(INT)
        token = self.current_token
        print(self.current_token)
        self.eat(ASSIGN)
        val = self.expr()
        
        decl = Declaration(var_node, type_node,token,val)
        
        return decl

    def type_spec(self):
        """type_spec : INTEGER
                     | REAL
        """
        token = self.current_token
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
        node = Type(token)
        return node
    
    
    def id(self):
        """
        variable : ID | const
        """
        print(self.current_token.value)
        print("id")
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        return NoOp()

    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
        """
        print("expr")
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        """term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*"""
        print("term")
        node = self.factor()
        while self.current_token.type in (MUL, DIV, REM):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == REM:
                self.eat(REM)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        """factor : PLUS factor
                  | MINUS factor
                  | LPAREN expr RPAREN
                  | variable
        """
        print("factor")
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            print(token)
            return Num(token)
        else:
            node = self.id()
            return node

    def stmt1(self):
        """stmt1: 'if' '(' con_stmt ')' stmt_list [[semi] 'else' expr]  (cond_stmt)
                | 'do' Expr [semi] `while' `(' Expr ')'  (do_stmt)"""
        print("stmt1")
        if self.current_token.type == IF:
            node = self.if_stmt()
        elif self.current_token.type == DO:
            node = self.do_stmt()
        else:
            node = self.empty()
        return node

    def if_stmt(self):
        print("ifstmt")
        self.eat(IF)
        print(self.current_token)
        self.eat(LPAREN)
        print(self.current_token)
        condition = self.cond_stmt()
        print(self.current_token)
        self.eat(RPAREN)
        while self.current_token.type == 'EOL':
            self.advance()
        body = self.stmt_list()
        print(self.current_token)
        while self.current_token.type == 'EOL':
            self.advance()
        if (self.current_token.type == 'ELSE'):
            self.eat(ELSE)
            print(self.current_token)
            else_block = self.stmt_list()
        else:
            else_block = self.empty()

        node = If_stmt(condition, body, else_block)

        return node

    def do_stmt(self):
        print("dostmt")
        self.eat(DO)
        print(self.current_token)
        if (self.current_token.type == 'LCURL'):
            self.eat(LCURL)
            print(self.current_token)
            statement = self.stmt_list()
            print(self.current_token)
            self.eat(RCURL)
        else:
            statement = self.stmt_list()
        print(self.current_token)
        self.eat(WHILE)
        print(self.current_token)
        self.eat(LPAREN)
        print(self.current_token)
        cond = self.cond_stmt()
        print(self.current_token)
        self.eat(RPAREN)
        node = DO_stmt(cond, statement)

        return node

    def cond_stmt(self):
        print("cond_stmt")
        leftexpr = self.expr()
        comp_op = self.current_token.type
        self.skip()
        rightexpr = self.expr()
        node = Cond_stmt(leftexpr, comp_op, rightexpr)
        return node

    def parse(self):
        print("parse")
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node
    
class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
    
    
class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return '<{name}:{type}>'.format(name=self.name, type=self.type)

    __repr__ = __str__


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    __repr__ = __str__
    
class SymbolTable(object):
    def __init__(self):
        self._symbols = {}
        self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltinTypeSymbol('INTEGER'))

    def __str__(self):
        s = 'Symbols: {symbols}'.format(
            symbols=[value for value in self._symbols.values()]
        )
        return s

    __repr__ = __str__

    def define(self, symbol):
        print('Define: %s' % symbol)
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        print('Lookup: %s' % name)
        symbol = self._symbols.get(name)
        # 'symbol' is either an instance of the Symbol class or 'None'
        return symbol
    
    
class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.symtab = SymbolTable()

    def visit_Program(self, node):
        self.visit(node.body)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Num(self, node):
        pass

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_Body(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Declaration(self, node):
        type_name = node.type_node.value
        type_symbol = self.symtab.lookup(type_name)
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)
        self.symtab.define(var_symbol)
        self.visit(node.val)

    def visit_Assign_stmt(self, node):
        var_name = node.left.value
        var_symbol = self.symtab.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))

        self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.symtab.lookup(var_name)

        if var_symbol is None:
            raise NameError(repr(var_name))

    
class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.GLOBAL_MEMORY = {}

    def visit_Program(self, node):
        self.visit(node.body)

    def visit_Declaration(self, node):
        # Do nothing
        pass

    def visit_Type(self, node):
        # Do nothing
        pass

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == REM:
            return float(self.visit(node.left)) % float(self.visit(node.right))

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Body(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign_stmt(self, node):
        var_name = node.left.value
        var_value = self.visit(node.right)
        self.GLOBAL_MEMORY[var_name] = var_value

    def visit_Var(self, node):
        var_name = node.value
        var_value = self.GLOBAL_MEMORY.get(var_name)
        return var_value

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        tree = self.tree
        if tree is None:
            return ''
        return self.visit(tree)


def main():
    import sys
    text = input("enter input : ")

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    symtab_builder = SymbolTableBuilder()
    symtab_builder.visit(tree)
    print('')
    print('Symbol Table contents:')
    print(symtab_builder.symtab)

    interpreter = Interpreter(tree)
    result = interpreter.interpret()

    print('')
    print('Run-time GLOBAL_MEMORY contents:')
    for k, v in sorted(interpreter.GLOBAL_MEMORY.items()):
        print('{} = {}'.format(k, v))


if __name__ == '__main__':
    main()