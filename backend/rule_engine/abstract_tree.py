import json
from rule_engine.parser import Lexer, Parser, Node 
from globalDS import catalog # True: integer type, False: string type

def ast_to_json(ast: Node) -> str:
    """
    Convert AST root to JSON
    """
    if ast is None:
        return ""
    return json.dumps(ast, default=lambda o: o.__dict__)

def json_to_ast(rule_json: str) -> Node:
    """
    Conver JSON to AST (root Node)
    """
    data = json.loads(rule_json)
    return convert_to_node(data)

def convert_to_node(data: dict) -> Node:
    """
    Convert dictionary to AST Node
    """

    node = Node(type= data['type'], op= data['op'], attrType=data['attrType']) 
    if(data['type']== 'operator'):
        node.left = convert_to_node(data.get('left'))
        node.right = convert_to_node(data.get('right'))
    else:
        node.left = data['left']
        node.right = data['right']

    return node


class AST(object):
    def __init__(self, root=None):
        self.root = root

    def create_rule(self, rule: str):
        lexer = Lexer(rule)
        parser = Parser(lexer)
        self.root = parser.expr()
        return self.root
    
    def evaluate_rule(self, data):
        if self.root is None:
            return True
        return self.root.evaluate(data)


    def combine_rules(self, rules: list[str], operator: str):
        """
        Combines multiple rules into a single AST with the specified operator ('AND' or 'OR').
        
        Args:
            rules: List of rule strings to be combined.
            operator: The operator to combine the rules ('AND' or 'OR').
        
        Returns:
            The root of the combined AST.
        """
        if not rules:
            raise ValueError("The rule list cannot be empty")
        # TODO: add functionality to specify rule name too 
        # Parse the first rule
        lexer = Lexer(rules[0])
        parser = Parser(lexer)
        combined_ast = parser.expr()
        
        # Parse and combine each remaining rule with the operator
        for rule in rules[1:]:
            lexer = Lexer(rule)
            parser = Parser(lexer)
            next_ast = parser.expr()
            
            # Combine the two ASTs with the specified operator
            combined_ast = Node(type="operator", left=combined_ast, op=operator, right=next_ast)
        return combined_ast

