import html
import re

# Private-use code points: never appear in normal text and Markdown passes them through untouched.
# (Python-Markdown itself uses \x02/\x03 for its placeholders, so we avoid those.)
_START, _END = '\ue000', '\ue001'
_PLACEHOLDER = re.compile(_START + r'(\d+)' + _END)

_FENCE = re.compile(r'(?m)^(`{3,}|~{3,}).*\n(?:.*\n)*?\1[ \t]*$')


def protect_math(source):
    """Replace $...$ / $$...$$ spans with opaque placeholders so Markdown can't mangle them.

    A delimiter only closes the span at brace depth 0, so `$$ \\text{the variable $x$} $$` works.
    Fenced code blocks and inline code spans are left untouched.
    """
    stash = []
    out = []
    i, n = 0, len(source)

    def placeholder(math):
        stash.append(math)
        return f'{_START}{len(stash) - 1}{_END}'

    while i < n:
        # fenced code block at start of line: copy verbatim
        if i == 0 or source[i - 1] == '\n':
            m = _FENCE.match(source, i)
            if m:
                out.append(m.group())
                i = m.end()
                continue
        c = source[i]
        if c == '\\' and i + 1 < n:          # escaped char (e.g. \$) outside math
            out.append(source[i:i + 2])
            i += 2
        elif c == '`':                        # inline code span: copy up to matching backtick run
            run = re.match(r'`+', source[i:]).group()
            end = source.find(run, i + len(run))
            end = n if end == -1 else end + len(run)
            out.append(source[i:end])
            i = end
        elif c == '$':
            delim = '$$' if source.startswith('$$', i) else '$'
            end = _find_close(source, i + len(delim), delim)
            if end is None:
                out.append(c)
                i += 1
            else:
                out.append(placeholder(source[i:end + len(delim)]))
                i = end + len(delim)
        else:
            out.append(c)
            i += 1
    return ''.join(out), stash


def _find_close(s, j, delim):
    depth = 0
    while j < len(s):
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        elif depth <= 0 and s.startswith(delim, j):
            # a lone $ must not be the first half of $$
            if delim == '$' and s.startswith('$$', j):
                return None
            return j
        elif delim == '$' and c == '\n' and s.startswith('\n', j + 1):
            return None                       # inline math doesn't span paragraphs
        j += 1
    return None


def restore_math(html_text, stash):
    return _PLACEHOLDER.sub(lambda m: html.escape(stash[int(m.group(1))], quote=False), html_text)
