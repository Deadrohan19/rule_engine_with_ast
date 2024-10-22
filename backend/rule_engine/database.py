
"""
Database operations for the rule engine.

"""

from sqlalchemy.orm import Session
from rule_engine.models import Rule


def get_rule(db: Session, rule_name: str) -> Rule:
    """
    Retrieve a rule from the database by its name.
    """
    return db.query(Rule).filter(Rule.rule_name == rule_name).first()


def create_rule(db: Session, rule_name: str, rule_str: str, rule_json: str) -> Rule:
    """
    Create a new rule in the database.

    Args:
        db (Session): The database session.
        rule_name (str): The name of the rule.
        rule_str (str): The original rule string
        rule_json (str): The JSON representation of the AST for the rule.

    Returns:
        Rule: The created rule object.
    """
    db_rule = Rule(rule_name=rule_name, rule_str=rule_str, rule_json=rule_json)
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

def update_rule(db: Session, rule_name: str, new_rule_str: str, new_rule_json: str) -> Rule:
    """
    Update an existing rule in the database.

    Args:
        db (Session): The database session.
        rule_name (str): The name of the rule to update.
        new_rule_str (str): The updated rule string.
        new_rule_json (str): The updated JSON representation of the AST for the rule.

    Returns:
        Rule: The updated rule object, or None if no rule was found.
    """
    # Retrieve the existing rule
    db_rule = db.query(Rule).filter(Rule.rule_name == rule_name).first()

    if db_rule is None:
        return None  # If rule does not exist, return None or raise an error based on preference

    # Update the rule fields
    db_rule.rule_str = new_rule_str
    db_rule.rule_json = new_rule_json

    # Commit the changes
    db.commit()
    db.refresh(db_rule)  # Refresh the object to reflect the latest state from the DB

    return db_rule
