{
    "title": "Approximating sums and integrals"
}

# Approximating sums and integrals

In this post, I'll derive the Euler-Maclaurin summation formula, which allows you to closely approximate a summation over a function $f$ by its integral, or vice versa.

We have the approximate equality:
$$ \sum_{k = a}^{b - 1} f(k) \approx \int_a^b f(x)\text{d}x $$

However, the approximation is not very good.

Note that $\sum_{k = a}^{b - 1} f(k) = \int_a^b f(\lfloor x \rfloor)\text{d}x$ so that we can write the error term $E(x)$ explicitly as
$$ E(x) = f(\lfloor x \rfloor) - f(x) $$

We now have
$$ \sum_{k = a}^{b - 1} f(k) = \int_a^b f(x) + E(x)\ \text{d}x \tag{1} $$

Let's visualize this and draw $f(x)$, $f(\lfloor x \rfloor)$, and $E(x)$ in a single graph:
![](../images/f_k_integral_diagram_clean.svg)

Each of the shaded parts represents an integral $\int_k^{k+1} E(x)\ \text{d}x$ for $k = a, a + 1, ..., b - 1$. When $f$ is positive and monotonically decreasing as in the graph, we have $f(x) < f(\lfloor x \rfloor)$ so that $E(x)$ is nonnegative.

[BEGIN]
Perhaps surprisingly, the sum and integral do not have to be finite in order to apply this. For example, when $f(x) = \frac{1}{x}$ we have $\int_1^n f(x)\ \text{d}x = \log(n)$ and $\int_1^\infty E(x)\ \text{d}x = \gamma \approx 0.577$ so that as $n$ goes to infinity, we have
$$ \sum_{k = 1}^n f(k) = \int_1^\infty f(x)\ \text{d}x + \int_1^\infty E(x)\ \text{d}x  \rightarrow \gamma + \log(n) $$

So for large $n$ we have $\sum_{k = 1}^n \frac{1}{k} \approx \gamma + \log(n)$
[END]

The area of the shaded parts is bounded by $f(a) - f(b)$, which can be seen when we gather them:
![](../images/f_k_integral_gathered_and_original.svg)

So, when $f$ is positive and monotonically decreasing, we have
$$ 0 < \int_a^b E(x)\ \text{d}x < f(a) - f(b) $$

Similarly we have $f(x) < f(x - 1)$, and using this we can derive similar bounds. Similar bounds can also be derived for the case where $f$ is monotonically increasing.


## A geometric trick to improve the estimate

In the general case where $f$ is not monotonically increasing or decreasing, these bounds do not hold, but we can still come up with a significantly improved estimate by using some simple geometry.

In the previous graphs, we can note that the shaded areas look a lot like triangles. This is true for smooth functions which do not oscillate a lot on intervals of unit length. We can therefore easily estimate the shaded area on the interval $[k, k + 1]$ as
$$ \int_k^{k+1} E(x)\ \text{d}x \approx \frac{f(k) - f(k + 1)}{2} $$

If we plug this into $(1)$, we get
$$ \sum_{k = a}^{b - 1} f(k) \approx \int_a^b f(x) + \frac{f(a) - f(b)}{2} \text{d}x \tag{2} $$
