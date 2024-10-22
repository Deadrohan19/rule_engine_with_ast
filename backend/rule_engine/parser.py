""" Lexer and Parser for rules """

import re
from globalDS import catalog  
from rule_engine.error import SyntaxError, InvalidTokenError, TypeError, InsufficientDataError

###############################################################################
#                                                                             #
#  LEXER        
###############################################################################

NUMBER, STRING, LPAREN, RPAREN, AND, OR, COMPARISION, EOF = 'NUMBER', 'STRING', 'LPAREN', 'RPAREN', 'AND', 'OR', 'COMPARISION', 'EOF'

def tokenize(rule: str) -> list[str]:
    token_pattern = re.compile(r'\s*(-?\d+.\d+?|<=|>=|!=|==|&&|\|\||[()><=]|[\w]+|[^ \t\n\r\f\v\w])\s*')
    return [token for token in token_pattern.findall(rule) if token.strip()]


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(AND, '&&')
            Token(OR, '||')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        self.tokens = tokenize(text)
        self.pos = -1
        self.current_val = "" 

    def get_next_token(self):
        """ Lexical analyzer """

        self.pos+=1
        if self.pos < len(self.tokens):
            self.current_val = self.tokens[self.pos]
            if self.current_val in ('AND', '&&'):
                return Token(AND, 'AND')
            
            if self.current_val in ('OR', '||'):
                return Token(OR, 'OR')
            
            if self.current_val in ('>', '<', '>=', '<=', '=', '!='):
                return Token(COMPARISION, self.current_val)
            
            if self.current_val == '(':
                return Token(LPAREN, '(')
            
            if self.current_val == ')':
                return Token(RPAREN, ')')
            
            if re.match(r'^-?\d+(\.\d+)?$', self.current_val): 
                return Token(NUMBER, self.current_val)
            
            # for 'Sales' case
            if self.current_val == "'":
                if self.pos+2 < len(self.tokens) and self.tokens[self.pos+2] == "'":
                    if re.match(r'^[\w]+$', self.tokens[self.pos+1]) == False:
                        raise InvalidTokenError(token=self.current_val, pos = self.pos)
                    tmpToken = Token(STRING, self.tokens[self.pos+1])
                    self.pos +=2
                    return tmpToken
                    
            if re.match(r'^[\w]+$', self.current_val):
                return Token(STRING, self.current_val)

            raise InvalidTokenError(token=self.current_val, pos = self.pos)
        return Token(EOF, None)

###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class Node(object):
    def __init__(self, type, left=None, op=None, right=None, attrType=None):
        self.type = type
        self.op = op
        self.attrType = attrType
        self.left = left
        self.right = right

    def __str__(self):
        return "type: {}, op: {}, attrType: {}, left: {}, right: {}".format(
            self.type, self.op, self.attrType, self.left, self.right
        )

    def __repr__(self):
        return self.__str__()
    
    def comparision(self, val):
        # checking for same type
        if self.left not in catalog:
            catalog[self.left] = self.attrType

        if catalog[self.left] == NUMBER and not isinstance(val, (int, float)):
            raise TypeError(attr=self.left, val=val, ref=self.right)
        if catalog[self.left] == NUMBER:
            self.right = float(self.right)
            val = float(val)
            if self.op == ">":
                return val > self.right
            elif self.op == ">=":
                return val >= self.right
            elif self.op == "<":
                return val < self.right
            elif self.op == "<=":
                return val <= self.right

        # common comparisions
        if self.op == "=":
            return val == self.right
        elif self.op == "!=":
            return val != self.right

    def evaluate(self, data):
        if(self.type=="comparision"):
            if self.left not in data:
                raise InsufficientDataError(self.left)

            return self.comparision(data[self.left])
        elif(self.type=="operator"):
            if self.op == "AND":
                # short circuiting, if left term is False then right term would not be evaluated.
                return self.left.evaluate(data) and self.right.evaluate(data)
            else:
                return self.left.evaluate(data) or self.right.evaluate(data)

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError(expected= token_type, got= self.current_token.type, val=self.current_token.value)
    
    def comparision(self):
        """comparision: variable operator value"""

        left = self.current_token.value
        self.eat(STRING)
        op = self.current_token.value
        self.eat(COMPARISION)
        right = self.current_token.value

        attrType = self.current_token.type
        if attrType == NUMBER:
            self.eat(NUMBER)
        else: 
            self.eat(STRING)
        
        # Here I have added attribute validation, keep adding in hashmap and during
        # evaluation check for same datatype in this attribute COMPARISION
        if left in catalog:
            if catalog[left] != attrType: 
                raise Exception("TypeError: different type of value for same attribute: {}".format(left))
        else:
            catalog[left] = attrType

        # Create AST NODE: comparision type 
        node = Node(type="comparision", left=left,op=op, right=right, attrType=attrType)
        return node

    def term(self):
        """term: comparision | LPAREN expression RPAREN"""
        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif self.current_token.type == STRING:
            node = self.comparision()
            return node

    def expr(self):
        """
        expr: term ((AND|OR) term)*
        term: comparision | LPAREN expr RPAREN
        comparision: variable operator value
        """
        
        node = self.term()

        while self.current_token.type in ('AND', 'OR'):
            op = self.current_token
            if op.type == AND:
                self.eat(AND)
            else:
                self.eat(OR)

            node = Node(type="operator", left=node, op=op.value, right=self.term())

        return node
