from unidiff.patch import PatchSet, PatchedFile, Hunk
import mydifflib
from diff_match_patch import diff_match_patch
import re
from difflib import SequenceMatcher


dmp = diff_match_patch()


def intersperse(iterable, delimiter):
    it = iter(iterable)

    try:
        yield next(it)
    except StopIteration:
        return

    for x in it:
        yield delimiter
        yield x


def diff_words_to_chars(text1, text2):
    word_array = [""]
    word_hash = {}

    # Order matters: whitespace, identifier characters, then everything else.
    token_re = re.compile(r"\s+|[A-Za-z0-9_]+|[^A-Za-z0-9_\s]+")

    def encode(text):
        chars = []

        for match in token_re.finditer(text):
            token = match.group(0)

            if token not in word_hash:
                word_hash[token] = len(word_array)
                word_array.append(token)

            chars.append(chr(word_hash[token]))

        return "".join(chars)

    chars1 = encode(text1)
    chars2 = encode(text2)

    return chars1, chars2, word_array


cruncher = SequenceMatcher()
def match_ratio(x, y):
    cruncher.set_seqs(x, y)
    return cruncher.ratio()

def diffjes(oldline, newline, wordlevel=True):
    if wordlevel:
        chars1, chars2, word_array = diff_words_to_chars(oldline, newline)
    else:
        chars1, chars2 = oldline, newline
        word_array = []

    dmpdiffs = dmp.diff_main(chars1, chars2, False)

    if wordlevel:
        dmp.diff_charsToLines(dmpdiffs, word_array)

    return dmpdiffs


def render_hunk(hunk: Hunk, side_by_side: bool):
    def maptuple(sfd: tuple[tuple[int | str, str], tuple[int | str, str], bool]):
        oldtuple, newtuple, changed = sfd
        if type(oldtuple[0]) is int:
            oldtuple = (oldtuple[0] + hunk.source_start - 1, oldtuple[1].replace('\0+','').replace('\0-','')\
                                                                        .replace('\0^','').replace('\1',''))
        else:
            oldtuple = None

        if type(newtuple[0]) is int:
            newtuple = (newtuple[0] + hunk.target_start - 1, newtuple[1].replace('\0+','').replace('\0-','')\
                                                                        .replace('\0^','').replace('\1',''))
        else:
            newtuple = None

        return oldtuple, newtuple, changed

    old = [line.value[:-1] for line in hunk if line.line_type in (' ', '-')]
    new = [line.value[:-1] for line in hunk if line.line_type in (' ', '+')]
    diffs: Iterator[tuple[tuple[int | str, str], tuple[int | str, str], bool]] = mydifflib._mdiff(old, new) # type: ignore
    linepairs: map[tuple[tuple[int, str] | None, tuple[int, str] | None, bool]] = map(maptuple, diffs)

    panea, paneb = [], []
    for (oldtuple, newtuple, changed) in linepairs:
        if not changed:
            assert oldtuple is not None and newtuple is not None
            (oldlineno, oldline), (newlineno, newline) = oldtuple, newtuple
            if side_by_side:
                panea.append(f'<span class="line"><span class="ln" data-a="{oldlineno}"></span>{oldline}</span>')
                paneb.append(f'<span class="line"><span class="ln" data-b="{newlineno}"></span>{newline}</span>')
            else:
                panea.append(f'<span class="line"><span class="ln" data-a="{oldlineno}" data-b="{newlineno}"></span>{oldline}</span>')
        else:
            if oldtuple is not None and newtuple is not None and match_ratio(oldtuple[1], newtuple[1]) > .8:
                (oldlineno, oldline), (newlineno, newline) = oldtuple, newtuple

                dmpdiffs = diffjes(oldline, newline)

                linea, lineb = '', ''
                for op, text in dmpdiffs:
                    if op == 0:
                        linea += text
                        lineb += text
                    elif op == -1:
                        linea += f'<span class="w">{text}</span>'
                    elif op == 1:
                        lineb += f'<span class="w">{text}</span>'

                if side_by_side:
                    panea.append(f'<span class="line del"><span class="ln" data-a="{oldlineno}"></span>{linea}</span>')
                    paneb.append(f'<span class="line add"><span class="ln" data-b="{newlineno}"></span>{lineb}</span>')
                else:
                    panea.append(f'<span class="line del"><span class="ln" data-a="{oldlineno}"></span>{linea}</span>')
                    panea.append(f'<span class="line add"><span class="ln" data-b="{newlineno}"></span>{lineb}</span>')
            else:
                if oldtuple is not None:
                    oldlineno, oldline = oldtuple
                    panea.append(f'<span class="line del"><span class="ln" data-a="{oldlineno}"></span>{oldline}</span>')
                else:
                    if side_by_side:
                        panea.append('<span class="line gap"><span class="ln" ></span></span>')

                if newtuple is not None:
                    newlineno, newline = newtuple
                    if side_by_side:
                        paneb.append(f'<span class="line add"><span class="ln" data-b="{newlineno}"></span>{newline}</span>')
                    else:
                        panea.append(f'<span class="line add"><span class="ln" data-b="{newlineno}"></span>{newline}</span>')
                else:
                    if side_by_side:
                        paneb.append('<span class="line gap"><span class="ln"></span></span>')

    if side_by_side:
        return f'<div class="pane a"><pre class="diff numbered"><code>{''.join(panea)}</code></pre></div><div class="pane b"><pre class="diff numbered"><code>{''.join(paneb)}</code></pre></div>'
    else:
        return ''.join(panea)


def generate_filename_diff(old, new):
    dmpdiffs = diffjes(old, new, False)
    linea, lineb = '', ''
    for op, text in dmpdiffs:
        if op == 0:
            linea += text
            lineb += text
        elif op == -1:
            linea += f'<span class="w">{text}</span>'
        elif op == 1:
            lineb += f'<span class="w">{text}</span>'

    return f'''
<div class="pane a">
<div class="filename del">{linea}</div>
</div>
<div class="pane b">
<div class="filename add">{lineb}</div>
</div>
'''

def render_file(file: PatchedFile, side_by_side: bool) -> str:
    is_modified = file.added != 0 or file.removed != 0
    if (file.is_rename and not is_modified) or file.is_removed_file:
        side_by_side = True

    if file.is_rename:
        filename_header = generate_filename_diff(file.source_file[2:], file.target_file[2:])
    elif file.is_removed_file:
        filename_header = f'<div class="filename del">{file.source_file[2:]}</div>'
    else:
        if file.is_added_file:
            side_by_side = False

        filename_header = f'<div class="filename">{file.target_file[2:]}</div>'

    if side_by_side:
        hunk_separator = '<span class="hunk-sep"></span>'
    else:
        hunk_separator = '<span class="line hunk"></span>'

    if side_by_side:
        return '<div class="diff-split">' + \
            filename_header + \
            (hunk_separator if (not file.is_removed_file) and len(file) and file[0].target_start != 1 and file[0].target_start != 1 else '') + \
            (''.join(intersperse([render_hunk(hunk, side_by_side=side_by_side) for hunk in file], hunk_separator)) if not file.is_removed_file else '') + \
            '</div>'
    else:
        return '<div class="codeblock">' + \
            filename_header + \
            '<pre class="diff numbered">' + \
            '<code>' + \
            (hunk_separator if (not file.is_removed_file) and len(file) and file[0].target_start != 1 and file[0].target_start != 1 else '') + \
            (''.join(intersperse([render_hunk(hunk, side_by_side=side_by_side) for hunk in file], hunk_separator)) if not file.is_removed_file else '') + \
            '</code>' + \
            '</pre>' + \
            '</div>'


def render(diff: str, side_by_side: bool = False):
    patch_set = PatchSet.from_string(diff)
    return ''.join(intersperse([render_file(file, side_by_side=side_by_side) for file in patch_set], '\n\n'))
