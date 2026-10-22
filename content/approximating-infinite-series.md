{
    "title": "Approximating infinite series",
    "date": "2026-10-22"
}

# Approximating infinite series

<p class="lede" markdown="1">In this post, I'll derive the Euler-Maclaurin summation formula, which allows you to closely approximate a summation over a function $f$ by its integral.</p>

For infinite series that are hard to evaluate analytically, we can sometimes resort to *numeric evaluation*, that is, we find a close approximation of the series.

For example, Euler famously applied this to the [Basel problem](https://en.wikipedia.org/wiki/Basel_problem), which asks for the value of $\sum_{k = 1}^\infty \frac{1}{k^2}$. Before finding the analytical value $\frac{pi^2}{6}$, Euler found that
$$ \sum_{k = 1}^\infty \frac{1}{k^2} \approx 1.64493406... $$

Euler found the first 20 fractional digits of the expression, and it is commonly believed that this convinced him that $\sum_{k = 1}^\infty = \frac{\pi^2}{6}$, which he subsequently proved.

In this post, I'll explain how Euler was able to find such an accurate approximation. We'll start with a naive approximation method and figure out more accurate methods step-by-step.


## Infinite sums, the naive way

Suppose we want to numerically evaluate
$\sum_{k = 1}^\infty f(k)$. In order for this sum to converge, $f$ must be a function that satisfies $\lim_{k \rightarrow \infty} f(k)= 0$. By definition, we have
$$ \sum_{k = 1}^\infty f(k) = \lim_{N \rightarrow \infty} \sum_{k = 1}^N f(k) $$

So, as a first approximation to $\sum_{k = 1}^\infty f(k)$, we can take some $N$ and evaluate the partial sum of the first $N$ terms. We expect the approximation to get better as $N$ gets larger.

This gives us our first, naive way of approximation $\sum_{k = 1}^\infty f(k)$: For large $N$, we have
$$ \sum_{k = 1}^\infty f(k) \approx \sum_{k = 1}^N f(k) \tag{1} $$

How well this method works depends greatly on how fast $f$ goes to 0.

TODO: examples here


## Estimating the tail

We can write split the series explicitly in the partial sum of the first $N$ terms, and the other terms:

$$ \sum_{k = 1}^N f(k) = \sum_{k = 1}^N f(k) + \sum_{k = N+1}^\infty f(k) \tag{2} $$


By approximating an infinite series with a partial sum, we essentially drop the infinite "tail" $\sum_{k = N+1}^\infty f(k)$. Evaluating this sum directly is as hard as evaluating the original (complete) sum, but we can improve the accuracy of our initial approximation by adding an approximation to the infinite sum.

For this, we can use the approximation

$$ \sum_{k = a}^{b - 1} f(k) \approx \int_a^b f(x)\text{d}x $$

This gives us an improved formula for approximating $\sum_{k = 1}^N f(k)$:
$$ \sum_{k = 1}^\infty f(k) \approx \sum_{k = 1}^N f(k) + \int_{N+1}^\infty f(x)\text{d}x \tag{3} $$

TODO: examples


## A geometric improvement

Now, again, we want to improve the accuracy of the approximation
$$ \sum_{k = a}^{b - 1} f(k) \approx \int_a^b f(x)\text{d}x $$

Using $\sum_{k = a}^{b - 1} f(k) = \int_a^b f(\lfloor x \rfloor)\text{d}x$ we can write the error $E(x)$ explicitly as $E(x) = f(\lfloor x \rfloor) - f(x)$. We now have
$$ \sum_{k = a}^{b - 1} f(k) = \int_a^b f(x) + E(x)\ \text{d}x \tag{4} $$

Let's visualize this and draw $f(x)$, $f(\lfloor x \rfloor)$, and $E(x)$ in a single graph:
![](../images/f_k_integral_diagram_clean.svg)

Gathering the shaded segments on the left, we can see that the shaded areas look a lot like triangles:

![](../images/f_k_integral_gathered_and_original.svg)

We can therefore estimate the shaded area on the interval $[k, k+1]$ with the formula for the area of a triangle:
$$ \int_k^{k+1} E(x)\ \text{d}x \approx \frac{f(k) - f(k+1)}{2} $$

If we plug this into $(4)$, we get
$$ \sum_{k = a}^{b - 1} f(k) \approx \int_a^b f(x)\ \text{d}x + \frac{f(a) - f(b)}{2} \tag{5} $$

Setting $a = N+1$, $b = \infty$ and using that $\lim_{k \rightarrow \infty} f(k) = 0$ gives us
$$ \sum_{N+1}^\infty f(k) \approx \int_{N+1}^\infty f(x)\ \text{d}x + \frac{f(N+1)}{2} $$

If we plug this into $(2)$, we get
$$ \sum_{k = 1}^\infty f(k) \approx \sum_{k = 1}^N f(k) + \int_{N+1}^\infty f(x)\ \text{d}x + \frac{f(N+1)}{2} \tag{6} $$

This is again an improvement over the previous approximation formula.

TODO: examples

A natural question is now if we can further improve this method. Intuitively you'd expect a connection with the first derivative of $f$, and it feels like you might be able to generalize this to higher-order derivatives. However, geometrically it's not clear exactly how this would generalize.


## Analysis with Taylor series

Let's try to see what's going on through the lens of Taylor series.

If we take $(5)$ and set $a = k$, $b = k+1$, the summation is just over a single term. Using $\int_k^{k+1} f(x)\ \text{d}x = \int_0^1 f(k + t)\ \text{d}t$ we get
$$ f(k) = \int_0^1 f(k + t)\ \text{d}t + \frac{f(k) - f(k+1)}{2} \tag{7} $$

Using the Taylor expansion of $f(x)$ at $x = k$, we get
$$ f(k + t) = f(k) + f'(k)t + \frac{f''(k)}{2} t^2 + ... $$

We can substitute the Taylor series both in $\int_0^1 f(k + t)\ \text{d}t$ and $f(k+1)$:
$$ \begin{align*} \int_0^1 f(k + t)\ \text{d}t &= f(k) + \frac{f'(k)}{2} + \frac{f''(k)}{6} + ... \\
f(k+1) &= f(k) + f'(k) + \frac{f''(k)}{2} + ...
 \end{align*} $$

Substituting these expressions back in $(7)$ gives
$$ \int_0^1 f(k + t)\ \text{d}t + \frac{f(k) - f(k+1)}{2} \\= f(k) - \frac{1}{12} f''(k) + ... $$

In other words, the term $\frac{f(k) - f(k+1)}{2}$ serves as a correction that cancels the term involving $f'(k)$ in the Taylor expansion of $\int_0^1 f(k + t)\ \text{d}t$. The rest terms now only derivatives of at least second order. For smooth functions we expect that the magnitude of higher derivatives is much smaller than that of lower derivatives, which explains why $(6)$ is a better approximation to $f(k)$ than $(3)$.


## General case

In the previous section we saw that adding the term $\frac{f(k) - f(k+1)}{2}$ cancels the terms involving first order derivatives in the Taylor expansion of $\int_0^1 f(k + t)\ \text{d}t$. This idea generalizes in a straightforward way: We'll now try to cancel the terms involving the first $N$ derivatives.

That is, we try to find $c_0$, $c_1$, ..., $c_{N-1}$ such that
$$ \int_0^1 f(k + t)\ \text{d}t + \sum_{i = 0}^{N - 1} c_i(f^{(i)}(k) - f^{(i)}(k+1)) $$

contains no terms involving $f'(k)$, $f''(k)$, ..., $f^{(N)}(k)$. This happens exactly when the coefficients of $f^{(n)}(k)$ in the Taylor expansions of $\int_0^1 f(k + t)\ \text{d}t$ and $-\sum_{i = 0}^{N - 1} c_i(f^{(i)}(k) - f^{(i)}(k+1))$ match for $n = 1, 2, ..., N$.

Using the Taylor expansion of $f(x)$ at $x = k$ we get
$$ \int_0^1 f(k + t)\ \text{d}t = \sum_{j = 0}^\infty \frac{1}{(j+1)!} f^{(j)}(k) $$

So the coefficient of $f^{(n)}$ in the Taylor expansion of $\int_0^1 f(k + t)\ \text{d}t$ is $\frac{1}{(n+1)!}$.

Likewise we have $-\sum_{i = 0}^{N - 1} c_j(f^{(j)}(k) - f^{(j)}(k+1)) = \sum_{i = 0}^{N - 1} c_j(f^{(j)}(k+1) - f^{(j)}(k))$ and

$$ c_i (f^{(i)}(k+1) - f^{(i)}(k)) = \sum_{j = 1}^\infty \frac{c_i}{j!} f^{(i + j)}(k) $$

So the coefficient of $f^{(n)}$ in the Taylor expansion of $-\sum_{i = 0}^{N - 1} c_j(f^{(j)}(k) - f^{(j)}(k+1))$ is $\sum_{i = 0}^{n - 1} \frac{c_i}{(n - i)!}$.

Equating the two gives
$$ \sum_{i = 0}^{n - 1} \frac{1}{(n - i)!} c_i = \frac{1}{(n+1)!} \tag{8} $$

Evaluating this relation for $n = 1$ gives $c_0 = \frac{1}{2}$. For $n = 2$ it gives
$$ \frac{1}{2!} c_0 + \frac{1}{1!} c_1 = \frac{1}{3!} $$

Substituting $c_0 = \frac{1}{2}$ gives $c_1 = -\frac{1}{12}$. Now, we can set $n = 3$ and substitute the values for $c_0$ and $c_1$ to find $c_2$. We can continue this strategy to compute all the coefficients we need.

The first 10 coefficients are:
$$ \frac{1}{2}, -\frac{1}{12}, 0, \frac{1}{720}, 0, -\frac{1}{30240}, 0, -\frac{1}{1209600}, 0, -\frac{1}{47900160} $$


## Demonstration

<div>
  <style>
    .loggraph {
      --lg-s1: #2a78d6; --lg-s2: #eb6834; --lg-s3: #1baf7a; --lg-s4: #eda100;
      --lg-s5: #e87ba4; --lg-s6: #008300; --lg-s7: #4a3aa7; --lg-s8: #e34948;
      font-family: var(--ui-font, sans-serif);
      margin: 1.5em 0;
    }
    @media (prefers-color-scheme: dark) {
      .loggraph {
        --lg-s1: #3987e5; --lg-s2: #d95926; --lg-s3: #199e70; --lg-s4: #c98500;
        --lg-s5: #d55181; --lg-s6: #008300; --lg-s7: #9085e9; --lg-s8: #e66767;
      }
    }
    .loggraph .lg-controls { display: flex; flex-wrap: wrap; align-items: center; gap: .5em 1.5em; margin-bottom: .5em; font-size: .9rem; }
    .loggraph select { font: inherit; color: var(--fg); background: var(--bg); border: 1px solid var(--rule); border-radius: 4px; padding: .2em .4em; }
    .loggraph .lg-legend { display: flex; flex-wrap: wrap; gap: .25em 1em; margin: 0; padding: 0; list-style: none; color: var(--muted); }
    .loggraph .lg-legend li { display: flex; align-items: center; gap: .4em; }
    .loggraph .lg-swatch { display: inline-block; width: 16px; height: 3px; border-radius: 2px; }
    .loggraph svg { display: block; width: 100%; height: auto; user-select: none; }
    .loggraph .lg-grid { stroke: var(--rule); stroke-width: 1; }
    .loggraph .lg-axis { stroke: var(--muted); stroke-width: 1; }
    .loggraph .lg-tick-label { fill: var(--muted); font-size: 14.5px; }
    .loggraph .lg-axis-title { fill: var(--fg); font-size: 15.5px; }
    .loggraph .lg-line { fill: none; stroke-width: 2; stroke-linejoin: round; stroke-linecap: round; }
    .loggraph .lg-point { stroke: var(--bg); stroke-width: 1.5; }
    .loggraph .lg-crosshair { stroke: var(--muted); stroke-width: 1; stroke-dasharray: 4 3; pointer-events: none; }
    .loggraph .lg-tooltip rect { fill: var(--bg); stroke: var(--rule); }
    .loggraph .lg-tooltip text { fill: var(--fg); font-size: 14px; }
  </style>

  <div class="loggraph">
    <div class="lg-controls">
      <label>Graph: <select class="lg-select"></select></label>
      <ul class="lg-legend"></ul>
    </div>
    <svg class="lg-svg" xmlns="http://www.w3.org/2000/svg"></svg>
  </div>

  <script>
  (function () {
    // ===================== Configuration =====================
    const ENABLE_CROSSHAIR = true;   // dashed crosshair + readout following the cursor
    const ENABLE_SNAPPING = true;    // snap to the nearest data point when close
    const SNAP_RADIUS = 14;          // snapping distance, in SVG units (~px at full width)

    // Fixed axis ranges, given as exponents (never derived from the data).
    // x runs from 2^X_MIN_EXP to 2^X_MAX_EXP, y runs from 10^Y_MIN_EXP to 10^Y_MAX_EXP.
    const X_MIN_EXP = -0.5, X_MAX_EXP = 24.5;
    const Y_MIN_EXP = -16,  Y_MAX_EXP = 1;
    const X_LABEL_STEP = 2;          // label every 2nd power of 2 (minor tick on every power)
    const Y_LABEL_STEP = 2;          // label every 2nd power of 10 (minor tick on every power)
    const X_TITLE = 'number of terms';
    const Y_TITLE = 'Absolute error';

    // Data: y-values per series; the i-th value is plotted at x = 2**i.
    // Non-positive values and null are skipped (they cannot be shown on a log axis).
    const DATA = {
        "Basel": {
            "naive": [ 0.6449340668482264, 0.3949340668482264, 0.22132295573711525, 0.11751201469403139, 0.0605875334032393, 0.030766804020301963, 0.015503565439338951, 0.007782061893764514, 0.0038986305395458665, 0.0019512188931296581, 0.000976085818062078, 0.00048816206011292884, 0.00024411082510300552, 0.00012206286222249396, 6.1033293642820396e-05, 3.051711246837563e-05, 1.5258672647844307e-05, 7.629365427419543e-06, 3.814689989667386e-06, 1.9073468138230965e-06, 9.536738616588991e-07, 4.768370445162873e-07, 2.3841855067985307e-07, 1.1920928244535389e-07 ],
            "0th": [ 0.1449340668482264, 0.06160073351489315, 0.02132295573711529, 0.006400903582920225, 0.001764003991474583, 0.00046377371727168715, 0.00011895005472362108, 3.0123909268375826e-05, 7.579955888292744e-06, 1.9011543381797225e-06, 4.760619645161057e-07, 1.1911233355199613e-07, 2.979019941840022e-08, 7.44906492045061e-09, 1.862455745182956e-09, 4.656375285350123e-10, 1.1641243524707079e-10, 2.9103386367523854e-11, 7.275957614183426e-12, 1.8189894035458565e-12, 4.547473508864641e-13, 1.1368683772161603e-13, 2.842170943040401e-14 ],
            "1st": [ 0.019934066848226406, 0.0060451779593375665, 0.0013229557371152723, 0.0002280640767473585, 3.39001852462939e-05, 4.636894498588617e-06, 6.068594573527264e-07, 7.763801068705334e-08, 9.818565960273418e-09, 1.234514712677992e-09, 1.5476642190037637e-10, 1.9374057913523757e-11, 2.4236168627567167e-12, 3.0309088572266774e-13, 3.7969627442180354e-14 ],
            "2nd": [ 0.0008992664851068533, 0.0001276615468353004, 1.0377596218136276e-05, 5.59608666517164e-07, 2.341879734579777e-08, 8.511860105642199e-10, 2.8723468048497125e-11, 9.330314298949816e-13, 2.9753977059954195e-14 ],
            "4th": [ 0.0001424001815597542, 9.512664413069416e-06, 2.8907044846704366e-07, 4.894260330345901e-09, 5.774514200140857e-11, 5.579980921766037e-13 ]
        },
        "Fractional power": {
            "naive": [ 1.6123753486854882, 1.2588219580922144, 0.9413718683623391, 0.6856986689786073, 0.4923095009330627, 0.35081283084425996, 0.24902725206146714, 0.17643210265720954, 0.12487804889652399, 0.08834521034885556, 0.06248474493622691, 0.044188779686094026, 0.031248092767782065, 0.022096412583082703, 0.015624761585058433, 0.01104845916298558, 0.007812470197790855, 0.00552426119132754, 0.00390624627471281, 0.002762134546921313, 0.0019531245343387127, 0.0013810677673684602, 0.0009765624417923391, 0.0006905339454226223 ],
            "0th": [ 0.19816178631239323, 0.10412141971296274, 0.04694467736242336, 0.019032002311940577, 0.0072382508603969775, 0.0026575189328643667, 0.0009577828830500401, 0.0003419213920845543, 0.00012147658616301626, 4.3053211185917206e-05, 1.5240180784470425e-05, 5.391505493612669e-06, 1.9067666978678233e-06, 6.742466909237521e-07, 2.3840038965161625e-07, 8.429048126146199e-08, 2.9801753509417495e-08, 1.0536611139144725e-08, 3.7252720908043102e-09, 1.3170855517330438e-09, 4.656608432185294e-10, 1.6463541641087431e-10, 5.820766091346741e-11, 2.0579093984451902e-11 ],
            "1st": [ 0.021385091015756252, 0.00789637484802519, 0.00222331781242735, 0.000513483793421976, 0.0001048501240341615, 1.9978691111255387e-05, 3.669540056261411e-06, 6.613508731767581e-07, 1.180527871014192e-07, 2.0970865488578738e-08, 3.71621000638811e-09, 6.577409727981376e-10, 1.1634382346414895e-10, 2.0572876735514e-11, 3.6366465394621628e-12, 6.425970866530406e-13, 1.1324274851176597e-13, 1.9539925233402755e-14 ],
            "2nd": [ 0.0007119958963235362, 0.0001223788907194212, 1.275016507262805e-05, 9.194987589111747e-07, 5.2827971330771106e-08, 2.6743567360654197e-09, 1.266475813110901e-10, 5.795808277753167e-12, 2.611244553918368e-13, 1.199040866595169e-14 ],
            "4th": [ 9.36270640128356e-05, 7.5546189362007965e-06, 2.9356479602782315e-07, 6.63885568741307e-09, 1.074860200844796e-10, 1.4459544672718039e-12, 1.7319479184152442e-14 ]
        },
        "Near harmonic": {
            "naive": [ 9.584448464950809, 9.117931969182404, 8.601641508411454, 8.072919613922199, 7.55517101493529, 7.0600825606526065, 6.592399990698391, 6.153320931827826, 5.742370802601563, 5.358344173184569, 4.9997559030850685, 4.665051072250923, 4.352699684669206, 4.0612371943599594, 3.789279852405711, 3.535528511166313, 3.2987672601776676, 3.0778598592531274, 2.8717453397509134, 2.679433400810118, 2.4999998807907335, 2.332582423228926, 2.176376382295885, 2.0306309787870873 ],
            "0th": [ 0.25411854958273494, 0.15834737077478245, 0.08824228320360739, 0.04550399631989244, 0.02239406568490132, 0.010740153818288078, 0.00508145974634111, 0.002387470945963699, 0.0011177721011410569, 0.0005223914748579972, 0.0002439222537748975, 0.00011384467107511398, 5.312230089593584e-05, 2.4785202528576633e-05, 1.1563352723342746e-05, 5.394645699041689e-06, 2.516726409496073e-06, 1.1741025982558995e-06, 5.477401447961938e-07, 2.5553026183899874e-07, 1.192091882984414e-07, 5.5613078586702613e-08, 2.594442527481533e-08, 1.2103503976845786e-08 ],
            "1st": [ 0.02086030169853359, 0.00902096080132253, 0.0031082909515287582, 0.0009072428887684225, 0.0002388393635772701, 5.933198975149878e-05, 1.429164560917684e-05, 3.3882091869941178e-06, 7.968033788330331e-07, 1.8662283984838268e-07, 4.3620563161539394e-08, 1.0185287280251032e-08, 2.3770194701455694e-09, 5.546016978996704e-10, 1.2938095039771724e-10, 3.0183855415089056e-11, 7.041478511382593e-12, 1.644906433284632e-12, 3.836930773104541e-13, 9.237055564881302e-14, 2.3092638912203256e-14 ],
            "2nd": [ 0.0005217043575189706, 0.00010454203038889887, 1.3288764380448015e-05, 1.2094959398467608e-06, 8.954773100811053e-08, 5.90929616350877e-09, 3.6698288852221594e-10, 2.2092550011620915e-11, 1.3091749906379846e-12, 7.638334409421077e-14 ],
            "4th": [ 5.828255675055516e-05, 5.470975970922609e-06, 2.588915872792086e-07, 7.381636635273026e-09, 1.539532945571409e-10, 2.6982860390489805e-12, 4.263256414560601e-14 ]
        },
        "Logarithmic": {
            "naive": [ 1.069058310734086, 0.7928798275040116, 0.5855828460103218, 0.44401813327412865, 0.34935330444432156, 0.2847701750670557, 0.23911635040590573, 0.20560544648124313, 0.18014705341223358, 0.1602243079291492, 0.14423904296474221, 0.13114150155257165, 0.12021929470314063, 0.1109742867607395, 0.10304867360996983, 0.09617924594812033, 0.09016825396909045, 0.08486433175047647, 0.08014968773564801, 0.07593130144613447, 0.07213474460089664, 0.06869976047609239, 0.06557704577520829, 0.06272587063944668 ],
            "0th": [ 0.15881908410724876, 0.07153230705953018, 0.02747221945907441, 0.00972365137087694, 0.0033770481831281174, 0.0011916830157221447, 0.000433198314875316, 0.00016262729248461838, 6.290464310199084e-05, 2.497549993929482e-05, 1.013953725959027e-05, 4.194819032132813e-06, 1.7634192182036657e-06, 7.514908215711102e-07, 3.2402943261899964e-07, 1.4114244972773804e-07, 6.20275790730318e-08, 2.747287952686861e-08, 1.2252665104739435e-08, 5.498447031015985e-09, 2.4811783738698523e-09, 1.1252505593972728e-09, 5.126392643717281e-10, 2.345141858484112e-10 ],
            "1st": [ 0.02072984249221177, 0.0064895264031048505, 0.0015149301699555195, 0.00029306652029603697, 5.206013044745106e-05, 9.083586985259018e-06, 1.6100793289730575e-06, 2.936311145340653e-07, 5.522326107509912e-08, 1.0688547380510727e-08, 2.121770315000049e-09, 4.304423484313702e-10, 8.895595371427589e-11, 1.8675283541824683e-11, 3.97326616052851e-12, 8.535394613318203e-13, 1.8385293287792592e-13, 3.907985046680551e-14 ],
            "2nd": [ 0.0009078092078635969, 0.00013046017002338317, 1.0941143004483678e-05, 6.315926044386799e-07, 2.9887051056221026e-08, 1.3098486739693271e-09, 5.682387893557461e-11, 2.5153212845907547e-12, 1.163513729807164e-13 ],
            "4th": [ 0.00016867582949409154, 1.3664365769994191e-05, 6.690261513675466e-07, 2.799824683208385e-08, 1.1636096530764917e-09, 4.816325116507869e-11, 1.9966250874858815e-12, 8.260059303211165e-14 ]
        },
        "Exponential": {
            "naive": [ 0.214097265697884, 0.07876198246127131, 0.010659275204673135, 0.00019523143546429367, 6.54928502541452e-08 ],
            "0th": [ 0.07876198246127131, 0.028974914093407356, 0.00392132820558766, 7.18216313776443e-05, 2.4093473105502028e-08 ],
            "1st": [ 0.011094340842965011, 0.0040813799094754355, 0.0005523547060449774, 1.0116729334264107e-05, 3.3937844756692925e-09 ],
            "2nd": [ 0.000183599426752723, 6.754245451323637e-05, 9.140877212154841e-06, 1.6742100628075463e-07, 5.616362930283003e-11 ],
            "4th": [ 4.3662444092484876e-06, 1.6062515532100363e-06, 2.173825087714576e-07, 3.9814993524345255e-09, 1.3354872763216008e-12 ]
        }
    }
    // =========================================================

    const root = document.currentScript.parentElement.querySelector('.loggraph');
    const svg = root.querySelector('.lg-svg');
    const select = root.querySelector('.lg-select');
    const legend = root.querySelector('.lg-legend');
    const NS = 'http://www.w3.org/2000/svg';
    const COLORS = [1, 2, 3, 4, 5, 6, 7, 8].map(k => `var(--lg-s${k})`);

    // Geometry (SVG user units; the SVG scales to the container width).
    const W = 720, H = 450;
    const M = { top: 14, right: 18, bottom: 56, left: 72 };
    const PW = W - M.left - M.right, PH = H - M.top - M.bottom;
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);

    // Scales work on exponents: x = 2^xe, y = 10^ye.
    const sx = xe => M.left + (xe - X_MIN_EXP) / (X_MAX_EXP - X_MIN_EXP) * PW;
    const sy = ye => M.top + (Y_MAX_EXP - ye) / (Y_MAX_EXP - Y_MIN_EXP) * PH;
    const invX = px => X_MIN_EXP + (px - M.left) / PW * (X_MAX_EXP - X_MIN_EXP);
    const invY = py => Y_MAX_EXP - (py - M.top) / PH * (Y_MAX_EXP - Y_MIN_EXP);

    function el(name, attrs, parent) {
      const node = document.createElementNS(NS, name);
      for (const k in attrs) node.setAttribute(k, attrs[k]);
      if (parent) parent.appendChild(node);
      return node;
    }
    const minus = s => String(s).replace('-', '−');
    // Appends "base^exp" as text with a superscript.
    function powerText(textEl, base, exp) {
      el('tspan', {}, textEl).textContent = base;
      el('tspan', { dy: '-0.55em', 'font-size': '0.78em' }, textEl).textContent = minus(exp);
    }

    // ---- Static axes and grid ----
    const axes = el('g', {}, svg);
    const ceilX = Math.ceil(X_MIN_EXP), ceilY = Math.ceil(Y_MIN_EXP);
    for (let k = ceilX; k <= X_MAX_EXP; k++) {
      const x = sx(k), major = k % X_LABEL_STEP === 0;
      if (major) el('line', { class: 'lg-grid', x1: x, x2: x, y1: M.top, y2: M.top + PH }, axes);
      el('line', { class: 'lg-axis', x1: x, x2: x, y1: M.top + PH, y2: M.top + PH + (major ? 6 : 3) }, axes);
      if (major) powerText(el('text', { class: 'lg-tick-label', x: x, y: M.top + PH + 22, 'text-anchor': 'middle' }, axes), '2', k);
    }
    for (let k = ceilY; k <= Y_MAX_EXP; k++) {
      const y = sy(k), major = k % Y_LABEL_STEP === 0;
      if (major) el('line', { class: 'lg-grid', x1: M.left, x2: M.left + PW, y1: y, y2: y }, axes);
      el('line', { class: 'lg-axis', x1: M.left - (major ? 6 : 3), x2: M.left, y1: y, y2: y }, axes);
      if (major) powerText(el('text', { class: 'lg-tick-label', x: M.left - 10, y: y + 5, 'text-anchor': 'end' }, axes), '10', k);
    }
    el('line', { class: 'lg-axis', x1: M.left, x2: M.left + PW, y1: M.top + PH, y2: M.top + PH }, axes);
    el('line', { class: 'lg-axis', x1: M.left, x2: M.left, y1: M.top, y2: M.top + PH }, axes);
    el('text', { class: 'lg-axis-title', x: M.left + PW / 2, y: H - 8, 'text-anchor': 'middle' }, axes).textContent = X_TITLE;
    el('text', { class: 'lg-axis-title', x: 0, y: 0, 'text-anchor': 'middle',
                 transform: `translate(16 ${M.top + PH / 2}) rotate(-90)` }, axes).textContent = Y_TITLE;

    // ---- Data layer (clipped to the plot area) ----
    const clipId = 'lg-clip-' + Math.random().toString(36).slice(2);
    el('rect', { x: M.left, y: M.top, width: PW, height: PH },
       el('clipPath', { id: clipId }, el('defs', {}, svg)));
    const dataLayer = el('g', { 'clip-path': `url(#${clipId})` }, svg);

    // ---- Interaction layer ----
    const hover = el('g', { visibility: 'hidden', 'pointer-events': 'none' }, svg);
    const vLine = el('line', { class: 'lg-crosshair', y1: M.top, y2: M.top + PH }, hover);
    const hLine = el('line', { class: 'lg-crosshair', x1: M.left, x2: M.left + PW }, hover);
    const marker = el('circle', { class: 'lg-point', r: 6 }, hover);
    const tooltip = el('g', { class: 'lg-tooltip' }, hover);
    const ttRect = el('rect', { rx: 4 }, tooltip);
    const ttText = el('text', {}, tooltip);
    if (!ENABLE_CROSSHAIR) { vLine.remove(); hLine.remove(); }

    let points = []; // { series, color, i, y, px, py } for the current graph

    function render(name) {
      dataLayer.replaceChildren();
      legend.replaceChildren();
      points = [];
      Object.entries(DATA[name]).forEach(([series, ys], s) => {
        const color = COLORS[s % COLORS.length];
        let d = '', penDown = false;
        const pts = [];
        ys.forEach((y, i) => {
          if (y == null || !(y > 0) || !isFinite(y)) { penDown = false; return; }
          const px = sx(i), py = sy(Math.log10(y));
          d += (penDown ? 'L' : 'M') + px.toFixed(2) + ' ' + py.toFixed(2);
          penDown = true;
          pts.push({ series, color, i, y, px, py });
        });
        el('path', { class: 'lg-line', d, stroke: color }, dataLayer);
        pts.forEach(p => el('circle', { class: 'lg-point', cx: p.px, cy: p.py, r: 4, fill: color }, dataLayer));
        points.push(...pts);

        const li = document.createElement('li');
        const sw = document.createElement('span');
        sw.className = 'lg-swatch';
        sw.style.background = color;
        li.append(sw, series);
        legend.appendChild(li);
      });
      hover.setAttribute('visibility', 'hidden');
    }

    // ---- Tooltip ----

    function setTooltip(lines, cx, cy) {
      ttText.replaceChildren();
      lines.forEach((line, n) => {
        const t = el('tspan', { x: 10, dy: n === 0 ? '1.25em' : '1.35em' }, ttText);
        if (line.bold) t.setAttribute('font-weight', '600');
        t.textContent = line.text;
      });
      const bb = ttText.getBBox();
      const w = bb.width + 20, h = bb.height+10;
      ttRect.setAttribute('width', w);
      ttRect.setAttribute('height', h);
      let tx = cx+14, ty = cy+14;
      if (tx + w > M.left + PW) tx = cx - 14 - w;
      if (ty + h > M.top + PH) ty = cy - 14 - h;
      tooltip.setAttribute('transform', `translate(${tx} ${Math.max(M.top, ty)})`);
    }

    function toSvgPoint(evt) {
      const pt = svg.createSVGPoint();
      pt.x = evt.clientX; pt.y = evt.clientY;
      return pt.matrixTransform(svg.getScreenCTM().inverse());
    }

    function onMove(evt) {
      if (!ENABLE_CROSSHAIR && !ENABLE_SNAPPING) return;
      const p = toSvgPoint(evt);
      const inside = p.x >= M.left && p.x <= M.left + PW && p.y >= M.top && p.y <= M.top + PH;
      if (!inside) { hover.setAttribute('visibility', 'hidden'); return; }

      let snap = null;
      if (ENABLE_SNAPPING) {
        let best = SNAP_RADIUS * SNAP_RADIUS;
        for (const q of points) {
          const d2 = (q.px - p.x) ** 2 + (q.py - p.y) ** 2;
          if (d2 <= best) { best = d2; snap = q; }
        }
      }
      if (!snap && !ENABLE_CROSSHAIR) { hover.setAttribute('visibility', 'hidden'); return; }

      const cx = snap ? snap.px : p.x, cy = snap ? snap.py : p.y;
      vLine.setAttribute('x1', cx); vLine.setAttribute('x2', cx);
      hLine.setAttribute('y1', cy); hLine.setAttribute('y2', cy);
      marker.setAttribute('visibility', snap ? 'visible' : 'hidden');

      if (snap) {
        marker.setAttribute('cx', cx); marker.setAttribute('cy', cy);
        marker.setAttribute('fill', snap.color);
        setTooltip([
          { text: snap.series, bold: true },
          { text: `x = ${2 ** snap.i}` },
          { text: `y = ${snap.y}` },
        ], cx, cy);
      } else {
        // Between data points: round to 4 significant digits to avoid float noise.
        const round = v => Number(v.toPrecision(4));
        setTooltip([
          { text: `x = ${round(2 ** invX(cx))}` },
          { text: `y = ${round(10 ** invY(cy))}` },
        ], cx, cy);
      }
      hover.setAttribute('visibility', 'visible');
    }

    svg.addEventListener('pointermove', onMove);
    svg.addEventListener('pointerdown', onMove);
    svg.addEventListener('pointerleave', () => hover.setAttribute('visibility', 'hidden'));

    Object.keys(DATA).forEach(name => select.add(new Option(name, name)));
    select.addEventListener('change', () => render(select.value));
    render(select.value);
  })();
  </script>
</div>


## Relation to the Bernoulli numbers

Taking $(8)$ and multiplying it by $(n+1)!$ we get
$$ \sum_{i = 0}^{n - 1} \frac{(n+1)!}{(n - i)!} c_i = 1 $$

We have $\frac{(n+1)!}{(n - i)!} = \binom{n+1}{i+1} \cdot (i+1)!$, so let's substitute $c_i = (i+1)! B_{i+1}$ so we can simplify. We get
$$ \sum_{i = 1}^n \binom{n+1}{i} B_i = 1 $$

This is a recurrence relation for the Bernoulli numbers $B_1$, $B_2$, ... However, the recurrence relation doesn't account for the first Bernoulli number $B_0$. If we boldly extend the summation to $i = 0$ and set $n = 0$ we get $\binom{1}{0} B_0 = 1$, which is indeed correct. For $n > 0$ we have
$$ \sum_{i = 0}^n \binom{n+1}{i} B_i = 1 + \sum_{i = 1}^n \binom{n+1}{i} B_i $$

So we have found the following recurrence relation for the Bernoulli numbers:
$$ \sum_{i = 0}^n \binom{n+1}{i} B_i = \delta_{n, 0} $$

Here, $\delta_{n, 0}$ is defined as
$$ \delta_{n, 0} = \begin{cases} 1 \qquad \text{when $n = 0$} \\ 0 \qquad \text{when $n \neq 0$} \end{cases} $$
