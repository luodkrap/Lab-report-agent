"""
베르누이 실험 문항 1-1: 이론 유량 계산 및 유량계수 산정
- 벤투리미터 원리를 이용한 이론 유량 계산
- 실제 유량과 비교하여 유량계수(C_d) 산정
- 시각화 그래프 생성
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.rcParams['font.family'] = 'AppleGothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# === 실험 데이터 ===
Q_actual_LPM = 10.8  # 실제 유량 (LPM)
Q_actual = Q_actual_LPM / 60000  # m^3/s
g = 9.81  # m/s^2

inlet_height = 304  # mm (입구수조 높이)
outlet_height = 213  # mm (출구수조 높이)

# 액주계 높이 (mm) - M1~M24
h_manometer = np.array([
    272, 270, 265, 259, 254, 244, 237, 226, 211, 187,
    160, 111, 125, 159, 175, 187, 195, 201, 206, 210,
    213, 216, 218, 220
])

# 벤투리관 단면적 (m^2) - 제원표 기반
areas = np.array([
    0.000295, 0.000278, 0.000261, 0.000244, 0.000227,
    0.000210, 0.000193, 0.000176, 0.000159, 0.000142,
    0.000125, 0.000108, 0.000125, 0.000142, 0.000159,
    0.000176, 0.000193, 0.000210, 0.000227, 0.000244,
    0.000261, 0.000278, 0.000295, 0.000312
])

# 벤투리관 Z 높이 (mm) - 단면 높이 (폭 12mm)
Z_heights = np.array([
    24.583, 23.167, 21.750, 20.333, 18.917,
    17.500, 16.083, 14.667, 13.250, 11.833,
    10.417, 9.000, 10.417, 11.833, 13.250,
    14.667, 16.083, 17.500, 18.917, 20.333,
    21.750, 23.167, 24.583, 26.000
])

labels = [f'M{i}' for i in range(1, 25)]

# === 이론 유량 계산 (M1-M12 기준) ===
A1 = areas[0]   # M1 단면적
A2 = areas[11]  # M12 단면적 (throat)
h1 = h_manometer[0] / 1000   # m
h2 = h_manometer[11] / 1000  # m
delta_h = h1 - h2  # 수두차 (m)

# Q_ideal = (A1 * A2) / sqrt(A1^2 - A2^2) * sqrt(2g * delta_h)
Q_ideal = (A1 * A2) / np.sqrt(A1**2 - A2**2) * np.sqrt(2 * g * delta_h)
Q_ideal_LPM = Q_ideal * 60000

C_d = Q_actual / Q_ideal
error_pct = abs(Q_ideal_LPM - Q_actual_LPM) / Q_actual_LPM * 100

print("=" * 60)
print("문항 1-1: 이론 유량 계산 및 유량계수 산정")
print("=" * 60)
print(f"\n[입력 데이터]")
print(f"  실제 유량 (Q_actual)    = {Q_actual_LPM} LPM")
print(f"  입구수조 높이           = {inlet_height} mm")
print(f"  출구수조 높이           = {outlet_height} mm")
print(f"\n[벤투리미터 제원]")
print(f"  상류부 (M1)  단면적 A₁  = {A1:.6e} m²")
print(f"  목 (M12)    단면적 A₂  = {A2:.6e} m²")
print(f"  면적비 A₂/A₁           = {A2/A1:.4f}")
print(f"\n[수두 데이터]")
print(f"  M1  정압수두 h₁        = {h1*1000:.0f} mm = {h1:.3f} m")
print(f"  M12 정압수두 h₂        = {h2*1000:.0f} mm = {h2:.3f} m")
print(f"  수두차 Δh = h₁ - h₂   = {delta_h*1000:.0f} mm = {delta_h:.3f} m")
print(f"\n[이론 유량 계산]")
print(f"  Q_ideal = (A₁·A₂)/√(A₁²-A₂²) × √(2g·Δh)")
print(f"  A₁·A₂                 = {A1*A2:.6e} m⁴")
print(f"  A₁² - A₂²             = {A1**2 - A2**2:.6e} m⁴")
print(f"  √(A₁² - A₂²)         = {np.sqrt(A1**2 - A2**2):.6e} m²")
print(f"  √(2g·Δh)             = {np.sqrt(2*g*delta_h):.4f} m/s")
print(f"  Q_ideal               = {Q_ideal:.6e} m³/s")
print(f"  Q_ideal               = {Q_ideal_LPM:.3f} LPM")
print(f"\n[결과]")
print(f"  유량계수 C_d = Q_actual / Q_ideal = {C_d:.4f}")
print(f"  오차율                 = {error_pct:.2f}%")

# === 다양한 상류 지점별 이론 유량 계산 ===
print(f"\n{'='*60}")
print("다양한 상류 지점 기준 이론 유량 비교")
print(f"{'='*60}")
print(f"{'상류지점':^8} | {'A_up (m²)':^14} | {'Δh (mm)':^10} | {'Q_ideal (LPM)':^14} | {'C_d':^8}")
print("-" * 65)

upstream_points = [0, 1, 2, 3, 4, 5]  # M1 ~ M6
Q_ideals_upstream = []
Cd_upstream = []
for i in upstream_points:
    A_up = areas[i]
    A_throat = areas[11]
    dh = (h_manometer[i] - h_manometer[11]) / 1000
    if dh > 0:
        Q_th = (A_up * A_throat) / np.sqrt(A_up**2 - A_throat**2) * np.sqrt(2 * g * dh)
        Q_th_LPM = Q_th * 60000
        cd = Q_actual / Q_th
        Q_ideals_upstream.append(Q_th_LPM)
        Cd_upstream.append(cd)
        print(f"  M{i+1:>2}    | {A_up:.6e}  | {dh*1000:>8.0f}  | {Q_th_LPM:>12.3f}  | {cd:>6.4f}")

# === 시각화 ===
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp', 'figures')
os.makedirs(output_dir, exist_ok=True)

# --- 그래프 1: 벤투리관 단면 형상 + 액주계 수두 분포 ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [1, 1.5]})

# 상단: 벤투리관 단면 형상
x_pos = np.arange(1, 25)
half_z = Z_heights / 2
ax1.fill_between(x_pos, -half_z, half_z, alpha=0.3, color='steelblue', label='벤투리관 단면')
ax1.plot(x_pos, half_z, 'b-', linewidth=1.5)
ax1.plot(x_pos, -half_z, 'b-', linewidth=1.5)
ax1.set_ylabel('단면 높이 Z/2 (mm)', fontsize=11)
ax1.set_title('벤투리관 단면 형상 및 정압수두 분포', fontsize=14, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(labels, fontsize=8, rotation=45)
ax1.axvline(x=12, color='red', linestyle='--', alpha=0.5, label='목(Throat) M12')
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)

# 하단: 액주계 높이 분포
colors = ['#2196F3' if i < 11 else '#F44336' if i == 11 else '#4CAF50' for i in range(24)]
bars = ax2.bar(x_pos, h_manometer, color=colors, alpha=0.8, edgecolor='white', linewidth=0.5)
ax2.axhline(y=inlet_height, color='orange', linestyle='--', linewidth=1.5, label=f'입구수조 높이 ({inlet_height} mm)')
ax2.axhline(y=outlet_height, color='purple', linestyle='--', linewidth=1.5, label=f'출구수조 높이 ({outlet_height} mm)')

# 수두차 화살표 표시
ax2.annotate('', xy=(12, h_manometer[11]), xytext=(12, h_manometer[0]),
             arrowprops=dict(arrowstyle='<->', color='red', lw=2))
ax2.text(12.5, (h_manometer[0] + h_manometer[11]) / 2, f'Δh = {delta_h*1000:.0f} mm',
         fontsize=10, color='red', fontweight='bold', va='center')

ax2.set_xlabel('액주계 위치', fontsize=11)
ax2.set_ylabel('정압수두 h (mm)', fontsize=11)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(labels, fontsize=8, rotation=45)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'q1_venturi_pressure.png'), dpi=200, bbox_inches='tight')
plt.close()
print(f"\n[그래프 1 저장] {os.path.join(output_dir, 'q1_venturi_pressure.png')}")

# --- 그래프 2: 유량 비교 차트 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 좌측: 이론 vs 실제 유량 비교
bar_labels = ['이론 유량\n(Q_ideal)', '실제 유량\n(Q_actual)']
bar_values = [Q_ideal_LPM, Q_actual_LPM]
bar_colors = ['#FF7043', '#42A5F5']
bars = ax1.bar(bar_labels, bar_values, color=bar_colors, width=0.5, edgecolor='white', linewidth=2)
ax1.set_ylabel('유량 (LPM)', fontsize=12)
ax1.set_title('이론 유량 vs 실제 유량', fontsize=13, fontweight='bold')

for bar, val in zip(bars, bar_values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
             f'{val:.2f} LPM', ha='center', va='bottom', fontsize=11, fontweight='bold')

# C_d 표시
ax1.text(0.5, max(bar_values) * 0.5, f'$C_d$ = {C_d:.4f}',
         ha='center', fontsize=14, fontweight='bold', color='green',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='green'),
         transform=ax1.get_xaxis_transform())

ax1.set_ylim(0, max(bar_values) * 1.25)
ax1.grid(True, alpha=0.3, axis='y')

# 우측: 다양한 상류 지점별 C_d
upstream_labels = [f'M{i+1}-M12' for i in upstream_points]
ax2.bar(upstream_labels, Cd_upstream, color='#66BB6A', alpha=0.85, edgecolor='white', linewidth=1.5)
ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=1, label='이상 유량계수 (C_d = 1)')
ax2.axhline(y=np.mean(Cd_upstream), color='blue', linestyle=':', linewidth=1.5,
            label=f'평균 C_d = {np.mean(Cd_upstream):.4f}')
ax2.set_ylabel('유량계수 $C_d$', fontsize=12)
ax2.set_title('상류 기준점별 유량계수 비교', fontsize=13, fontweight='bold')
ax2.legend(fontsize=9)
ax2.set_ylim(0.7, 1.15)
ax2.grid(True, alpha=0.3, axis='y')

for i, (lbl, cd) in enumerate(zip(upstream_labels, Cd_upstream)):
    ax2.text(i, cd + 0.01, f'{cd:.3f}', ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'q1_flow_comparison.png'), dpi=200, bbox_inches='tight')
plt.close()
print(f"[그래프 2 저장] {os.path.join(output_dir, 'q1_flow_comparison.png')}")

# --- 그래프 3: 벤투리관 단면적 변화와 압력 분포 관계 ---
fig, ax1 = plt.subplots(figsize=(12, 5))
ax2_twin = ax1.twinx()

line1, = ax1.plot(x_pos, areas * 1e6, 'b-o', markersize=5, linewidth=2, label='단면적 A (mm²)')
line2, = ax2_twin.plot(x_pos, h_manometer, 'r-s', markersize=5, linewidth=2, label='정압수두 h (mm)')

ax1.set_xlabel('액주계 위치', fontsize=11)
ax1.set_ylabel('단면적 A (mm²)', fontsize=11, color='blue')
ax2_twin.set_ylabel('정압수두 h (mm)', fontsize=11, color='red')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(labels, fontsize=8, rotation=45)
ax1.set_title('단면적 변화와 정압수두 분포의 상관관계', fontsize=14, fontweight='bold')

ax1.tick_params(axis='y', labelcolor='blue')
ax2_twin.tick_params(axis='y', labelcolor='red')

lines = [line1, line2]
ax1.legend(lines, [l.get_label() for l in lines], loc='upper center', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.axvline(x=12, color='gray', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'q1_area_pressure_relation.png'), dpi=200, bbox_inches='tight')
plt.close()
print(f"[그래프 3 저장] {os.path.join(output_dir, 'q1_area_pressure_relation.png')}")

print(f"\n{'='*60}")
print("모든 계산 및 시각화 완료")
print(f"{'='*60}")
