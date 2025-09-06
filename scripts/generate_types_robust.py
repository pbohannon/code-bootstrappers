#!/usr/bin/env python3
"""
Robust TypeScript type generation from Pydantic schemas.
This script uses Pydantic's native JSON schema generation and converts it to TypeScript.
It handles edge cases gracefully and doesn't depend on buggy third-party libraries.
"""

import json
import importlib.util
import inspect
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union
from datetime import datetime
import sys
import os


class TypeScriptGenerator:
    """Generate TypeScript types from JSON Schema."""
    
    def __init__(self):
        self.interfaces: Dict[str, str] = {}
        self.processed_refs: Set[str] = set()
        
    def json_schema_to_typescript(self, schema: Dict[str, Any], interface_name: str = "Model") -> str:
        """Convert a JSON Schema to TypeScript interface."""
        if schema.get("type") == "object":
            return self._generate_interface(schema, interface_name)
        elif schema.get("type") == "array":
            items_type = self._resolve_type(schema.get("items", {}))
            return f"{items_type}[]"
        else:
            return self._resolve_type(schema)
    
    def _generate_interface(self, schema: Dict[str, Any], interface_name: str) -> str:
        """Generate a TypeScript interface from an object schema."""
        properties = schema.get("properties", {})
        required = set(schema.get("required", []))
        
        if not properties:
            return f"export interface {interface_name} {{\n  [key: string]: any;\n}}"
        
        interface_parts = []
        interface_parts.append(f"export interface {interface_name} {{")
        
        for prop_name, prop_schema in properties.items():
            is_required = prop_name in required
            optional_marker = "" if is_required else "?"
            
            prop_type = self._resolve_type(prop_schema)
            
            # Add description as comment if available
            description = prop_schema.get("description")
            if description:
                interface_parts.append(f"  /**\n   * {description}\n   */")
            
            interface_parts.append(f"  {prop_name}{optional_marker}: {prop_type};")
        
        interface_parts.append("}")
        
        return "\n".join(interface_parts)
    
    def _resolve_type(self, schema: Dict[str, Any]) -> str:
        """Resolve a JSON Schema type to TypeScript type."""
        if not schema:
            return "any"
        
        schema_type = schema.get("type")
        
        # Handle null type
        if schema_type == "null":
            return "null"
        
        # Handle union types (anyOf, oneOf)
        if "anyOf" in schema or "oneOf" in schema:
            union_key = "anyOf" if "anyOf" in schema else "oneOf"
            union_types = [self._resolve_type(sub_schema) for sub_schema in schema[union_key]]
            # Remove duplicates while preserving order
            unique_types = list(dict.fromkeys(union_types))
            return " | ".join(unique_types)
        
        # Handle array types
        if schema_type == "array":
            items_schema = schema.get("items", {})
            items_type = self._resolve_type(items_schema)
            return f"{items_type}[]"
        
        # Handle object types
        if schema_type == "object":
            return "Record<string, any>"  # Generic object type
        
        # Handle enum types
        if "enum" in schema:
            enum_values = schema["enum"]
            if all(isinstance(v, str) for v in enum_values):
                return " | ".join(f'"{v}"' for v in enum_values)
            else:
                return " | ".join(str(v) for v in enum_values)
        
        # Handle basic types
        type_mapping = {
            "string": "string",
            "integer": "number",
            "number": "number",
            "boolean": "boolean",
        }
        
        if schema_type in type_mapping:
            return type_mapping[schema_type]
        
        # Handle format-specific string types
        if schema_type == "string":
            format_type = schema.get("format")
            if format_type in ("email", "uri", "uuid", "date", "datetime", "time"):
                return "string"  # All these formats are strings in TypeScript
        
        return "any"  # Fallback for unknown types


def discover_pydantic_models(schemas_path: Path) -> List[Any]:
    """Discover all Pydantic models in the schemas directory."""
    models = []
    
    if not schemas_path.exists():
        return models
    
    # Add the backend directory to the Python path
    backend_path = schemas_path.parent.parent.parent
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    
    # Look for Python files in the schemas directory
    for py_file in schemas_path.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        
        try:
            # Import the module
            spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find all Pydantic models in the module
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        hasattr(obj, 'model_json_schema') and
                        hasattr(obj, '__module__') and 
                        obj.__module__ == module.__name__):
                        # This is a Pydantic model defined in this module
                        models.append((name, obj))
        
        except Exception as e:
            print(f"⚠️  Warning: Could not import {py_file}: {e}")
            continue
    
    return models


def generate_typescript_types(schemas_path: Path, output_path: Path) -> bool:
    """Generate TypeScript types from Pydantic schemas."""
    try:
        # Discover Pydantic models
        models = discover_pydantic_models(schemas_path)
        
        if not models:
            # Create empty types file
            empty_content = generate_empty_types_file()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(empty_content)
            print("⚠️  No Pydantic models found. Created empty types file.")
            return True
        
        print(f"🔍 Found {len(models)} Pydantic models")
        
        # Generate TypeScript interfaces
        generator = TypeScriptGenerator()
        interfaces = []
        
        for model_name, model_class in models:
            try:
                # Generate JSON schema from Pydantic model
                schema = model_class.model_json_schema()
                
                # Generate TypeScript interface
                interface = generator.json_schema_to_typescript(schema, model_name)
                interfaces.append(interface)
                
                print(f"✅ Generated interface for {model_name}")
            
            except Exception as e:
                print(f"⚠️  Warning: Could not generate interface for {model_name}: {e}")
                continue
        
        if not interfaces:
            # Create empty types file
            empty_content = generate_empty_types_file()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(empty_content)
            print("⚠️  No interfaces generated. Created empty types file.")
            return True
        
        # Generate the complete TypeScript file
        content = generate_typescript_file(interfaces)
        
        # Write to output file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)
        
        print(f"✅ Successfully generated TypeScript types at {output_path}")
        return True
    
    except Exception as e:
        print(f"❌ Error generating TypeScript types: {e}")
        return False


def generate_empty_types_file() -> str:
    """Generate an empty types file for when no schemas are found."""
    return f"""/* eslint-disable */
/* tslint:disable */
/**
 * AUTO-GENERATED FILE - DO NOT EDIT
 * This file is automatically generated from Pydantic schemas.
 * Run 'make types' from the root to regenerate.
 * Generated at: {datetime.now().isoformat()}
 */

// No Pydantic models found to generate types from
export type EmptySchemas = Record<string, never>;

/**
 * Placeholder type that can be used when no schemas are available
 */
export interface ApiResponse<T = any> {{
  data?: T;
  message?: string;
  error?: string;
}}
"""


def generate_typescript_file(interfaces: List[str]) -> str:
    """Generate the complete TypeScript file content."""
    header = f"""/* eslint-disable */
/* tslint:disable */
/**
 * AUTO-GENERATED FILE - DO NOT EDIT
 * This file is automatically generated from Pydantic schemas.
 * Run 'make types' from the root to regenerate.
 * Generated at: {datetime.now().isoformat()}
 */

"""
    
    content = header + "\n\n".join(interfaces) + "\n"
    return content


def main():
    """Main function to generate TypeScript types."""
    if len(sys.argv) < 3:
        print("Usage: python generate_types_robust.py <schemas_path> <output_path>")
        return 1
    
    schemas_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    print(f"🔄 Generating TypeScript types...")
    print(f"   Schemas: {schemas_path}")
    print(f"   Output:  {output_path}")
    
    success = generate_typescript_types(schemas_path, output_path)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())