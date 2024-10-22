
import pytest
from rule_engine.abstract_tree import AST, Node, ast_to_json, json_to_ast  

@pytest.fixture
def ast():
    """Fixture to initialize an AST for each test."""
    return AST()

def test_create_rule_individual(ast):
    """
    Test creating individual rules and verify their AST representation.
    """
    # Define a rule string
    rule1 = "age > 30 AND department = 'Sales'"
    
    # Create the rule and get the root of the AST
    ast_root = ast.create_rule(rule1)
    
    # Verify the AST structure
    assert isinstance(ast_root, Node)  # Check if root is an instance of Node
    assert ast_root.op == "AND"        # The top-level operator should be "AND"
    assert ast_root.left.left == "age" # Check left operand
    assert ast_root.right.left == "department"  # Check right operand

def test_combine_rules(ast):
    """
    Test combining multiple rules and check the combined AST.
    """
    rule1 = "age > 30 AND department = 'Sales'"
    rule2 = "salary > 50000 OR experience > 5"

    # Combine the rules
    combined_ast = ast.combine_rules([rule1, rule2], operator="AND")

    # Check the top-level operator and structure of the AST
    assert isinstance(combined_ast, Node)
    assert combined_ast.op == "AND"  # Assuming "AND" as the top-level operator
    assert combined_ast.left.left.left == "age"  # Check left node in combined rule
    assert combined_ast.right.left.left == "salary"  # Check right node in combined rule

def test_combine_and_logic(ast):
    """
    Test combining multiple rules and evaluating them on more complex scenarios.
    """
    rule1 = "age > 30 AND department = 'Sales'"
    rule2 = "salary > 50000 OR experience > 5"
    rule3 = "age < 25 AND department = 'Marketing'"

    # Combine multiple rules
    combined_ast = ast.combine_rules([rule1, rule2, rule3], operator="OR")

    # Test data that should satisfy the combined rule
    data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
    result = combined_ast.evaluate(data)
    assert result is True

    # Test data that does not satisfy the combined rule
    data2 = {"age": 20, "department": "Engineering", "salary": 30000, "experience": 2}
    result2 = combined_ast.evaluate(data2)
    assert result2 is False

def test_evaluate_rule(ast):
    """
    Test evaluating rules against sample JSON data.
    """
    rule = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    ast.create_rule(rule)

    # Test data that should return True
    data1 = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
    result1 = ast.evaluate_rule(data1)
    assert result1 is True

    # Test data that should return False
    data2 = {"age": 25, "department": "Marketing", "salary": 60000, "experience": 3}
    result2 = ast.evaluate_rule(data2)
    assert result2 is False

def test_invalid_rule_handling(ast):
    """
    Test error handling for invalid rule strings and ensure proper exceptions are raised.
    """
    invalid_rule = "age > 30 AND department == 'Sales'"  # Using '==' instead of '='

    with pytest.raises(Exception) as excinfo:
        ast.create_rule(invalid_rule)

    assert "Invalid" in str(excinfo.value)

def test_attribute_validation(ast):
    """
    Test validation of attributes during rule evaluation (e.g., correct data types).
    """
    rule = "age > 30 AND salary > 50000"
    ast.create_rule(rule)

    # Test data with invalid type for "age"
    data_invalid = {"age": "thirty-five", "salary": 60000}

    with pytest.raises(Exception) as excinfo:
        ast.evaluate_rule(data_invalid)
    
    assert "TypeError"  in str(excinfo.value)

def test_evaluate_rule_missing_data(ast):
    """
    Test Validation of missing required attributes during rule evaluation
    """
    rule = "age > 30 AND department = 'Sales'"
    ast.create_rule(rule)
    
    missing_data = {"age": 40, "Salary": 5000}

    with pytest.raises(Exception) as e:
        print(ast.evaluate_rule(missing_data))
    
    assert "InsufficientDataError" in str(e.value)


def test_modification_of_existing_rules(ast):
    """
    Test modifying existing rules by changing operators, values, or sub-expressions.
    """
    rule = "age > 30 AND department = 'Sales'"
    ast.create_rule(rule)

    # Modify the rule to "age > 40"
    ast.root.left.right = 40

    data = {"age": 35, "department": "Sales"}
    result = ast.evaluate_rule(data)
    assert result is False

    data_modified = {"age": 45, "department": "Sales"}
    result_modified = ast.evaluate_rule(data_modified)
    assert result_modified is True

def test_json_to_ast_and_vice_versa(ast):
    """
    Testing the conversion functions
        json -> AST
        AST -> JSON
    """

    rule = "age > 40 AND department = 'Sales'"

    ast.create_rule(rule)

    # converting from AST to JSON
    rule_json = ast_to_json(ast.root)

    # converting from JSON to AST
    rule_ast = json_to_ast(rule_json)

    # creating new AST object with rule_ast
    newAst = AST(rule_ast)

    data = {"age": 35, "department": "Sales"}
    assert ast.evaluate_rule(data) == newAst.evaluate_rule(data)

    data2 = {"age": 45, "department": "Sales"}
    assert ast.evaluate_rule(data2) == newAst.evaluate_rule(data2)
