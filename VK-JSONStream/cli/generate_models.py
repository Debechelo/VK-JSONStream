import json
import os
import click
from pydantic import BaseModel, Field, create_model
from typing import Any, Dict, Type
import yaml


@click.command(name='gen-models')
@click.option('--schema-file', required=True, type=click.Path(exists=True), help='Path to JSON or YAML Schema file')
@click.option('--out-dir', required=True, type=click.Path(), help='Directory to save generated models')
def generate_models(schema_file, out_dir):
    try:
        with open(schema_file, "r", encoding="utf-8") as f:
            if schema_file.endswith(('.yaml', '.yml')):
                schema = yaml.safe_load(f)
            else:
                schema = json.load(f)

            model_name = schema.get("title", "GeneratedModel")
            fields = create_pydantic_model_field(model_name, schema)
            model_code = generate_model_code(model_name, fields)

            os.makedirs(out_dir, exist_ok=True)
            model_filename = os.path.join(out_dir, f"{model_name.lower()}.py")
            with open(model_filename, "w", encoding="utf-8") as out:
                out.write(model_code)

            click.echo(f"Generated Pydantic model: {model_filename}")

    except FileNotFoundError:
        click.echo(f"Error: File {schema_file} not found.")
    except Exception as e:
        click.echo(f"Error generating Pydantic model: {e}")


def create_pydantic_model_field(name: str, schema: Dict[str, Any]) -> Dict[str, Any]:
    properties = schema.get("properties", {})
    required_fields = schema.get("required", [])

    fields = {}
    for field_name, field_schema in properties.items():
        field_args = {"title": field_schema.get("title", field_name)}

        if "maxLength" in field_schema:
            field_args["max_length"] = field_schema["maxLength"]
        if "pattern" in field_schema:
            field_args["regex"] = field_schema["pattern"]
        if "minimum" in field_schema:
            field_args["ge"] = field_schema["minimum"]
        if "maximum" in field_schema:
            field_args["le"] = field_schema["maximum"]

        field_type = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "object": dict,
            "array": list
        }.get(field_schema.get("type", "Any"), Any)

        # Determine if field is required
        if field_name not in required_fields:
            field_default = None
        else:
            field_default = ...

        fields[field_name] = (field_type, field_args, field_default)

    return fields


def generate_model_code(name: str, fields: Dict[str, Any]) -> str:
    fields_code = []
    for field_name, (field_type, field_args, field_default) in fields.items():
        field_def = f"    {field_name}: {field_type.__name__}"
        #if field_default is None:
        field_def += " = Field(..."
        #else:
            #field_def += f" = Field(default={field_default}"

        # Add additional field arguments
        for key, value in field_args.items():
            field_def += f", {key}={value!r}"

        field_def += ")\n"
        fields_code.append(field_def)

    model_code = f"""from pydantic import BaseModel, Field

class {name}(BaseModel): 
""" + "".join(fields_code)

    return model_code


def create_pydantic_model(name: str, fields: Dict[str, Any]) -> Type[BaseModel]:
    return create_model(name, **fields)


# if __name__ == "__main__":
#     generate_models()

# python cli/main.py gen-models --schema-file=engine-schema.json --out-dir=rest/models/engine