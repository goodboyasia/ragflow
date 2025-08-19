#!/usr/bin/env python3
"""
JSON Parser Example

This script demonstrates how to use RAGFlowJsonParser to parse JSON content from:
1. JSON strings
2. JSONL content
3. Binary data

Usage:
    python json_parser_example.py [--json JSON_STRING] [--jsonl JSONL_STRING] [--file FILE_PATH]

Examples:
    python json_parser_example.py --json '{"name": "John", "age": 30}'
    python json_parser_example.py --jsonl '{"name": "John"}\n{"age": 30}'
    python json_parser_example.py --file "./sample.json"
"""

import argparse
import json
import sys
import os

# Add the project root to the path so we can import the parser
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from deepdoc.parser.json_parser import RAGFlowJsonParser


def parse_json_string(json_string):
    """Parse JSON string content"""
    print("Parsing JSON string:")
    print(f"Input: {json_string}")
    
    try:
        # Create parser instance
        parser = RAGFlowJsonParser()
        
        # Parse the JSON string
        sections = parser._parse_json(json_string)
        
        print(f"\nParsed into {len(sections)} section(s):")
        print("-" * 50)
        for i, section in enumerate(sections, 1):
            print(f"Section {i}:")
            print(section)
            # Try to parse it back to show it's valid JSON
            try:
                parsed = json.loads(section)
                print(f"Valid JSON with {len(str(parsed))} characters")
            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}")
            print()
            
        return sections
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return None


def parse_jsonl_string(jsonl_string):
    """Parse JSONL string content"""
    print("Parsing JSONL string:")
    print("Input:")
    print(jsonl_string)
    
    try:
        # Create parser instance
        parser = RAGFlowJsonParser()
        
        # Parse the JSONL string
        sections = parser._parse_jsonl(jsonl_string)
        
        print(f"\nParsed into {len(sections)} section(s):")
        print("-" * 50)
        for i, section in enumerate(sections, 1):
            print(f"Section {i}:")
            print(section)
            # Try to parse it back to show it's valid JSON
            try:
                parsed = json.loads(section)
                print(f"Valid JSON with {len(str(parsed))} characters")
            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}")
            print()
            
        return sections
    except Exception as e:
        print(f"Error parsing JSONL: {e}")
        return None


def parse_file(file_path):
    """Parse JSON/JSONL file content"""
    print(f"Parsing file: {file_path}")
    
    try:
        # Read file content
        with open(file_path, 'rb') as f:
            binary_data = f.read()
        
        # Create parser instance
        parser = RAGFlowJsonParser()
        
        # Parse the binary data
        sections = parser(binary_data)
        
        print(f"\nParsed into {len(sections)} section(s):")
        print("-" * 50)
        for i, section in enumerate(sections, 1):
            print(f"Section {i}:")
            print(section)
            # Try to parse it back to show it's valid JSON
            try:
                parsed = json.loads(section)
                print(f"Valid JSON with {len(str(parsed))} characters")
            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}")
            print()
            
        return sections
    except Exception as e:
        print(f"Error parsing file: {e}")
        return None


def demonstrate_chunking():
    """Demonstrate JSON chunking with a large JSON object"""
    print("Demonstrating JSON chunking with large object:")
    
    # Create a large JSON object for testing chunking
    large_json = {
        "title": "Large JSON Document",
        "metadata": {
            "author": "Test User",
            "created": "2023-01-01",
            "version": "1.0"
        },
        "sections": [
            {
                "id": i,
                "title": f"Section {i}",
                "content": f"This is the content of section {i}. " * 50  # Make it long
            }
            for i in range(5)  # 5 sections
        ],
        "tags": ["test", "json", "chunking"] * 20  # Make it long
    }
    
    json_string = json.dumps(large_json, ensure_ascii=False)
    print(f"Original JSON size: {len(json_string)} characters")
    
    # Create parser with smaller chunk size for demonstration
    parser = RAGFlowJsonParser(max_chunk_size=500)
    
    # Parse with chunking
    sections = parser._parse_json(json_string)
    
    print(f"\nChunked into {len(sections)} section(s):")
    print("-" * 50)
    for i, section in enumerate(sections, 1):
        print(f"Section {i}: {len(section)} characters")
        # Show beginning and end of section
        if len(section) > 100:
            print(f"  {section[:50]}...{section[-50:]}")
        else:
            print(f"  {section}")
        print()


def demonstrate_jsonl_detection():
    """Demonstrate JSONL format detection"""
    print("Demonstrating JSONL format detection:")
    
    parser = RAGFlowJsonParser()
    
    # Test JSONL content
    jsonl_content = """{"name": "John", "age": 30}
{"name": "Jane", "age": 25, "city": "New York"}
{"product": "Widget", "price": 9.99, "in_stock": true}"""
    
    print("Testing JSONL content:")
    print("Content is JSONL:", parser.is_jsonl_format(jsonl_content))
    
    # Test regular JSON content
    json_content = """{
    "name": "John",
    "age": 30,
    "city": "New York"
}"""
    
    print("Testing regular JSON content:")
    print("Content is JSONL:", parser.is_jsonl_format(json_content))
    
    # Test plain text content
    text_content = """This is plain text
    Not JSON or JSONL"""
    
    print("Testing plain text content:")
    print("Content is JSONL:", parser.is_jsonl_format(text_content))
    print()


def main():
    parser = argparse.ArgumentParser(description="RAGFlow JSON Parser Example")
    parser.add_argument("--json", help="JSON string to parse")
    parser.add_argument("--jsonl", help="JSONL string to parse")
    parser.add_argument("--file", help="Path to JSON/JSONL file to parse")
    parser.add_argument("--demo", action="store_true", help="Run demonstrations")

    args = parser.parse_args()
    args.file = "./sample.json"
    # If no arguments provided, run a simple example
    if not any([args.json, args.jsonl, args.file, args.demo]):
        print("Running default examples...\n")
        
        # Simple JSON example
        simple_json = '{"name": "John Doe", "age": 35, "occupation": "Developer"}'
        parse_json_string(simple_json)
        
        print("\n" + "="*60 + "\n")
        
        # Simple JSONL example
        simple_jsonl = '{"name": "John"}\n{"age": 35}\n{"occupation": "Developer"}'
        parse_jsonl_string(simple_jsonl)
        
    else:
        if args.json:
            parse_json_string(args.json)
            
        if args.jsonl:
            parse_jsonl_string(args.jsonl)
            
        if args.file:
            parse_file(args.file)
            
        if args.demo:
            print("Running demonstrations...\n")
            demonstrate_chunking()
            print("\n" + "="*60 + "\n")
            demonstrate_jsonl_detection()


if __name__ == "__main__":
    main()