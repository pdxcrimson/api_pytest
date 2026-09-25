# utils/validators.py
import json
from pathlib import Path

import jsonschema

SCHEMAS_DIR = Path(__file__).parent.parent / "schemas"


def load_schema(name: str) -> dict:
    return json.loads((SCHEMAS_DIR / f"{name}.json").read_text())


def assert_schema(data: dict | list, schema_name: str):
    """Raises AssertionError with a clear message if validation fails."""
    schema = load_schema(schema_name)
    try:
        if isinstance(data, list):
            for item in data:
                jsonschema.validate(instance=item, schema=schema)
        else:
            jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        raise AssertionError(
            f"Schema '{schema_name}' violation:\n"
            f"  Path:    {' -> '.join(str(p) for p in e.absolute_path)}\n"
            f"  Message: {e.message}\n"
            f"  Value:   {e.instance}"
        ) from e
