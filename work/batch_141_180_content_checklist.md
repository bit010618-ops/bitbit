# Batch 06 content checklist: source PPT 141-180

Status: source inspection started. This batch must follow the full-content rule for the complete final DSP handout.

Hard rules:
- Preserve all source page content unless it is watermark, decorative background, or a clearly wrong item being corrected.
- Red emphasis, example steps, exercise lists, formulas, diagrams, and tables must be carried into the A4 handout.
- Formula statements and example givens must be rendered as math images, not source-code-like inline text.
- Chapter-cover decorative network background and watermarks can be omitted, but the chapter title and useful navigation content must be preserved.

## Source page checklist

- 141: after-class exercise list for the previous z-transform/frequency-domain chapter. Preserve as an exercise index/reference list in the final handout, not as decorative material. Include Zheng Junli book exercises 8-17, 8-21(2)(4), 8-23, 8-24, 8-25, 8-26, 8-27, 8-29, 8-32, 8-33, 8-34, 8-36, 8-37 and Gao Xi full-book exercises 2-12, 2-13, 2-14, 2-15, 2-17, 2-18, 2-19, 2-23, 2-24, 2-25, 2-28 with their source notes.
- 142: chapter cover for chapter 3 "离散傅里叶变换". Preserve as a clean chapter opener in the final handout; omit decorative network background, class-banner, and watermark.
- 143: chapter 3 contents page. Preserve six items: 离散傅里叶级数 DFS, 离散傅里叶变换 DFT, 各种变换的关系, 频率采样, 用 DFT 进行线性卷积, 用 DFT 进行频谱分析. Omit decorative boxes/background only after converting the content into the handout's chapter roadmap style.
- 144: review page with Fourier Series, Fourier Transform, and DTFT formulas. Preserve the three paired transform definitions:
  - Fourier series: periodic signal expansion and coefficient integral over one period.
  - Fourier transform: inverse and forward transform integrals.
  - DTFT: inverse integral over [-π,π] and forward infinite sum.
  All formulas must be rendered as math formulas in the handout, not copied as raster screenshots unless redrawn cleanly.
- 145: review page showing four time/frequency continuity-periodicity cases. Preserve the four panels and labels:
  - (a) time-domain periodic continuous signal, frequency-domain nonperiodic discrete spectrum.
  - (b) time-domain nonperiodic continuous signal, frequency-domain nonperiodic continuous spectrum.
  - (c) time-domain nonperiodic discrete signal, frequency-domain periodic continuous spectrum.
  - (d) time-domain periodic discrete signal, frequency-domain periodic discrete spectrum.
  Redraw as a clean four-cell comparison if possible, preserving axes and qualitative shapes.
- 146: 3.1.1 DFS definition. Preserve forward transform and inverse transform:
  - \tilde{X}(k)=DFS[\tilde{x}(n)]=Σ_{n=0}^{N-1}\tilde{x}(n)e^{-j(2π/N)kn}, with red k range.
  - \tilde{x}(n)=IDFS[\tilde{X}(k)]=(1/N)Σ_{k=0}^{N-1}\tilde{X}(k)e^{j(2π/N)kn}, with red n range.
  Use rendered formulas; keep the distinction between periodic sequence symbols and DFS/IDFS.
- 147: DFS definition using twiddle factor W_N. Preserve W_N=e^{-j2π/N}, forward formula \tilde{X}(k)=Σ\tilde{x}(n)W_N^{kn}, inverse formula \tilde{x}(n)=(1/N)Σ\tilde{X}(k)W_N^{-kn}, and red k/n ranges. This page reinforces notation and must not be omitted as a duplicate.
- 148: visual relation between DTFT and DFS. Preserve the diagram showing time-domain discrete/nonperiodic sequence x(n), time-domain periodic sequence \tilde{x}_N(n), frequency-domain periodic continuous DTFT X(e^{jω}), frequency-domain discrete DFS samples \tilde{X}_N(k), DTFT/IDTFT and DFS/IDFS arrows, and the sampling relation \omega/(2π)=k/N with one-period N-point sampling.
- 149: DFS example. Preserve problem statement: real sequence x(n)=R_4(n), periodize it with N=8 to form \tilde{x}(n), and find DFS coefficients in one period. Preserve derivation \tilde{X}(k)=Σ_{n=0}^{7}R_4(n)W_8^{kn}=Σ_{0}^{3}W_8^{kn}=1+W_8^k+W_8^{2k}+W_8^{3k}, red k range, and all eight results: X(0)=4, X(1)=1-j(√2+1), X(2)=0, X(3)=1-j(√2-1), X(4)=0, X(5)=1+j(√2-1), X(6)=0, X(7)=1+j(√2+1).
- 150: 3.1.2 DFS properties opening. Preserve red explanation that DFS can be interpreted by z-transform at z=e^{j(2π/N)k}, so many DFS properties are similar to z-transform. Preserve assumptions X1(k)=DFS[x1(n)], X2(k)=DFS[x2(n)], then property names and formulas:
  - linearity: DFS[a x1(n)+b x2(n)]=aX1(k)+bX2(k).
  - time-domain shift: DFS[x(n+m)]=W_N^{-mk}X(k).
- 151: DFS properties continuation. Preserve the same red z-transform explanation banner and assumptions \tilde{X}_1(k)=DFS[\tilde{x}_1(n)], \tilde{X}_2(k)=DFS[\tilde{x}_2(n)]. Include property names and formulas:
  - (3) frequency-domain shift: DFS[W_N^{mn}\tilde{x}(n)] = \tilde{X}(k+m).
  - (4) periodic convolution sum: if \tilde{Y}(k)=\tilde{X}_1(k)\tilde{X}_2(k), then \tilde{y}(n)=IDFS[\tilde{Y}(k)]=sum_{m=0}^{N-1}\tilde{x}_1(m)\tilde{x}_2(n-m)=sum_{m=0}^{N-1}\tilde{x}_2(m)\tilde{x}_1(n-m). Render sums and tildes as formulas; do not omit property names.
- 152: 3.2 DFT definition, 3.2.1 definition page. Preserve heading "离散傅里叶变换（DFT）" and "定义". Include both labelled transforms:
  - 正变换: X(k)=DFT[x(n)]_N=sum_{n=0}^{N-1}x(n)W_N^{kn}, with red k in [0,N-1].
  - 反变换: x(n)=IDFT[X(k)]_N=(1/N)sum_{k=0}^{N-1}X(k)W_N^{-kn}, with red n in [0,N-1].
  Use rendered formulas and keep red range notes as important emphasis.
- 153: DFT example begins: "求下列长度为 N (N 为偶数) 的有限长序列的 N 点 DFT." Preserve both problem statements:
  - (1) x(n)=delta(n)+delta(n-n0), 0 <= n0 <= N-1.
  - (2) x(n)=1 for n even and 0 for n odd, both over 0 <= n <= N-1. Render as a piecewise function with the approved tight brace style.
  Preserve solution (1) direct DFT derivation: X(k)=sum_{n=0}^{N-1}x(n)W_N^{kn}=sum[delta(n)+delta(n-n0)]W_N^{kn}=W_N^{0k}+W_N^{n0 k}=1+W_N^{n0 k}, with red k in [0,N-1].
- 154: Same DFT example, solution (1) second method. Preserve z-transform route:
  - X(z)=1+z^{-n0}.
  - X(k)=X(z)|_{z=e^{j(2pi/N)k}}=1+e^{-j(2pi/N)k n0}, k in [0,N-1].
  Keep this as an alternative derivation, not a replacement for page 153's direct-sum derivation.
- 155: DFT example solution (2). Preserve the even-index piecewise problem and full derivation:
  - X(k)=sum_{n=0}^{N-1}x(n)W_N^{kn}=sum_{r=0}^{N/2-1}x(2r)W_N^{2rk}=sum_{r=0}^{N/2-1}W_N^{2rk}.
  - Convert to geometric-series fraction (1-W_N^{2k*(N/2)})/(1-W_N^{2k})=(1-W_N^{kN})/(1-W_N^{2k}).
  - Final piecewise result: N/2 for k=0,N/2 and 0 for other k, with k in [0,N-1]. Use the approved tight brace layout and fraction formatting.
- 156: IDFT example: given N-point DFT X(k), find inverse transform x(n). Preserve problem statements and both derivations:
  - (1) X(k)=delta(k): x(n)=(1/N)sum_{k=0}^{N-1}X(k)W_N^{-kn}=(1/N)sum delta(k)W_N^{-kn}=(1/N)W_N^{0*n}=1/N for n in [0,N-1], so x(n)=(1/N)R_N(n).
  - (2) X(k)=R_N(k): x(n)=(1/N)sum_{k=0}^{N-1}R_N(k)W_N^{-kn}=(1/N)*(1-W_N^{-Nn})/(1-W_N^{-n}), then piecewise 1 for n=0 and 0 for other n, so x(n)=delta(n)R_N(n).
  Preserve two-column logic if layout allows, but avoid source watermark/background.
- 157: 3.2.2 cyclic/circular shift definition. Preserve formula x_m(n)=x(((n+m))_N)R_N(n) and the three-step explanation:
  - x(n) periodic extension: \tilde{x}(n)=x(((n))_N).
  - shift: \tilde{x}(n+m)=x(((n+m))_N).
  - take principal-value sequence: x_m(n)=x(((n+m))_N)R_N(n).
  This stepwise explanation must stay; do not collapse it into only the final formula.
- 158: circular shift example problem statement. Preserve x(n)={1,2,3,4} and the four requested sequences:
  - x(((n+2))_8)R_8(n)
  - x(((n-2))_8)R_8(n)
  - x(((-n+2))_8)R_8(n)
  - x(((-n-2))_8)R_8(n)
  Preserve the red note: if sequence length is less than the requested N-point length, pad zeros to N points. This note is important and should remain red/emphasized.
- 159: circular shift example solution. Preserve all four resulting 8-point sequences and the n=0 marker/underline convention:
  - x(((n+2))_8)R_8(n) = {3,4,0,0,0,0,1,2}, with 3 as the n=0 entry.
  - x(((n-2))_8)R_8(n) = {0,0,1,2,3,4,0,0}, with first 0 as the n=0 entry.
  - x(((-n+2))_8)R_8(n) = {3,2,1,0,0,0,0,4}, with 3 as the n=0 entry.
  - x(((-n-2))_8)R_8(n) = {0,0,0,4,3,2,1,0}, with first 0 as the n=0 entry.
  In the handout, mark the n=0 entry clearly (underline or small "n=0" note) because the source underlines those entries.
- 160: 3.2.3 DFT basic properties begins. Preserve property name "(1) 线性性质". Include the if/then structure:
  - If y(n)=a x1(n)+b x2(n), then Y(k)=DFT[y(n)]=aX1(k)+bX2(k).
  Render both formulas as math, and keep the property name rather than only listing the formula.
- 161: DFT basic properties continuation. Preserve property names and formulas:
  - (2) time-domain shift: DFT[x(((n+m))_N)R_N(n)] = W_N^{-km}X(k).
  - (3) frequency-domain shift: DFT[W_N^{mn}x(n)] = X(((k+m))_N)R_N(k).
  Preserve the red note "牢记下面两个等式" and the two red formulas z=e^{jω}, ω=(2π/N)k. Keep them as emphasized review notes.
- 162: DFT property example problem statement. Preserve: If X(k) is the 4-point DFT of x(n), with x(n)={1,3/4,1/2,1/4} (n=0 entry underlined/marked), and if Y(k) is the 4-point DFT of y(n) with Y(k)=W_4^{3k}X(k), find y(n). Render all fractions as fractions; do not leave slash notation.
- 163: DFT property example solution. Preserve the derivation from frequency-domain factor to time-domain circular shift:
  - Y(k)=W_4^{3k}X(k)=e^{-j(2pi/4)k3}X(k) -> e^{-jω3}X(e^{-jω}) -> z^{-3}X(z).
  - Therefore y(n)=x(((n-3))_4)R_4(n)=x(((n+1))_4)R_4(n), with the second equality in red.
  - Final sequence y(n)={3/4,1/2,1/4,1}, with n=0 entry marked.
  Preserve the red reminder box/text: z=e^{jω} and ω=(2π/N)k.
- 164: Same example extension. Preserve original problem statement and red extension:
  - If the condition changes to Y(k)=W_2^k X(k), find y(n).
  - Preserve red answer y(n)={1/2,1/4,1,3/4}, with n=0 marker. This is source content and must not be dropped as an aside.
- 165: DFT basic property (4) conjugate symmetry, marked with a red star. Preserve the definition section:
  - conjugate symmetric: x_e(n)=x_e^*(-n).
  - conjugate anti-symmetric: x_o(n)=-x_o^*(-n).
  - From x(n), compute x_e(n)=[x(n)+x^*(-n)]/2 and x_o(n)=[x(n)-x^*(-n)]/2.
  Red star indicates importance; carry it into the handout as a key property marker or emphasized label.
- 166: DFT circular conjugate symmetry. Preserve as distinct from page 165:
  - DFT下的圆周共轭对称.
  - circular conjugate symmetric: x_ep(n)=x_ep^*(N-n).
  - circular conjugate anti-symmetric: x_op(n)=-x_op^*(N-n).
  - From x(n), compute x_ep(n)=[x(n)+x^*(N-n)]/2 and x_op(n)=[x(n)-x^*(N-n)]/2.
  Render every fraction as a fraction and keep the red-star importance.
- 167: Conjugate-symmetry correspondences. Preserve all three-line logic for both items:
  - If x(n)=x_r(n)+j x_i(n), and X(k)=X_ep(k)+X_op(k), then x_r(n) <-> X_ep(k), jx_i(n) <-> X_op(k).
  - If x(n)=x_ep(n)+x_op(n), and X(k)=X_r(k)+jX_i(k), then x_ep(n) <-> X_r(k), x_op(n) <-> jX_i(k).
  Keep as a compact correspondence table or aligned formulas; do not rewrite into vague prose.
- 168: Important special case under conjugate symmetry. Preserve the red emphasis:
  - If x(n) is a real sequence, then X(k)=X^*(N-k) (red, marked with three stars).
  - Therefore |X(k)|=|X(N-k)| and theta(k)=-theta(N-k).
  This is a high-priority 814 review note; keep the red formula and the magnitude/phase consequences.
- 169: Conjugate-symmetry example. Preserve problem statement and both solutions:
  - Given finite sequence x(n)={1,2,3,4}, its 6-point DFT is X(k); y(n)'s 6-point DFT is Y(k). Given Y(k)=Re[X(k)], find y(n).
  - Solution 1: from circular conjugate symmetry, y(n)=x_ep(n)=[x(n)+x^*(N-n)]/2={1,1,3/2,4,3/2,1}, with n=0 marker.
  - Solution 2: first form x_e(n)=[x(n)+x^*(-n)]/2={2,3/2,1,1,1,3/2,2}, then use circular conjugate symmetry and take x_ep(n)=x_e(((n))_6)R_6(n)={1,1,3/2,4,3/2,1}. Preserve both routes.
- 170: Example using one N-point DFT to compute two real-sequence DFTs. Preserve the problem and derivation:
  - x1(n) and x2(n) are both N-point real sequences; use one N-point DFT to calculate their respective DFTs.
  - Let y(n)=x1(n)+j x2(n). Then Y(k)=DFT[y(n)]=X1(k)+jX2(k).
  - Also Y(k)=Y_ep(k)+Y_op(k).
  - Therefore X1(k)=Y_ep(k)=1/2[Y(k)+Y^*(N-k)] and X2(k)=(1/j)Y_op(k)=1/(2j)[Y(k)-Y^*(N-k)].
  Preserve this as a method example; do not shorten to only the final two formulas.
- 171: Reverse method example: known DFTs X1(k), X2(k) of real sequences x1(n), x2(n), derive a method that uses one IDFT to obtain x1(n), x2(n). Preserve:
  - Let Y(k)=X1(k)+jX2(k).
  - Then y(n)=IDFT[Y(k)]=x1(n)+jx2(n).
  - Since x1(n), x2(n) are real sequences, x1(n)=Re[y(n)] and x2(n)=Im[y(n)].
- 172: 3.2.4 common N-point DFT transform pairs. Preserve all four red-arrow pairs:
  - delta(((n))_N)R_N(n) -> R_N(k).
  - delta(((n-m))_N)R_N(n) -> e^{-j(2pi/N)km}R_N(k).
  - 1*R_N(n) -> N delta(((k))_N)R_N(k).
  - e^{j(2pi/N)nm}R_N(n) -> N delta(((k-m))_N)R_N(k).
  Preserve the red memory note: the third pair is DC in time, so all spectral energy N is concentrated on the k=0 DC spectral line.
- 173: Common DFT-pair example. Preserve even if similar to page 156 because source repeats it in this subsection:
  - Given X(k)=delta(k) and X(k)=R_N(k), find inverse x(n).
  - Preserve both IDFT derivations and conclusions x(n)=(1/N)R_N(n) and x(n)=delta(n)R_N(n), including the piecewise result for the second item.
- 174: Common N-point DFT-pair example problem statement. Preserve: find the 10-point DFT of x(n)=cos((3pi/5)n) sin((4pi/5)n). Render products and fractions as math; the solution continues on later source pages and must connect naturally.
- 175: Solution to the 10-point DFT example. Preserve the full Euler expansion and simplification:
  - cos(3πn/5)sin(4πn/5) expanded into exponential products with denominators 2 and 2j.
  - Re-express exponents as e^{j(2π/10)7n}, e^{j(2π/10)n}, e^{-j(2π/10)n}, e^{-j(2π/10)7n}.
  - Final DFT result X(k)=10/(4j)[δ(k-7)+δ(k-1)-δ(k+1-10)-δ(k+7-10)] = 5/(2j)[δ(k-7)+δ(k-1)-δ(k-9)-δ(k-3)], k in [0,9].
  Keep all fractions rendered and do not collapse the derivation into only the final line.
- 176: Common DFT-pair inverse example problem statement. Preserve: a length-8 sequence x(n) is zero outside 0 <= n <= 7, and its 8-point DFT is X(k)=1+2sin(πk/4)+3cos(πk/2)+4sin(3πk/4). Find x(n). Render the given X(k) formula exactly with fractions.
- 177: Solution to the 8-point inverse example. Preserve the full sequence of steps:
  - Rewrite X(k)=1+2sin((2πk/8)*1)+3cos((2πk/8)*2)+4sin((2πk/8)*3).
  - Convert sin/cos terms into exponentials using denominators 2j and 2.
  - Simplify to 1 - j[e^{j(2πk/8)*1}-e^{j(2πk/8)*(-1)}] + 1.5[e^{j(2πk/8)*2}+e^{j(2πk/8)*(-2)}] - 2j[e^{j(2πk/8)*3}-e^{j(2πk/8)*(-3)}].
  - Convert to x(n)=δ(n)-jδ(n+1-8)+jδ(n-1)+1.5δ(n+2-8)+1.5δ(n-2)-2jδ(n+3-8)+2jδ(n-3), then simplify for n in [0,7].
  - Final sequence x(n)=[1,j,1.5,2j,0,-2j,1.5,-j], with n=0 marker.
- 178: 3.3 relationship among transforms, DFS and DFT relation. Preserve red heading "DFS和DFT的关系" and note "DFT由DFS导出". Preserve all three numbered explanations:
  1. For x(n), 0 <= n <= M-1, take an N-point DFT (N >= M); N-point periodic extension gives \tilde{x}(n), and DFS over any N-period gives \tilde{X}(k). The [0,N-1] period equals x(k) over 0 <= k <= N-1.
  2. In DFT processing, the sequence may first be periodically extended before the corresponding processing.
  3. DFT operations are equivalent to DFS operations on one period/main-value interval after periodic extension, except k has a range limit.
- 179: DFT, DTFT, and z-transform relationship. Preserve red heading "DFT和DTFT、Z变换的关系" and assumption: sequence x(n) has length M and is transformed by N-point DFT (N >= M). Preserve all formulas:
  - DFT: X(k)=sum_{n=0}^{N-1}x(n)e^{-j(2π/N)kn}.
  - DTFT: X(e^{jω})=sum_{n=0}^{N-1}x(n)e^{-jωn}.
  - z-transform: X(z)=sum_{n=0}^{N-1}x(n)z^{-n}.
  - Relationship: X(k)=X(e^{jω})|_{ω=k(2π/N)}=X(z)|_{z=e^{j(2π/N)k}}.
  Preserve bottom explanation: the DFT is uniform sampling of the DTFT from 0 to 2π at spacing 2π/N, and is N samples on the z-transform unit circle.
- 180: Relationship example begins. Preserve problem statement: let x(n)=R_5(n); find (1) X(e^{jω}), (2) x(k) for N=5, (3) x(k) for N=10. Preserve solution part (1):
  - X(e^{jω})=sum_{n=0}^{4}e^{-jωn}
  - =(1-e^{-j5ω})/(1-e^{-jω})
  - = e^{-j5ω/2}(e^{j5ω/2}-e^{-j5ω/2}) / [e^{-jω/2}(e^{jω/2}-e^{-jω/2})]
  - = e^{-j2ω} sin(5ω/2)/sin(ω/2)
  This example continues after source page 180, so do not terminate the generated section here.
- 181: Continuation of page 180 example. Preserve solution part (2): N=5 DFT is the 5 equally spaced samples of X(e^{jω}).
  - X(e^{jω})=e^{-j2ω} sin(5ω/2)/sin(ω/2).
  - X(k)=X(e^{jω})|_{ω=2πk/5}=e^{-j4πk/5} sin(πk)/sin(πk/5).
  - Piecewise result: 5 for k=0 and 0 for k=1,2,3,4. Use the approved piecewise brace style.
- 182: Continuation of page 180 example. Preserve solution part (3): N=10 DFT is the 10 equally spaced samples of X(e^{jω}).
  - X(e^{jω})=e^{-j2ω} sin(5ω/2)/sin(ω/2).
  - x(k)=x(e^{jω})|_{ω=2πk/10}=e^{-j2πk/5} sin(πk/2)/sin(πk/10), 0 <= k <= 9.
  Source page stops at this expression; keep it as the N=10 answer unless a following page further evaluates it.
- 183: Section mind map / recap for DFT relationships. Preserve as a compact chapter-map page or summary block:
  - DFS branch: definition, properties, reminder that computers can only process discrete data, leading to DFS; DTFT is discrete in time and sampled in frequency to obtain DFS. Notes "严谨说法参考教材" should be retained as a caution/reference note.
  - DFT branch: definition, properties including linearity, circular shift, circular conjugate symmetry, common transform pairs, and reminders that DFT is obtained from DFS on the main-value interval and that one period of a periodic sequence determines the whole periodic sequence.
  - Preserve the final note about remembering transform relationships according to different custom definitions.
- 184: After-class exercises for the DFT section. Preserve exercise list and formula:
  - 3-1 求序列DFT.
  - 3-2 求X(k), with modified item (2) piecewise X(k): -N/2*j*e^{jθ} for k=m; N/2*j*e^{-jθ} for k=N-m; 0 for other k. Render with approved brace style and Chinese "其他 k".
  - 3-15 实序列的DFT及DFT的性质.
  - 3-16 利用DFT的性质求DFT.
  - 3-23 DFT和DTFT的关系.
