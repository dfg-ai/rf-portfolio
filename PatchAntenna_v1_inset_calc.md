# 内嵌馈电凹槽计算

## 原理
贴片内部电场呈余弦分布，阻抗从边缘向内下降：
$$R_{in}(y_0) = R_{edge} \cdot \cos^2\left(\frac{\pi \cdot y_0}{L}\right)$$

## 计算
- R_edge ≈ 200 Ω（估算，FR4 会偏低一点）
- 目标 Rin = 50 Ω
- L = 28 mm

$$50 = 200 \cdot \cos^2\left(\frac{\pi \cdot y_0}{28}\right)$$

$$\cos^2 = 0.25 \implies \cos = 0.5 \implies \frac{\pi \cdot y_0}{28} = \frac{\pi}{3}$$

$$y_0 = \frac{28}{3} = 9.33 \text{ mm}$$

> 馈线需要伸进贴片约 9.3mm，两侧各留 ~1.5mm 间隙 → 凹槽宽 3mm+3mm+3.1mm？不...
> 
> 实际做法：馈线宽 3.1mm，凹槽宽度 = 馈线宽 + 两侧间隙 = 3.1 + 2×1.5 = 6.1mm
> 凹槽深度 = 9.3mm

## 尺寸汇总
| 参数 | 值 |
|------|-----|
| Lp (贴片长度) | **28 mm** |
| 凹槽宽度 (gap × 2 + feed) | **6.1 mm** |
| 凹槽深度 (inset depth) | **9.3 mm** |
| 馈线长度 (从基板边缘到凹槽底) | **5 + 9.3 = 14.3 mm** |
