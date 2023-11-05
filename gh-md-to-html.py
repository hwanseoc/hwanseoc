# usage: python3 gh-md-to-html.py readme.md readme.html

import argparse
import requests

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file name", type=str)
    parser.add_argument("output", help="Output file name", type=str)
    parser.add_argument("-m", "--mode", help="Markdown rendering mode (markdown or gfm)", choices=["markdown", "gfm"], default="markdown")
    parser.add_argument("-c", "--context", help="Repository context when rendering in gfm mode", type=str)
    args = parser.parse_args()

    if args.context and args.mode == "markdown":
        raise ValueError("[ERROR] Cannot apply context in markdown mode. Remove context or switch to gfm mode.")

    md = read_file(args.input)

    payload = {"text": md, "mode": args.mode}
    if args.context:
        payload["context"] = args.context

    response = requests.post("https://api.github.com/markdown", json=payload)

    if response.ok:
        html = response.text
    else:
        raise requests.exceptions.HTTPError(f"[ERROR][HTTP {response.status_code}] {response.json()}")

    write_file(args.output, html)

if __name__ == "__main__":
    main()
