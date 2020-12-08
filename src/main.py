import argparse
import notion2md
import os
import shutil

parser = argparse.ArgumentParser()

parser.add_argument("--token_v2", type=str)

parser.add_argument("--url", type=str)

args = parser.parse_args()


def find_markdown(directory: str):
    yaml_files = []
    for root, _dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file = os.path.join(root, file)
            _filename, file_extension = os.path.splitext(file)
            if file_extension == ".md":
                yaml_files.append(file)
    if len(yaml_files) == 1:
        return yaml_files[0]
    elif len(yaml_files) > 1:
        raise ValueError("Multiple Markdown files found")
    else:
        raise ValueError("No config Mardown found")


if __name__ == '__main__':
    notion2md.export_cli(args.token_v2, args.url, bmode=0)
    md_path = find_markdown(directory="notion2md_output")
    shutil.move(md_path, "README.md")
