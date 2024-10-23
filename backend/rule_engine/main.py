"""
FASTAPI

API endpoints

"""
import json
from globalDS import catalog

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from rule_engine import models, database
from rule_engine.abstract_tree import AST, ast_to_json, json_to_ast

app = FastAPI()

# List of allowed origins (adjust as needed)
origins = [
    "http://localhost:3000",  # If your frontend is on port 3000
    "http://localhost:5000",  # If the backend is making internal requests
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Can also be ['*'] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

class CreateParam(BaseModel):
    """Pydantic model for an create request."""
    name: str
    rule: str

class CombineParam(BaseModel):
    """Pydantic model for an combine request."""
    rules: list[str]
    operator: str = "AND"

class EvaluateParam(BaseModel):
    """Pydantic model for an evaluation request."""
    rule_name: str
    data: dict

class ASTNode(BaseModel):
    """Pydantic model for an AST node."""
    type: str
    left: dict
    op: str
    right: dict
    attrType: str = None

def init_db():
    """
    Dependency to provide the database session.

    Yields:
        Session: SQLAlchemy session object. The session is closed once the request lifecycle is complete.
    """
    db = models.SessionLocal()

    try:
        yield db
    finally:
        db.close()

# AST object for executing methods
ast = AST()

@app.post("/create_rule", response_model=ASTNode)
def create_rule(rule_string: CreateParam, db: Session = Depends(init_db)):
    """
    Create a new rule and store it in the database.

    Args:
        rule_string: The rule string and its associated name.
        db (Session): Database session for storing the rule.

    Returns:
        ASTNode: Root node of the generated AST in JSON format.
    Raises:
        HTTPException: If rule parsing fails or any error occurs, returns a 400 error with the failure details.
    """
    try:
        rule_ast = ast.create_rule(rule_string.rule)
        rule_json = ast_to_json(rule_ast)

        database.create_rule(db,rule_name=rule_string.name, rule_str=rule_string.rule, rule_json=rule_json) 

        rule_data = json.loads(rule_json)
        return JSONResponse(rule_data)
    # Handle specific IntegrityError caused by UniqueViolation
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            # If the error is a UniqueViolation, return a proper HTTP response
            raise HTTPException(
                status_code=400,
                detail=f"Rule with the name '{rule_string.name}' already exists. Please choose a different name."
            )
        else:
            raise HTTPException(status_code=400, detail="Database error occurred.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/evaluate_rule")
def evaluate_rule(request: EvaluateParam, db: Session = Depends(init_db)):
    """
    Evaluate a stored rule using provided data.

    Args:
        request (EvaluateParam): Contains the rule ID and the data to be evaluated.
        db (Session): Database session to retrieve the stored rule.

    Returns:
        Dict: Evaluation result (True/False based on rule evaluation).
    Raises:
        HTTPException: 404 error if the rule is not found in the database.
    """
    rule = database.get_rule(db, rule_name= request.rule_name)
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    try:
        rule_ast = json_to_ast(rule.rule_json)
        res = rule_ast.evaluate(request.data) 
        return {"result": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/combine_rules", response_model= ASTNode)
def combine_rules(rule_list: CombineParam, db: Session = Depends(init_db)):
    """
    Combine multiple rule strings into a single AST.

    Args:
        rule_list (CombineParam): List containing multiple rule strings.

    Returns:
        ASTNode: Root node of the combined AST, joined by AND operators.
    """
    try:
        combined_ast = ast.combine_rules(rule_list.rules, rule_list.operator) 
        rule_json = ast_to_json(combined_ast)
        rule_data = json.loads(rule_json)
        return JSONResponse(rule_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_catalog", response_model= dict)
def get_catalog():
    """
    Send catalog containing attribute with their data type

    Returns:
        Catalog: Dictonary of {attr: data_type}
    """
    return JSONResponse(catalog)

@app.get("/get_rule", response_model=ASTNode)
def get_rule(rule_name: str, db: Session = Depends(init_db)):
    """
    Get a stored rule from the database.

    Args:
        rule_name (str): The name of the rule to retrieve.
        db (Session): Database session to retrieve the rule.

    Returns:
        ASTNode: Root node of the retrieved rule in JSON format.
    Raises:
        HTTPException: 404 error if the rule is not found in the database.
    """
    rule = database.get_rule(db, rule_name=rule_name)
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    rule_data = json.loads(rule.rule_json)
    return JSONResponse(rule_data)

@app.get("/get_all_rule_names", response_model= list[str])
def get_all_rule_names(db: Session = Depends(init_db)):
    """
    Retrieve all rule names from the database.

    Returns:
        List[str]: List of rule names.
    """
    return JSONResponse(database.get_all_rule_names(db))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
