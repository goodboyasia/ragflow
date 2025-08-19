#!/usr/bin/env python3
"""
HTML Parser Example

This script demonstrates how to use RAGFlowHtmlParser to parse HTML content from:
1. A URL (by fetching the content)
2. A local HTML file
3. HTML text directly

Usage:
    python html_parser_example.py [--url URL] [--file FILE] [--text TEXT]

Examples:
    python html_parser_example.py --url "https://example.com"
    python html_parser_example.py --file "./sample.html"
    python html_parser_example.py --text "<html><head><title>Test</title></head><body><p>Hello World</p></body></html>"
"""

import argparse
import requests
from deepdoc.parser.html_parser import RAGFlowHtmlParser


def parse_url(url):
    """Fetch and parse HTML content from a URL"""
    print(f"Fetching content from URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html_content = response.text
        parser = RAGFlowHtmlParser()
        sections = parser.parser_txt(html_content)
        return sections
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return None


def parse_file(file_path):
    """Parse HTML content from a local file"""
    print(f"Parsing HTML file: {file_path}")
    try:
        parser = RAGFlowHtmlParser()
        sections = parser(file_path)
        return sections
    except Exception as e:
        print(f"Error parsing file: {e}")
        return None


def parse_text(html_text):
    """Parse HTML content from text"""
    print("Parsing HTML text")
    try:
        parser = RAGFlowHtmlParser()
        sections = parser.parser_txt(html_text)
        return sections
    except Exception as e:
        print(f"Error parsing HTML text: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="RAGFlow HTML Parser Example")
    parser.add_argument("--url", help="URL to fetch and parse")
    parser.add_argument("--file", help="Path to local HTML file to parse")
    parser.add_argument("--text", help="HTML text to parse directly")

    args = parser.parse_args()
    args.url = "https://ragflow.io/docs/dev/build_docker_image"
    args.url = "https://blog.csdn.net/zzq1989_/article/details/148395624"
    if args.url:
        sections = parse_url(args.url)
    elif args.file:
        sections = parse_file(args.file)
    elif args.text:
        sections = parse_text(args.text)
    else:
        # Default example with a simple HTML
        sample_html = """
        <html>
        <head><title>Sample Page</title></head>
        <body>
        <h1>Welcome to RAGFlow</h1>
        <p>RAGFlow is an open-source RAG (Retrieval-Augmented Generation) engine based on deep document understanding.</p>
        <p>It offers a streamlined RAG workflow for businesses of any scale.</p>
        </body>
        </html>
        """
        print("Parsing sample HTML content:")
        sections = parse_text(sample_html)

    if sections:
        print("\nParsed sections:")
        print("-" * 40)
        for i, section in enumerate(sections, 1):
            if section.strip():  # Only print non-empty sections
                print(f"{i}. {section.strip()}")


if __name__ == "__main__":
    main()