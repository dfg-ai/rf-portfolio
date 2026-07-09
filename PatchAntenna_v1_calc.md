# 矩形微带贴片天线 — 初始尺寸计算

> 设计频率: 2.44 GHz | 基板: FR4 (εr=4.4, h=1.6mm)

## 1. 贴片宽度 W

$$W = \frac{c}{2f_0} \sqrt{\frac{2}{\varepsilon_r + 1}}$$

$$= \frac{3 \times 10^{11}}{2 \times 2.44 \times 10^9} \sqrt{\frac{2}{5.4}}$$

$$= 61.48 \times 0.6086 = \boxed{37.42 \text{ mm}}$$

> W 选得略小可以减小面积，但不能太小否则效率下降。W < 38mm 时可能激励高次模，37.4mm 在合理范围。

## 2. 有效介电常数 εeff

$$\varepsilon_{eff} = \frac{\varepsilon_r+1}{2} + \frac{\varepsilon_r-1}{2}\left[1 + 12\frac{h}{W}\right]^{-1/2}$$

$$= 2.7 + 1.7 \times [1 + 0.513]^{-1/2}$$

$$= 2.7 + 1.7 \times 0.813 = \boxed{4.08}$$

## 3. 延伸长度 ΔL

$$\Delta L = 0.412h \cdot \frac{(\varepsilon_{eff}+0.3)(\frac{W}{h}+0.264)}{(\varepsilon_{eff}-0.258)(\frac{W}{h}+0.8)}$$

$$= 0.6592 \times \frac{4.382 \times 23.65}{3.824 \times 24.19}$$

$$= 0.6592 \times 1.1206 = \boxed{0.739 \text{ mm}}$$

## 4. 贴片长度 L

$$L = \frac{c}{2f_0\sqrt{\varepsilon_{eff}}} - 2\Delta L$$

$$= \frac{61.48}{2.0204} - 1.478$$

$$= 30.43 - 1.478 = \boxed{28.95 \text{ mm}}$$

## 5. 接地平面

$$W_g = W + 6h = 37.42 + 9.6 \approx \boxed{47 \text{ mm}}$$
$$L_g = L + 6h = 28.95 + 9.6 \approx \boxed{39 \text{ mm}}$$

## 6. 50Ω 微带馈线宽度

使用微带线特征阻抗公式反推（FR4: εr=4.4, h=1.6mm, Z₀=50Ω）:

$$W_f \approx \boxed{3.1 \text{ mm}}$$

## 汇总

| 参数 | 值 |
|------|-----|
| 贴片宽度 W | **37.4 mm** |
| 贴片长度 L | **29.0 mm** |
| 基板宽度 Wg | **47 mm** |
| 基板长度 Lg | **39 mm** |
| 基板厚度 h | **1.6 mm** |
| 馈线宽度 Wf | **3.1 mm** |
| 馈线长度 Lf | ~15-20 mm |

## 面试要点

- 传输线模型是最简单的微带天线分析方法
- 贴片长度约 λ/2（在介质中）= c/(2f₀√εeff) ≈ 30.4mm
- 边缘场效应导致有效长度增加 → 实际物理长度要减去 2ΔL
- FR4 在 2.4GHz 损耗较高（tanδ=0.02），效率会偏低，这是已知 trade-off
