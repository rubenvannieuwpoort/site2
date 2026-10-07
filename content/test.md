{
    "title": "test"
}

# Test

<p class="lede" markdown="1">A specimen page for the document style -- every element in one place, so you can see how headings, prose, code, quotes and tables sit together.</p>


## Prose and inline elements

Body copy runs at 16px with a 1.65 line-height and a **60rem** measure, which keeps lines at roughly 80–95 characters -- comfortable for technical reading without feeling cramped. Inline emphasis comes in the usual flavours: **bold for the thing that matters**, *italic for a shift in tone*, and **_both together_** when you really mean it.

Inline `code` gets a tinted background and a slightly smaller size so it doesn't disrupt the line rhythm -- useful for identifiers like `JournalRepository::save()` or paths like `api/modules/journals/`. Links are [a solid accent blue](#code) with an offset underline that thickens on hover. You can <del>strike text out</del>, <mark>highlight it</mark>, mark up an <abbr title="General Ledger Account">GLA</abbr> abbreviation, or drop in a keyboard hint like <kbd>⌘</kbd> <kbd>K</kbd>. Footnote markers hang as superscripts.[^1]

[^1]: This is a footnote definition.

<small>Small text steps down to 0.85em in the muted colour -- good for captions, timestamps and asides that shouldn't compete with the main flow.</small>


## Headings

###  A third-level heading

Level three is only marginally larger than body text; it earns its hierarchy from weight and the space above it rather than from size. Use it to break a long section into scannable parts.


#### A fourth-level label

Level four drops to uppercase micro-type in the muted colour. It reads as a label rather than a heading, which makes it good for repeating structures -- "Input", "Output", "Caveats" -- inside a section.

## Lists

### Unordered, with nesting
- Top-level items get a comfortable gap so multi-line entries stay legible.
- Nesting inherits the same rhythm:
  - a nested item,
  - and another one, which can itself run long enough to wrap onto a second line without the indent breaking down.
- The list ends flush with the paragraph spacing below it.


### Ordered, for procedures
1. **Apply the schema change.** Numbered items carry slightly more vertical space, since they usually describe actions rather than facts.
2. **Restart the container.** Bold lead-ins let the reader skim the sequence and drop into detail only where they need it.
3. **Verify.** Then check the result before moving on.


### Definitions


`created_at`
:   Set once, on insert. Never touched again.

`last_updated_at`
:   Rewritten on every save, including the insert.

`created_by_user_id`
:   Nullable, because background jobs have no authenticated user to attribute the write to.


<h2 id="code">Code</h2>

A plain block, for shell and short snippets:
```
make test dir=auditFields
docker exec -it moneymonk-mysql-1 mysql -uroot -p moneymonk
```

With a filename header, when the reader needs to know where the code lives:

<div class="codeblock">
  <div class="filename">api/modules/journals/repositories/JournalRepository.php</div>
  <pre><code>$userId = AuthenticationService::getInstance()->getUserId();
$now = TimePoint::now();

if (!$journal->hasId()) {
    $map->put('created_at', $now);
    $map->put('created_by_user_id', $userId);
}</code></pre>
</div>


### With line numbers

Line numbers are generated from a `data-n` attribute and rendered through `::before`, so they are *not* part of the selectable text -- copying the block gives you clean code with no numbers glued to the front. A line can also be highlighted to draw the eye:

<div class="codeblock">
  <div class="filename">src/modules/advanced/common/hooks/useSaveBankbook.ts</div>
  <pre class="numbered"><code><span class="line" data-n="1">import useAdministrationApiUrl from '../../../hooks/useAdministrationApiUrl';</span><span class="line" data-n="2">import useSaveAggregate from '../../../redux/hooks/useSaveAggregate';</span><span class="line" data-n="3">import JournalV1 from '../../../models/Journal';</span><span class="line" data-n="4"></span><span class="line" data-n="5">interface Data {</span><span class="line" data-n="6">  name?: string;</span><span class="line" data-n="7">  is_in_use?: boolean;</span><span class="line" data-n="8">}</span><span class="line" data-n="9"></span><span class="line" data-n="10">export default function useSaveBankbook(bankbookId: number | undefined) {</span><span class="line" data-n="11">  const url = `${useAdministrationApiUrl()}/bankbooks/${bankbookId}`;</span><span class="line" data-n="12"></span><span class="line hl" data-n="13">  // No apiVersion: this must stay on the v1 (PHP) API, not the Kotlin backend.</span><span class="line" data-n="14">  return useSaveAggregate<JournalV1>(url);</span><span class="line" data-n="15">}</span></code></pre>
</div>

Long lines scroll horizontally inside the block rather than wrapping, and the highlight extends the full scroll width -- so a marked line stays marked even when you scroll right.


## Diffs

Diffs reuse the code-block machinery: one `<span class="line">` per row, tinted by an `add` or `del` class, with the `+`/`-` marker drawn through `::before`. Like the line numbers, the marker is not selectable -- copying a block gives you the code rather than a patch you have to strip by hand.


### Inline

Two gutter columns, from `data-a` (the old file) and `data-b` (the new one). An added line has no `data-a`, a deleted line no `data-b` -- the blank column carries the same information as the marker, which is why split views can drop the marker entirely. Changed words can be picked out with `<span class="w">`:

<div class="codeblock">
  <div class="filename">src/modules/advanced/common/hooks/useSaveBankbook.ts</div>
  <pre class="diff numbered"><code><span class="line"><span class="ln" data-a="1" data-b="1"></span>import useSaveAggregate from '../../../redux/hooks/useSaveAggregate';</span><span class="line"><span class="ln" data-a="2" data-b="2"></span></span><span class="line del"><span class="ln" data-a="3"></span>export default function useSaveBankbook(bankbookId: <span class="w">number</span>) {</span><span class="line add"><span class="ln" data-b="3"></span>export default function useSaveBankbook(bankbookId: <span class="w">number | undefined</span>) {</span><span class="line"><span class="ln" data-a="4" data-b="4"></span>  const url = `${useAdministrationApiUrl()}/bankbooks/${bankbookId}`;</span><span class="line add"><span class="ln" data-b="5"></span></span><span class="line"><span class="ln" data-a="5" data-b="6"></span>  return useSaveAggregate<JournalV1>(url);</span><span class="line"><span class="ln" data-a="6" data-b="7"></span>}</span><span class="line hunk"></span></code></pre>
</div>


### Side-by-side

Two panes in a grid, divided by a hairline. Rows align because both panes carry the same number of lines: where one side has nothing, a `gap` filler holds the row open. On a narrow viewport the panes stack rather than forcing the page sideways.

The file name goes above the split, not inside each pane. A path that didn't change has nothing to say twice, so it takes the same single header as any other code block:


<div class="diff-split">
<div class="filename">api/modules/journals/repositories/JournalRepository.php</div>
<div class="pane a">
<pre class="diff numbered"><code><span class="line del"><span class="ln" data-a="1"></span>final class <span class="w">JournalRepository</span> extends Repository</span><span class="line"><span class="ln" data-a="2"></span>{</span><span class="line"><span class="ln" data-a="3"></span>    public function save(Journal $journal): void</span><span class="line"><span class="ln" data-a="4"></span>    {</span></code></pre>
</div>
<div class="pane b">
<pre class="diff numbered"><code><span class="line add"><span class="ln" data-b="1"></span>final class <span class="w">JournalStore</span> extends Repository</span><span class="line"><span class="ln" data-b="2"></span>{</span><span class="line"><span class="ln" data-b="3"></span>    public function save(Journal $journal): void</span><span class="line"><span class="ln" data-b="4"></span>    {</span></code></pre>
</div>
<span class="hunk-sep"></span>
</div>


### Side-by-side, when the path changes too

A rename is the one case where the file name earns two slots -- it *is* part of the change. The headers move back inside the panes and take the `del` / `add` classes, so they read as the first row of the diff rather than as labels. The directory here is unchanged, so only the basename takes the darker word-level tint -- the same `<span class="w">` that marks a changed word in the code rows:

<div class="diff-split">
<div class="pane a">
<div class="filename del">api/modules/journals/repositories/<span class="w">JournalRepository.php</span></div>
</div>
<div class="pane b">
<div class="filename add">api/modules/journals/repositories/<span class="w">JournalStore.php</span></div>
</div>
<span class="hunk-sep"></span>
<div class="pane a">
<pre class="diff numbered"><code><span class="line del"><span class="ln" data-a="1"></span>final class <span class="w">JournalRepository</span> extends Repository</span><span class="line"><span class="ln" data-a="2"></span>{</span><span class="line"><span class="ln" data-a="3"></span>    public function save(Journal $journal): void</span><span class="line"><span class="ln" data-a="4"></span>    {</span></code></pre>
</div>
<div class="pane b">
<pre class="diff numbered"><code><span class="line add"><span class="ln" data-b="1"></span>final class <span class="w">JournalStore</span> extends Repository</span><span class="line"><span class="ln" data-b="2"></span>{</span><span class="line"><span class="ln" data-b="3"></span>    public function save(Journal $journal): void</span><span class="line"><span class="ln" data-b="4"></span>    {</span></code></pre>
</div>
</div>

!!! note "Note"
    The two panes scroll horizontally on their own, so a long line in one does not drag the other along. That is the honest trade for panes that can be authored independently; syncing them needs a few lines of script, which this page deliberately does without.


## Math

Inline math sits in the line without disturbing its rhythm: every journal entry must satisfy $\sum_i d_i - \sum_i c_i = 0$, and the standard <abbr title="Value Added Tax">VAT</abbr> band applies a rate of $r = 0.21$. Delimiters are `\( … \)` or `$ … $` inline, `$$ … $$` or `\[ … \]` for display.

Display math gets its own centred block:
$$ \text{balance}(t) = \sum_{\substack{e \,\in\, E \\ \text{date}(e) \,\le\, t}} \bigl( d_e - c_e \bigr) $$

Multi-line derivations use an `aligned` environment, which lines the relations up on the `&`:

$$
\begin{aligned}
  \text{vat}   &= \text{gross} \cdot \frac{r}{1 + r} \\
  \text{net}   &= \text{gross} - \text{vat} \\
               &= \frac{\text{gross}}{1 + r}
\end{aligned}
$$

Numbered, for the equations you need to refer back to:
$$ A_n = P \, \frac{r\,(1+r)^n}{(1+r)^n - 1} \tag{1} $$

An equation too wide for the measure scrolls inside its own block, exactly as code and tables do -- the page body never scrolls sideways:

$$ \operatorname{depr}(t) = \frac{C - S}{n} \left\lfloor \frac{t}{12} \right\rfloor + \frac{C - S}{12n} \bigl( t \bmod 12 \bigr) + \varepsilon_1 + \varepsilon_2 + \cdots + \varepsilon_k \qquad \text{for } t \in [\,0,\; 12n\,] $$

Code is left alone: `pre`, `code` and `kbd` are on the ignore list, so a shell snippet containing `$$` or `\(` renders as written.

```
echo "pid $$ — untouched $by$ \(the\) renderer"
```


## Quotes

> A blockquote sits in italic muted text behind a hairline rule. It is deliberately quieter than body copy: quoted material is context, not the argument.
> <cite>The style guide, on itself</cite>

> Quotes nest, too, for the times you are quoting someone quoting someone.
> > The inner rule shifts to a darker colour so the levels stay distinguishable.


## Callouts

!!! note "Note"
    The default callout -- a blue-tinted panel for context the reader can safely skim past. Use it for background, links to related docs, or a definition that would clutter the main flow.

!!! warning "Watch out"
    The warning variant, for the thing that will bite. Keep these rare: a page with five warnings has none, because the reader stops seeing the colour.

!!! tip "Tip"
    The green variant, for shortcuts and good defaults. Also useful as a "done" marker at the end of a procedure.


## Tables

<div class="table-wrap">
<table>
  <caption>Table 1 -- element inventory. Wide tables scroll inside their own container so the page body never scrolls sideways.</caption>
  <thead>
    <tr>
      <th>Element</th>
      <th>Purpose</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code><blockquote></code></td>
      <td>Quoted material</td>
      <td>Italic, muted, hairline rule; <code><cite></code> renders with an em-dash prefix</td>
    </tr>
    <tr>
      <td><code><pre class="numbered"></code></td>
      <td>Code with line numbers</td>
      <td>Numbers come from <code>data-n</code>, excluded from selection</td>
    </tr>
    <tr>
      <td><code><dl></code></td>
      <td>Term / definition pairs</td>
      <td>Definitions indent behind a left rule</td>
    </tr>
    <tr>
      <td><code>.admonition</code></td>
      <td>Note, warning, tip</td>
      <td>Three variants; the label is optional</td>
    </tr>
    <tr>
      <td><code><pre class="diff"></code></td>
      <td>Unified diff</td>
      <td>Tints from <code>.add</code> / <code>.del</code>; markers excluded from selection</td>
    </tr>
    <tr>
      <td><code>.diff-split</code></td>
      <td>Side-by-side diff</td>
      <td>Two panes; <code>.gap</code> fillers keep the rows aligned</td>
    </tr>
    <tr>
      <td><code>$$ … $$</code></td>
      <td>Display math</td>
      <td>Rendered by KaTeX at load; wide equations scroll in place</td>
    </tr>
    <tr>
      <td><code>.equation</code></td>
      <td>Numbered display math</td>
      <td>Wraps a <code>$$ … $$</code> block plus an <code>.eqno</code> tag</td>
    </tr>
  </tbody>
</table>
</div>


<footer>
  Specimen page -- light and dark themes are driven by `prefers-color-scheme`. The only external assets are KaTeX (stylesheet, fonts and the auto-render script) from jsDelivr; everything else is inline. Without a network the page still reads fine -- math falls back to its TeX source.
</footer>
