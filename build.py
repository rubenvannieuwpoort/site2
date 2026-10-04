import os
import shutil
import markdown
import re
import jinja2
import json

from postprocess import postprocess
from mathprotect import protect_math, restore_math


BUILD_FOLDER = './build'
CONTENT_FOLDER = './content'
TEMPLATES_FOLDER = './templates'
ASSETS_FOLDER = './assets'

# EXCLUDED_FOLDERS = ['templates', '.git', '.venv', 'build', '__pycache__']

POST_TEMPLATE = "post.html"

EXTENSIONS = [
    "def_list",             # https://python-markdown.github.io/extensions/definition_lists
    "fenced_code",          # https://python-markdown.github.io/extensions/fenced_code_blocks
    "footnotes",            # https://python-markdown.github.io/extensions/footnotes
    "md_in_html",           # https://python-markdown.github.io/extensions/md_in_html
    "sane_lists",           # https://python-markdown.github.io/extensions/sane_lists
    "smarty",               # https://python-markdown.github.io/extensions/smarty
    "admonition",           # https://python-markdown.github.io/extensions/admonition
]

env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_FOLDER))


def build(file):
    name = os.path.splitext(os.path.basename(file))[0]

    with open(file, 'r') as f:
        input = f.read()

    # extract front matter
    front_matter, idx = json.JSONDecoder().raw_decode(input)
    source = input[idx:].lstrip('\n')

    # hide math from Markdown so it doesn't mangle backslash escapes, `_`, `*`, etc.
    source, math = protect_math(source)

    # hack to allow lists without a leading empty line
    source = re.sub(r'(?m)^([^\n`].*)\n(?=- )', r'\1\n\n', source)

    content = markdown.markdown(source, extensions=EXTENSIONS)
    content = restore_math(content, math)
    content = postprocess(content, front_matter)

    template = env.get_template(POST_TEMPLATE)
    result = template.render(content = content, **front_matter)

    os.makedirs(BUILD_FOLDER, exist_ok=True)
    with open(os.path.join(BUILD_FOLDER, f'{name}.html'), 'w') as f:
        f.write(result)


def main():
    # build HTML for articles
    for entry in os.scandir(CONTENT_FOLDER):
        # if entry.is_dir() and entry.name not in EXCLUDED_FOLDERS:
        build(entry.path)

    # copy the assets to the build folder
    shutil.copytree(ASSETS_FOLDER, BUILD_FOLDER, dirs_exist_ok=True)
    


if __name__ == '__main__':
    main()
