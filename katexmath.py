"""Python-Markdown extension that renders LaTeX math to HTML with KaTeX at build time.

Supported delimiters:

    $...$    \\(...\\)    inline math
    $$...$$  \\[...\\]    display math

A closing delimiter only counts at brace depth 0, so `$$ \\text{the variable $x$} $$` works.
A backslash-escaped dollar (`\\$`) is a literal dollar sign. Code spans and code blocks are left alone.

Usage:

    markdown.markdown(source, extensions=[KatexMathExtension()])
"""

import re
import xml.etree.ElementTree as etree

import pykatex
from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.inlinepatterns import InlineProcessor
from markdown.util import STX


CLOSERS = {'$': '$', '$$': '$$', '\\(': '\\)', '\\[': '\\]'}
DISPLAY = {'$$', '\\['}

# an opening delimiter that isn't escaped with a backslash
OPEN_RE = r'(?<!\\)(?:\$\$?|\\[(\[])'


def find_close(s, j, close):
    """Return the index of the closing delimiter `close` in `s`, starting at `j`, or None."""
    depth = 0
    while j < len(s):
        if depth <= 0 and s.startswith(close, j):
            # a lone $ must not be the first half of $$
            if close == '$' and s.startswith('$$', j):
                return None
            return j
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        elif close == '$' and s.startswith('\n\n', j):
            return None     # inline math doesn't span paragraphs
        j += 1
    return None


def render(math, display):
    try:
        return pykatex.renderToString(math, displayMode=display, output='html')
    except pykatex.ParseError as e:
        raise ValueError(f'KaTeX could not render {math!r}: {e}') from e


class InlineMathProcessor(InlineProcessor):
    """Math inside running text, in any of the four delimiter styles."""

    def handleMatch(self, m, data):
        opener = m.group(0)
        close = CLOSERS[opener]
        end = find_close(data, m.end(), close)
        if end is None:
            return None, None, None
        math = data[m.end():end]
        # an inline placeholder (e.g. a code span) inside means this wasn't really math
        if not math.strip() or STX in math:
            return None, None, None
        html = render(math, opener in DISPLAY)
        return self.md.htmlStash.store(html), m.start(), end + len(close)


class DisplayMathProcessor(BlockProcessor):
    """Display math that starts a block.

    Handled at block level so the contents (which may span several lines) are never mistaken
    for lists, headings, quotes, etc. Display math in the middle of a paragraph is picked up
    by `InlineMathProcessor` instead.
    """

    START_RE = re.compile(r'\s*(\$\$|\\\[)')

    def test(self, parent, block):
        return self.START_RE.match(block) is not None

    def run(self, parent, blocks):
        m = self.START_RE.match(blocks[0])
        close = CLOSERS[m.group(1)]

        # the math may contain blank lines, so it can span several blocks
        source = blocks[0]
        end = find_close(source, m.end(), close)
        n = 1
        while end is None and n < len(blocks):
            source += '\n\n' + blocks[n]
            end = find_close(source, m.end(), close)
            n += 1
        if end is None:
            return False    # no closing delimiter: let the other processors have it

        del blocks[:n]
        rest = source[end + len(close):].lstrip()
        if rest:
            blocks.insert(0, rest)

        p = etree.SubElement(parent, 'p')
        p.text = self.parser.md.htmlStash.store(render(source[m.end():end], True))


class KatexMathExtension(Extension):
    def extendMarkdown(self, md):
        # between 'code' (80) and 'hashheader' (70): indented code stays code, but lines inside
        # display math are never parsed as headings, lists, quotes, etc.
        md.parser.blockprocessors.register(DisplayMathProcessor(md.parser), 'katex_display', 75)
        # after 'backtick' (190) so code spans win, before 'escape' (180) so `\(`, `\[` survive
        md.inlinePatterns.register(InlineMathProcessor(OPEN_RE, md), 'katex_inline', 185)


def makeExtension(**kwargs):
    return KatexMathExtension(**kwargs)
