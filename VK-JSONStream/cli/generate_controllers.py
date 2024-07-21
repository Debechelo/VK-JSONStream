import os
import click


@click.command(name='gen-controllers')
@click.option('--model-file', required=True, type=click.Path(exists=True), help='Path to the Pydantic model file')
@click.option('--out-dir', required=True, type=click.Path(), help='Directory to save generated controllers')
def generate_controllers(model_file, out_dir):
    try:
        if model_file.endswith(".py"):
            model_name = os.path.splitext(os.path.basename(model_file))[0]
            controller_code = generate_controller_code(model_name, model_file)

            os.makedirs(out_dir, exist_ok=True)
            controller_filename = os.path.join(out_dir, f"{model_name}_controller.py")
            with open(controller_filename, "w", encoding="utf-8") as out:
                out.write(controller_code)

            click.echo(f"Generated controller: {controller_filename}")

    except FileNotFoundError:
        click.echo(f"Error: Model file {model_file} not found.")
    except Exception as e:
        click.echo(f"Error generating controllers: {e}")


def generate_controller_code(model_name: str, model_file: str) -> str:
    return f"""from fastapi import APIRouter, HTTPException, Depends
from {'.'.join(model_file[:-3].split('/'))} import {model_name.capitalize()} as {model_name}
from sqlalchemy.orm import Session
from src.app.db.database import get_db

router = APIRouter()


@router.post("/{model_name.lower()}/", response_model={model_name})
async def create_{model_name.lower()}(item: {model_name}, db: Session = Depends(get_db)):
    db_item = {model_name}(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("/{model_name.lower()}/{{item_id}}/configuration", response_model={model_name})
async def update_{model_name.lower()}_configuration(item_id: int, config: dict, db: Session = Depends(get_db)):
    db_item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.configuration = config
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("{model_name.lower()}/{{item_id}}/settings", response_model={model_name})
async def update_{model_name.lower()}_settings(item_id: int, settings: dict, db: Session = Depends(get_db)):
    db_item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.settings = settings
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("{model_name.lower()}/{{item_id}}/state", response_model={model_name})
async def update_{model_name.lower()}_state(item_id: int, state: str, db: Session = Depends(get_db)):
    db_item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.state = state
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("{model_name.lower()}/{{item_id}}", response_model={model_name})
async def delete_{model_name.lower()}(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return db_item


@router.get("{model_name.lower()}/{{item_id}}", response_model={model_name})
async def get_{model_name.lower()}(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("{model_name.lower()}/{{item_id}}/state", response_model=str)
async def get_{model_name.lower()}_state(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item.state
"""

# python cli/main.py gen-controllers --model-file src/app/models/application.py --out-dir src/app/routers