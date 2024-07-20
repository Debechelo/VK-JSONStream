import os
import click

@click.command(name='gen-controllers')
@click.option('--model-file', required=True, type=click.Path(exists=True), help='Path to the Pydantic model file')
@click.option('--out-dir', required=True, type=click.Path(), help='Directory to save generated controllers')
def generate_controllers(model_file, out_dir):
    try:
        if model_file.endswith(".py"):
            model_name = os.path.splitext(os.path.basename(model_file))[0]
            controller_code = generate_controller_code(model_name)

            os.makedirs(out_dir, exist_ok=True)
            controller_filename = os.path.join(out_dir, f"{model_name}_controller.py")
            with open(controller_filename, "w", encoding="utf-8") as out:
                out.write(controller_code)

            click.echo(f"Generated controller: {controller_filename}")

    except FileNotFoundError:
        click.echo(f"Error: Model file {model_file} not found.")
    except Exception as e:
        click.echo(f"Error generating controllers: {e}")

def generate_controller_code(model_name: str) -> str:
    return f"""from fastapi import APIRouter
from rest.models.engine.application import {model_name.capitalize()} as {model_name}
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{model_name.lower()}/", response_model={model_name})
async def create_{model_name.lower()}(item: {model_name}):
    pass
    
    
@router.put("/{model_name.lower()}/{{item_id}}/configuration", response_model={model_name})
async def update_{model_name.lower()}_configuration(item_id: str, config: dict):
    pass
    

@router.put("/{model_name.lower()}/{{item_id}}/settings", response_model={model_name})
async def update_{model_name.lower()}_settings(item_id: str, settings: dict):
    pass
    

@router.put("/{model_name.lower()}/{{item_id}}/state", response_model={model_name})
async def update_{model_name.lower()}_state(item_id: str, state: str):
    pass
    

@router.delete("/{model_name.lower()}/{{item_id}}", response_model={model_name})
async def delete_{model_name.lower()}(item_id: str):
    pass
    

@router.get("/{model_name.lower()}/{{item_id}}", response_model={model_name})
async def get_{model_name.lower()}(item_id: str):
    pass
    

@router.get("/{model_name.lower()}/{{item_id}}/state", response_model=str)
async def get_{model_name.lower()}_state(item_id: str):
    pass
"""

# python cli/main.py gen-controllers --model-file rest/models/engine/application.py --out-dir rest/routes
# /engine