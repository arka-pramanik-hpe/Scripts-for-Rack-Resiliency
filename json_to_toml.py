import json
import sys
from tomlkit import document, dumps, comment
from tomlkit.items import Whitespace

def json_to_toml(json_input, toml_output):
    """
    Convert a JSON file to a TOML file using tomlkit for pretty formatting.
    
    The output includes a header comment and nicely formatted tables.
    """
    try:
        # Load the JSON data
        with open(json_input, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create a TOML document
        doc = document()
        # Add a header comment
        doc.add(comment("Converted from JSON to TOML using tomlkit"))
        # Append a newline as a Whitespace item for better readability
        doc.append(Whitespace("\n"))
        
        # Add the JSON data into the TOML document.
        # tomlkit converts nested dicts into nested tables automatically.
        for key, value in data.items():
            doc.add(key, value)
        
        # Generate the pretty-printed TOML string
        toml_str = dumps(doc)
        
        # Write the TOML string to the output file
        with open(toml_output, 'w', encoding='utf-8') as f:
            f.write(toml_str)
            
        print(f"Conversion successful: '{json_input}' -> '{toml_output}'")
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python json_to_toml.py <input.json> <output.toml>")
        sys.exit(1)
    
    json_input = sys.argv[1]
    toml_output = sys.argv[2]
    json_to_toml(json_input, toml_output)
