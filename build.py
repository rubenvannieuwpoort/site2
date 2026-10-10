import os
import shutil
import markdown
import re
import jinja2
import json

from postprocess import postprocess
from katexmath import KatexMathExtension


BUILD_FOLDER = './build'
WORK_FOLDER = './work'
CONTENT_FOLDER = './content'
TEMPLATES_FOLDER = './templates'
ASSETS_FOLDER = './assets'

POSTS_SUBPATH = 'posts'
WIP_SUBPATH = 'wip'

# EXCLUDED_FOLDERS = ['templates', '.git', '.venv', 'build', '__pycache__']

POST_TEMPLATE = 'post.html'
INDEX_TEMPLATE = 'index.html'

EXTENSIONS = [
    "def_list",             # https://python-markdown.github.io/extensions/definition_lists
    "fenced_code",          # https://python-markdown.github.io/extensions/fenced_code_blocks
    "footnotes",            # https://python-markdown.github.io/extensions/footnotes
    "md_in_html",           # https://python-markdown.github.io/extensions/md_in_html
    "sane_lists",           # https://python-markdown.github.io/extensions/sane_lists
    "smarty",               # https://python-markdown.github.io/extensions/smarty
    "admonition",           # https://python-markdown.github.io/extensions/admonition
    KatexMathExtension(),   # katexmath.py: renders $...$, \(...\), $$...$$ and \[...\] with KaTeX
]

env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_FOLDER))


LIST_ITEM = re.compile(r'- |\d+\. ')

# hack to allow lists without a leading empty line: insert one before the first
# item of a list, but not between items (that would make the list loose)
def add_blank_lines_before_lists(source):
    lines = []
    in_list = False
    for line in source.split('\n'):
        if LIST_ITEM.match(line):
            if not in_list and lines and lines[-1] and not lines[-1].startswith('`'):
                lines.append('')
            in_list = True
        elif not line:
            in_list = False
        lines.append(line)
    return '\n'.join(lines)


def build(file, output_folder, front_matters):
    filename = os.path.splitext(os.path.basename(file))[0]

    with open(file, 'r') as f:
        input = f.read()

    # extract front matter
    front_matter, idx = json.JSONDecoder().raw_decode(input)
    front_matter['link'] = f'{output_folder}/{filename}'

    front_matters.append(front_matter)
    source = input[idx:].lstrip('\n')

    source = add_blank_lines_before_lists(source)

    content = markdown.markdown(source, extensions=EXTENSIONS)
    content = postprocess(content, front_matter)

    template = env.get_template(POST_TEMPLATE)
    result = template.render(content = content, **front_matter)

    os.makedirs(os.path.join(BUILD_FOLDER, output_folder), exist_ok=True)
    with open(os.path.join(BUILD_FOLDER, f'{output_folder}/{filename}.html'), 'w') as f:
        f.write(result)


def main():
    front_matters = []

    # build HTML for articles
    for entry in os.scandir(CONTENT_FOLDER):
        try:
            build(entry.path, POSTS_SUBPATH, front_matters)
        except:
            raise Exception(f'during processing of {entry.name}')

    for entry in os.scandir(WORK_FOLDER):
        try:
            build(entry.path, WIP_SUBPATH, [])
        except:
            raise Exception(f'during processing of {entry.name}')

    # create the index
    template = env.get_template(INDEX_TEMPLATE)

    front_matters.sort(key=lambda fm: fm['date'], reverse=True)
    years = list(reversed(range(int(front_matters[-1]['date'][:4]), int(front_matters[0]['date'][:4]) + 1)))
    front_matters_per_year = {year: [] for year in years}
    [front_matters_per_year[int(fm['date'][:4])].append(fm) for fm in front_matters]

    result = template.render(years=years, front_matters_per_year=front_matters_per_year)
    with open(os.path.join(BUILD_FOLDER, 'index.html'), 'w') as f:
        f.write(result)

    # copy the assets to the build folder
    shutil.copytree(ASSETS_FOLDER, BUILD_FOLDER, dirs_exist_ok=True)


if __name__ == '__main__':
    main()
