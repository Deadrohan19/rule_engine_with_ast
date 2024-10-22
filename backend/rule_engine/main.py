"""
FASTAPI

API endpoints

"""
import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from rule_engine import models, database
from rule_engine.abstract_tree import AST, ast_to_json, json_to_ast

app = FastAPI()

class CreateParam(BaseModel):
    name: str
    rule: str

class CombineParam(BaseModel):
    rules: list[str]
    operator: str = "AND"

class EvaluateParam(BaseModel):
    rule_name: str
    data: dict

class ASTNode(BaseModel):
    type: str
    left: dict
    op: str
    right: dict
    attrType: str = None

def init_db():
    db = models.SessionLocal()

    try:
        yield db
    finally:
        db.close()

# AST object for executing methods
ast = AST()

@app.post("/create_rule", response_model=ASTNode)
def create_rule(param: CreateParam, db: Session = Depends(init_db)):
    """
    Create a new rule and store it in database

    Args:
        params: name & rule
    Response:
        ASTNode: jsonified AST node
    """ 
    try:
        rule_ast = ast.create_rule(param.rule)
        rule_json = ast_to_json(rule_ast)

        database.create_rule(db,rule_name=param.name, rule_str=param.rule, rule_json=rule_json) 

        rule_data = json.loads(rule_json)
        return JSONResponse(rule_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/evaluate_rule")
def evaluate_rule(param: EvaluateParam, db: Session = Depends(init_db)):
    """
    Evaluate a rule against provided data.

    Args:
        param: rule_name & data
    Response:
        result with True or False
    """
    rule = database.get_rule(db, rule_name= param.rule_name)
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    try:
        rule_ast = json_to_ast(rule.rule_json)
        res = rule_ast.evaluate(param.data) 
        return {"result": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/combine_rules", response_model= ASTNode)
def combine_rules(param: CombineParam, db: Session = Depends(init_db)):
    """
    Combine multiple rules into single AST

    Args:
       params: rules, operator (optional)

    Response:
        ASTNode: combined ASTNode in json form 
    """
    try:
        combined_ast = ast.combine_rules(param.rules, param.operator) 
        rule_json = ast_to_json(combined_ast)
        rule_data = json.loads(rule_json)
        return JSONResponse(rule_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
