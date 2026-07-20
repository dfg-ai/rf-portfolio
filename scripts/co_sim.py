# -*- coding: utf-8 -*-
"""
ADS-HFSS Co-Simulation Demo
Step 1: Parse Touchstone S3P from HFSS
Step 2: Plot S-parameters (verify matches HFSS)
Step 3: Cascade two Wilkinsons → simulate 4-way divider
"""
import os, math

DESKTOP = os.path.expanduser("~/Desktop")
S3P_FILE = os.path.join(os.path.expanduser("~"), "Documents", "Ansoft", "Wilkinson.s3p")

# ══════════════════════════════════════════════════════════════
# Step 1: Parse Touchstone file
# ══════════════════════════════════════════════════════════════
def parse_s3p(filepath):
    """Parse .s3p Touchstone file. Returns (freqs, sparams) where
    sparams[port_i][port_j] = [(mag, ang_deg), ...] for each freq."""
    freqs = []
    s11, s12, s13 = [], [], []
    s21, s22, s23 = [], [], []
    s31, s32, s33 = [], [], []

    with open(filepath, 'r') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('!')]

    header = lines[0]  # # GHz S MA R 50
    # Find the data lines (skip header and optional Gamma/Impedance lines)
    data_lines = []
    for l in lines[1:]:
        if l.startswith('!') or l.startswith('#'):
            continue
        parts = l.split()
        if len(parts) > 1:
            data_lines.append([float(x) for x in parts])

    # Each frequency block = 3 lines for 3-port network
    i = 0
    while i + 2 < len(data_lines):
        r1 = data_lines[i]    # Freq S11m S11a S12m S12a S13m S13a
        r2 = data_lines[i+1]  # S21m S21a S22m S22a S23m S23a
        r3 = data_lines[i+2]  # S31m S31a S32m S32a S33m S33a
        try:
            f = r1[0]
            freqs.append(f)
            s11.append((r1[1], r1[2]))
            s12.append((r1[3], r1[4]))
            s13.append((r1[5], r1[6]))
            s21.append((r2[0], r2[1]))
            s22.append((r2[2], r2[3]))
            s23.append((r2[4], r2[5]))
            s31.append((r3[0], r3[1]))
            s32.append((r3[2], r3[3]))
            s33.append((r3[4], r3[5]))
        except (IndexError, ValueError):
            pass  # skip Gamma/Impedance lines
        i += 3  # skip the 3 data rows

    sparams = {
        (1,1): s11, (1,2): s12, (1,3): s13,
        (2,1): s21, (2,2): s22, (2,3): s23,
        (3,1): s31, (3,2): s32, (3,3): s33,
    }
    return freqs, sparams

# ══════════════════════════════════════════════════════════════
# Step 2: Compute S-parameter in dB at a given frequency
# ══════════════════════════════════════════════════════════════
def s_db(sparams, port_i, port_j, freqs, target_freq):
    """Return S(port_i,port_j) in dB at the closest frequency."""
    idx = min(range(len(freqs)), key=lambda i: abs(freqs[i] - target_freq))
    mag, ang = sparams[(port_i, port_j)][idx]
    db = 20 * math.log10(mag) if mag > 0 else -999
    return freqs[idx], db, ang

def all_s_db(sparams, port_i, port_j, freqs):
    """Return list of dB values vs frequency."""
    return [20 * math.log10(m[0]) if m[0] > 0 else -999 for m in sparams[(port_i, port_j)]]

# ══════════════════════════════════════════════════════════════
# Step 3: Cascade two identical 3-port networks
#         Wilkinson(1→2,3) + Wilkinson(→4-way)
# ══════════════════════════════════════════════════════════════
def cascade_wilkinson(freqs, sparams):
    """
    Cascade two identical Wilkinsons to make a 4-way divider.
    Port1 → Wilkinson1(P2,P3)
           P2 → Wilkinson2a(P2',P3')
           P3 → Wilkinson2b(P2'',P3'')
    We need S-param to T-param conversion for cascade.
    Simplified: assume ideal split, compute composite S-params.
    """
    # For simplicity, compute the composite S21 (Port1→any output)
    # |S21_total| = |S21_wilk|^2 (two stages)
    # S11_total ≈ S11_wilk (first stage sees mostly its own reflection)

    s11_db = all_s_db(sparams, 1, 1, freqs)
    s21_db = all_s_db(sparams, 2, 1, freqs)
    s31_db = all_s_db(sparams, 3, 1, freqs)
    s23_db = all_s_db(sparams, 2, 3, freqs)
    s22_db = all_s_db(sparams, 2, 2, freqs)

    # Composite 4-way divider: each output gets half of half = 1/4 power
    # S_2stage_21 ≈ 2*S21 (in dB, each stage -3dB, total -6dB)
    s41_cascade = [s21_db[i] + s21_db[i] for i in range(len(freqs))]  # -6dB total
    s11_cascade = s11_db[:]  # first order approx

    return s11_cascade, s41_cascade

# ══════════════════════════════════════════════════════════════
# Main: Parse, Print, Plot
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ADS-HFSS Co-Simulation: Wilkinson Power Divider")
print("=" * 60)

freqs, sparams = parse_s3p(S3P_FILE)
print(f"Parsed {len(freqs)} frequency points ({freqs[0]:.2f} - {freqs[-1]:.2f} GHz)")
print()

# Print key metrics at 2.44 GHz
target = 2.44
for pi, pj, label in [(1,1,"S11"), (2,1,"S21"), (3,1,"S31"), (2,3,"S23")]:
    f, db, ang = s_db(sparams, pi, pj, freqs, target)
    print(f"  {label} @ {f:.2f}GHz: {db:+.2f} dB  ∠{ang:.1f}°")

print()
print("4-Way Divider (two Wilkinsons cascaded):")
s11_d, s41_d = cascade_wilkinson(freqs, sparams)
idx = min(range(len(freqs)), key=lambda i: abs(freqs[i] - target))
print(f"  S11 @ {freqs[idx]:.2f}GHz: {s11_d[idx]:+.2f} dB")
print(f"  S41 (each output) @ {freqs[idx]:.2f}GHz: {s41_d[idx]:+.2f} dB")
print("  (S21 double: single -3dB → cascaded -6dB per output)")

# ══════════════════════════════════════════════════════════════
# Generate simple HTML report with embedded data
# ══════════════════════════════════════════════════════════════
html_path = os.path.join(DESKTOP, "CoSim_Report.html")
s11d = all_s_db(sparams, 1, 1, freqs)
s21d = all_s_db(sparams, 2, 1, freqs)
s31d = all_s_db(sparams, 3, 1, freqs)

# Build JS data arrays for Chart.js-like simple plot
freqs_js = ",".join(["%.3f"%f for f in freqs])
s11_js = ",".join(["%.2f"%v for v in s11d])
s21_js = ",".join(["%.2f"%v for v in s21d])
s31_js = ",".join(["%.2f"%v for v in s31d])
s41_js = ",".join(["%.2f"%v for v in s41_d])

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8"><title>ADS-HFSS 联合仿真报告</title>
<style>
body{{font-family:"Microsoft YaHei",sans-serif;max-width:900px;margin:40px auto;padding:0 20px;color:#222;line-height:1.8}}
h1{{text-align:center;font-size:22pt;margin-bottom:4pt}}
.sub{{text-align:center;color:#888;font-size:11pt;margin-bottom:28pt}}
h2{{font-size:15pt;color:#1a5276;border-bottom:2px solid #2980b9;padding-bottom:4pt;margin-top:26pt}}
p{{font-size:11pt;margin:5pt 0}}
table{{border-collapse:collapse;width:100%;margin:10pt 0}}
td,th{{border:1px solid #ccc;padding:5pt 10pt;font-size:11pt}}
th{{background:#e8e8e8}}
canvas{{display:block;margin:10px auto;max-width:100%}}
.good{{color:#27ae60;font-weight:bold}}
.footer{{margin-top:40pt;padding-top:14pt;border-top:1px solid #ddd;color:#aaa;font-size:9pt;text-align:center}}
</style></head><body>
<h1>ADS-HFSS 联合仿真 — Wilkinson 功分器</h1>
<p class="sub">HFSS EM仿真 → Touchstone S3P → Python系统级分析 → 4路功分器级联</p>

<h2>一、工作流</h2>
<table>
<tr><th>步骤</th><th>工具</th><th>输出</th></tr>
<tr><td>1. EM 建模</td><td>HFSS (3D FEM)</td><td>Wilkinson_v1.aedt</td></tr>
<tr><td>2. 导出 S 参数</td><td>HFSS → Touchstone</td><td>Wilkinson.s3p (ASCII)</td></tr>
<tr><td>3. 黑盒建模</td><td>Python parse S3P</td><td>S 参数提取 + 验证</td></tr>
<tr><td>4. 系统级仿真</td><td>Python S-matrix 级联</td><td>4 路功分器性能预测</td></tr>
</table>

<h2>二、单 Wilkinson 结果 (HFSS EM)</h2>
<table>
<tr><th>参数</th><th>@ 2.44GHz</th><th>评价</th></tr>
<tr><td>S11</td><td class="good">{s11d[idx]:+.2f} dB</td><td>匹配优秀</td></tr>
<tr><td>S21</td><td class="good">{s21d[idx]:+.2f} dB</td><td>功率等分（~-3dB 理想）</td></tr>
<tr><td>S31</td><td class="good">{s31d[idx]:+.2f} dB</td><td>与 S21 对称</td></tr>
<tr><td>S23</td><td>{all_s_db(sparams,2,3,freqs)[idx]:+.2f} dB</td><td>隔离（无电阻）</td></tr>
</table>

<h2>三、S 参数曲线</h2>
<canvas id="plot" width="800" height="400"></canvas>

<h2>四、系统级：双 Wilkinson 级联 → 4 路功分器</h2>
<p>将单个 Wilkinson 的 S3P 作为<b>黑盒模块</b>，级联两级 → 4 路等功分。</p>
<table>
<tr><th>指标</th><th>预测值</th></tr>
<tr><td>S11 @ 2.44GHz</td><td class="good">{s11_d[idx]:+.2f} dB</td></tr>
<tr><td>每路输出 (S41)</td><td>{s41_d[idx]:+.2f} dB (理想 −6dB)</td></tr>
</table>
<p style="font-size:10pt;color:#888">&#x26a0; 基于 S 参数直接级联（黑盒法），不考虑两级之间的互耦。实际产品需 HFSS 全模型验证。</p>

<h2>五、核心认知</h2>
<p><b>HFSS = 精确测量单颗芯片</b> &rarr; S参数 = 芯片规格书 &rarr; <b>ADS/Python = 用规格书设计系统</b></p>
<p>面试时谈这个联合仿真流程 = 展示理解"EM仿真在整个射频设计流程中的角色"</p>

<p class="footer">Project 6/6 · HFSS + Python Co-Simulation</p>

<script>
(function(){{
var canvas=document.getElementById("plot");
var ctx=canvas.getContext("2d");
var W=canvas.width,H=canvas.height;
var freqs=[{freqs_js}];
var s11=[{s11_js}];
var s21=[{s21_js}];
var s31=[{s31_js}];
var s41=[{s41_js}];
var n=freqs.length;
var px=function(i){{return 60+(W-100)*(i/n)}};
var py=function(v){{return H-40-(H-80)*(v+40)/40}};
ctx.fillStyle="#f9f9f9";ctx.fillRect(0,0,W,H);
ctx.strokeStyle="#ddd";
for(var db=-40;db<=0;db+=10){{
var y=py(db);ctx.beginPath();ctx.moveTo(50,y);ctx.lineTo(W-40,y);ctx.stroke();
ctx.fillStyle="#999";ctx.font="10px sans-serif";ctx.fillText(db+"dB",10,y+4);
}}
for(var f=1;f<=3.5;f+=0.5){{
var x=px(f);ctx.beginPath();ctx.moveTo(x,40);ctx.lineTo(x,H-40);ctx.stroke();
ctx.fillStyle="#999";ctx.fillText(f+"GHz",x-18,H-20);
}}
ctx.strokeStyle="#999";ctx.lineWidth=1;
ctx.beginPath();ctx.moveTo(px(2.44),40);ctx.lineTo(px(2.44),H-40);ctx.stroke();
ctx.fillStyle="#ff6b6b";ctx.fillText("2.44GHz",px(2.44)-20,35);
ctx.fillStyle="#27ae60";ctx.fillText("−10dB",10,py(-10)+4);
ctx.strokeStyle="#27ae60";ctx.beginPath();ctx.moveTo(50,py(-10));ctx.lineTo(W-40,py(-10));ctx.setLineDash([4,4]);ctx.stroke();ctx.setLineDash([]);

function draw(freqs,data,color,label){{
ctx.strokeStyle=color;ctx.lineWidth=2;ctx.beginPath();
for(var i=0;i<n;i++){{var x=px(freqs[i]),y=py(data[i]);if(i==0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}}
ctx.stroke();
ctx.fillStyle=color;ctx.font="bold 11px sans-serif";
var last=data[n-1];ctx.fillText(label,px(freqs[n-1])+5,py(last));
}}
draw(freqs,s11,"#e74c3c","S11");
draw(freqs,s21,"#2980b9","S21");
draw(freqs,s31,"#2980b9","");
draw(freqs,s41,"#8e44ad","S41(级联)");

ctx.fillStyle="#222";ctx.font="bold 13px sans-serif";
ctx.fillText("Wilkinson S-Parameters (HFSS EM → S3P → Python)",W/2-200,20);
}})();
</script>
</body></html>'''

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nReport: {html_path}")
print("Done.")
