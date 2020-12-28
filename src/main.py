import argparse
import os
import shutil

from notion.client import NotionClient
from notion_exporter import GitHubPageBlockExporter

parser = argparse.ArgumentParser()

parser.add_argument("--token_v2", type=str)

parser.add_argument("--url", type=str)

args = parser.parse_args()

OUTPUT_FOLDER = "./.README/"


def export_notion(token_v2, url):
    """
    Exports Notion Page.

    Args:
        token_v2: Notion Token V2
        url: URL to Notion Page
    """
    if not (os.path.isdir(OUTPUT_FOLDER)):
        os.makedirs(os.path.join(OUTPUT_FOLDER))
    client = NotionClient(token_v2=token_v2)
    exporter = GitHubPageBlockExporter(url, client, OUTPUT_FOLDER)
    export(exporter)


def find_markdown(directory: str) -> str:
    """
    Searches for the first Markdown in a directory.

    Args:
        directory: Directory to crawl
    """
    for root, _dirs, files in os.walk(directory, topdown=True):
        for file in files:
            file = os.path.join(root, file)
            _filename, file_extension = os.path.splitext(file)
            if file_extension == ".md":
                return file


def export(exporter):
    """
    Recursively export page block with its sub pages.

    Args:
        exporter: GitHubPageBlockExporter
    """
    exporter.page2md()
    exporter.write_file()
    for sub_exporter in exporter.sub_exporters:
        export(sub_exporter)


if __name__ == "__main__":
    export_notion(args.token_v2, args.url)

    md_path = find_markdown(directory=OUTPUT_FOLDER)
    shutil.move(md_path, "README.md")
