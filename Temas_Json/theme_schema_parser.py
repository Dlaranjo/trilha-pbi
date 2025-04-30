import json
import os
import csv
from typing import Dict, List, Optional, Any
from pathlib import Path

class SchemaParser:
    def __init__(self, schema_path: str):
        self.schema_path = schema_path
        self.schema_data = None
        self.rows = []
        
    def load_schema(self) -> None:
        """Load the schema JSON file"""
        if not os.path.exists(self.schema_path):
            raise FileNotFoundError(f"Schema file not found at: {self.schema_path}")
            
        with open(self.schema_path, 'r', encoding='utf-8') as f:
            self.schema_data = json.load(f)
            
        if not self.schema_data:
            raise ValueError("Failed to load schema data")
            
        # Debug: Print top-level keys
        print("\nTop-level keys in schema:")
        print(list(self.schema_data.keys()))
        
        # Debug: Print definitions keys
        if 'definitions' in self.schema_data:
            print("\nDefinitions keys:")
            print(list(self.schema_data['definitions'].keys()))
    
    def get_expected_type(self, data: Dict[str, Any]) -> str:
        """Determine the expected type of a property"""
        if not isinstance(data, dict):
            return ''
            
        # Check for explicit type
        if 'type' in data:
            if isinstance(data['type'], list):
                return ', '.join(data['type'])
            return data['type']
            
        # Check for format
        if 'format' in data:
            return data['format']
            
        # Check for const or enum to infer type
        if 'const' in data:
            return type(data['const']).__name__
        if 'enum' in data and data['enum']:
            return type(data['enum'][0]).__name__
            
        # Check for oneOf with const values
        if 'oneOf' in data:
            types = set()
            for item in data['oneOf']:
                if isinstance(item, dict) and 'const' in item:
                    types.add(type(item['const']).__name__)
            if types:
                return ', '.join(types)
                
        # Check for patternProperties or additionalProperties
        if 'patternProperties' in data or 'additionalProperties' in data:
            return 'object'
            
        # Check for items to infer array type
        if 'items' in data:
            if isinstance(data['items'], dict):
                return f"array of {self.get_expected_type(data['items'])}"
            return 'array'
            
        return ''
    
    def extract_enum_values(self, data: Dict[str, Any]) -> str:
        """Extract enum values from a property definition"""
        if isinstance(data, dict):
            # Handle references first
            if '$ref' in data:
                ref_data = self.resolve_reference(data['$ref'])
                if ref_data:
                    # If the reference is to a color definition
                    if data['$ref'] == '#/definitions/color':
                        return "Expected type: color"
                    return self.extract_enum_values(ref_data)
            
            if 'enum' in data:
                return ', '.join(str(v) for v in data['enum'])
            if 'anyOf' in data:
                enums = []
                for item in data['anyOf']:
                    if isinstance(item, dict) and 'enum' in item:
                        enums.extend(item['enum'])
                if enums:
                    return ', '.join(str(v) for v in enums)
            if 'oneOf' in data:
                enums = []
                for item in data['oneOf']:
                    if isinstance(item, dict) and 'const' in item:
                        enums.append(item['const'])
                if enums:
                    return ', '.join(str(v) for v in enums)
                    
            # If no enum values, return the expected type
            expected_type = self.get_expected_type(data)
            if expected_type:
                return f"Expected type: {expected_type}"
                
        return ''
    
    def resolve_reference(self, ref: str) -> Dict[str, Any]:
        """Resolve a JSON reference to its actual definition"""
        if not ref.startswith('#'):
            return {}
        
        path = ref.split('/')[1:]  # Remove the '#' and split
        current = self.schema_data
        
        for key in path:
            if key in current:
                current = current[key]
            else:
                return {}
        
        return current if isinstance(current, dict) else {}
    
    def process_property(self, visual_name: str, prop_name: str, prop_data: Dict[str, Any], path: List[str] = None) -> None:
        """Process a single property and its possible values"""
        if path is None:
            path = []
            
        # Skip wildcard properties
        if prop_name == '*':
            return
            
        current_path = path + [prop_name]
        
        # Handle references
        if isinstance(prop_data, dict):
            if '$ref' in prop_data:
                ref_data = self.resolve_reference(prop_data['$ref'])
                if ref_data:
                    prop_data = ref_data
            
            # Extract property information
            description = prop_data.get('title', '')
            enum_values = self.extract_enum_values(prop_data)
            
            # Create property path without 'items'
            clean_path = [p for p in current_path if p != 'items']
            
            # Only add row if it has at least 2 levels
            if len(clean_path) >= 2:
                row = {
                    'visual_name': visual_name.replace('visual-', ''),  # Remove visual- prefix
                    'property_category': clean_path[0],
                    'property_name': '.'.join(clean_path[1:]),
                    'property_description': description if description else "Color",
                    'property_values': enum_values if enum_values else "Expected type: color"  # Replace empty values with color
                }
                
                self.rows.append(row)
            
            # Process nested properties
            if 'properties' in prop_data:
                for nested_name, nested_data in prop_data['properties'].items():
                    self.process_property(visual_name, nested_name, nested_data, current_path)
            
            # Process items if it's an object
            if 'items' in prop_data and isinstance(prop_data['items'], dict):
                # Process items properties directly
                for item_name, item_data in prop_data['items'].get('properties', {}).items():
                    self.process_property(visual_name, item_name, item_data, current_path)
            
            # Process patternProperties
            if 'patternProperties' in prop_data:
                for pattern, pattern_data in prop_data['patternProperties'].items():
                    self.process_property(visual_name, f'pattern:{pattern}', pattern_data, current_path)
            
            # Process additionalProperties
            if 'additionalProperties' in prop_data and isinstance(prop_data['additionalProperties'], dict):
                self.process_property(visual_name, 'additionalProperties', prop_data['additionalProperties'], current_path)
    
    def process_visual_definition(self, visual_name: str, def_data: Dict[str, Any]) -> None:
        """Process a visual definition and all its properties"""
        if not isinstance(def_data, dict):
            return
            
        # Handle references in the definition
        if '$ref' in def_data:
            ref_data = self.resolve_reference(def_data['$ref'])
            if ref_data:
                def_data = ref_data
        
        # Process allOf if present
        if 'allOf' in def_data:
            for item in def_data['allOf']:
                if isinstance(item, dict):
                    if '$ref' in item:
                        ref_data = self.resolve_reference(item['$ref'])
                        if ref_data:
                            self.process_visual_definition(visual_name, ref_data)
                    else:
                        self.process_visual_definition(visual_name, item)
        
        # Process properties if they exist
        if 'properties' in def_data:
            for prop_name, prop_data in def_data['properties'].items():
                # If the property is an object, process its properties
                if isinstance(prop_data, dict) and 'properties' in prop_data:
                    for nested_name, nested_data in prop_data['properties'].items():
                        self.process_property(visual_name, nested_name, nested_data, [prop_name])
                else:
                    self.process_property(visual_name, prop_name, prop_data)
        
        # Process patternProperties
        if 'patternProperties' in def_data:
            for pattern, pattern_data in def_data['patternProperties'].items():
                self.process_property(visual_name, f'pattern:{pattern}', pattern_data)
        
        # Process additionalProperties
        if 'additionalProperties' in def_data and isinstance(def_data['additionalProperties'], dict):
            self.process_property(visual_name, 'additionalProperties', def_data['additionalProperties'])
    
    def parse_definitions(self) -> None:
        """Parse definitions from the schema"""
        if not self.schema_data:
            raise ValueError("Schema not loaded. Call load_schema() first.")
            
        definitions = self.schema_data.get('definitions', {})
        
        # Process each definition
        for def_name, def_data in definitions.items():
            # Only process visual definitions
            if not def_name.startswith('visual-'):
                continue
                
            print(f"\nProcessing visual: {def_name}")
            self.process_visual_definition(def_name, def_data)
    
    def export_to_csv(self, output_path: str) -> None:
        """Export the parsed schema to a CSV file"""
        # Create fieldnames with optimized names for DataFrames
        fieldnames = [
            'visual_name',
            'property_category',
            'property_name',
            'property_description',
            'property_values'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.rows)

def main():
    try:
        # Get the directory of the current script
        script_dir = Path(__file__).parent
        print(f"Script directory: {script_dir}")
        
        # Path to the schema file
        schema_path = script_dir / "reportThemeSchema-2.140.json"
        print(f"Looking for schema at: {schema_path}")
        
        # Create parser instance
        parser = SchemaParser(str(schema_path))
        
        # Load and parse the schema
        print("\nLoading schema...")
        parser.load_schema()
        
        print("\nParsing definitions...")
        parser.parse_definitions()
        
        # Export to CSV
        output_path = script_dir / "theme_schema_documentation.csv"
        print(f"\nExporting to CSV: {output_path}")
        parser.export_to_csv(str(output_path))
        
        print("\nExport completed successfully!")
        print(f"CSV file created at: {output_path}")
        print(f"Total properties found: {len(parser.rows)}")
        
        if len(parser.rows) == 0:
            print("\nWarning: No properties were found.")
            print("This might indicate that the schema structure is different than expected.")
            print("Please check the schema file structure.")
        else:
            print("\nYou can now import this CSV file into Power BI for analysis.")
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 