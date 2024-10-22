import pytest
from rule_engine.parser import tokenize, Token, Lexer, Parser

from rule_engine.parser import LPAREN, STRING, COMPARISION, NUMBER, OR

def test_tokenize():
    rule = "(age > 30 OR department = 'Sales') AND age < 25" 

    tokens = tokenize(rule)
    expected_tokens = ['(', 'age', '>', '30', 'OR', 'department', '=', "'", 'Sales', "'", ')', 'AND', 'age', '<', '25']

    assert tokens == expected_tokens

def test_lexer():
    rule = "(age > 30 OR department = 'Sales') AND age < 25"
    lexer = Lexer(rule)
    token = lexer.get_next_token()
    assert token.type == LPAREN
    assert token.value == '('
    
    token = lexer.get_next_token()
    assert token.type == STRING
    assert token.value == 'age'

    token = lexer.get_next_token()
    assert token.type == COMPARISION
    assert token.value == '>'

    token = lexer.get_next_token()
    assert token.type == NUMBER
    assert token.value == '30'

    token = lexer.get_next_token()
    assert token.type == OR
    assert token.value == 'OR'

def test_lexer_invalid_token():
    invalid_rule = "(age > 30 @ salary = 5000)"
    lexer = Lexer(invalid_rule)

    with pytest.raises(Exception) as e:
        token = lexer.get_next_token()
        while token.type != 'EOF':
            print(token)
            token = lexer.get_next_token()
    assert "InvalidToken" in str(e.value)

def test_parser_invalid_syntax():
    rule = "age>30 AND || department='sales'"
    
    lexer = Lexer(rule)
    parser = Parser(lexer)
    
    with pytest.raises(Exception) as e:
        node = parser.expr()

    assert "SyntaxError" in str(e.value)
    
def test_parser_invalid_data_type():
    rule = "(age>20 && salary > 5000) OR age < 'sixty'"

    lexer = Lexer(rule)
    parser = Parser(lexer)
    
    with pytest.raises(Exception) as e:
        node = parser.expr()

    assert "TypeError" in str(e.value)
