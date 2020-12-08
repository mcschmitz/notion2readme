import argparse
import shutil
import os
from notion.client import NotionClient
from notion2md.exporter import PageBlockExporter

parser = argparse.ArgumentParser()

parser.add_argument("--token_v2", type=str)

parser.add_argument("--url", type=str)

args = parser.parse_args()

OUTPUT_FOLDER = './README/'


class GitHubPageBlockExporter(PageBlockExporter):
    def __init__(self, url, client, blog_mode):
        super().__init__(url=url,client=client, blog_mode=blog_mode)
        if not self.bmode:
            self.file_name = self.page.title
            self.md = f"# {self.page.title} \n\n"


def export_notion(token_v2="", url=""):
    if not (os.path.isdir(OUTPUT_FOLDER)):
        os.makedirs(os.path.join(OUTPUT_FOLDER))
    client = NotionClient(token_v2=token_v2)
    exporter = GitHubPageBlockExporter(url, client, blog_mode=False)
    exporter.create_main_folder(OUTPUT_FOLDER)
    exporter.create_file()
    export(exporter)


def find_markdown(directory: str):
    for root, _dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file = os.path.join(root, file)
            _filename, file_extension = os.path.splitext(file)
            if file_extension == ".md":
                return file


def export(exporter):
    """Recursively export page block with its sub pages

        Args:
            exporter(PageBlockExporter()): export page block
    """
    exporter.page2md()
    exporter.write_file()
    for sub_exporter in exporter.sub_exporters:
        export(sub_exporter)


if __name__ == '__main__':
    export_notion(args.token_v2, args.url)

    md_path = find_markdown(directory=OUTPUT_FOLDER)
    shutil.move(md_path, "ReadMe.md")
