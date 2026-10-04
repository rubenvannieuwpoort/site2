from bs4 import BeautifulSoup
from gitdiff import diff_for_commit_message
from diffrender import render


def render_commit(element, front_matter):
    msg = element.get("msg", "")
    side_by_side = element.get("side-by-side", None) == ""
    diff = diff_for_commit_message(front_matter['repository'], msg)
    return render(diff, side_by_side=side_by_side)


RENDERERS = {
    "commit": render_commit,
}

def postprocess(html: str, front_matter) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for element in list(soup.find_all()):
        render = RENDERERS.get(element.name.lower())
        if render:
            rendered = render(element, front_matter)

            replacement = BeautifulSoup(rendered, "html.parser")
            element.replace_with(*replacement.contents)

    return str(soup)
