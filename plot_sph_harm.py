import numpy as np                      # 数値計算ライブラリ
import matplotlib.pyplot as plt         # グラフ描画ライブラリ
from scipy.special import sph_harm      # 球面調和関数 Y_l^m の計算関数

# θ（0〜π）と φ（0〜2π）の80点グリッドを作成し、2次元メッシュに展開
T, P = np.meshgrid(np.linspace(0, np.pi, 80), np.linspace(0, 2*np.pi, 80))

def Yr(l, m):
    """実球面調和関数: m>0 → cos(mφ)型、m<0 → sin(|m|φ)型"""
    # scipy は符号付き m を受け取らないため |m| で複素 Y_l^{|m|} を計算
    Y = sph_harm(abs(m), l, P, T)
    # m>0: 実部を取り √2 倍 → cos(mφ) 成分（例: p_x, d_{x²-y²}）
    if m > 0:   return np.sqrt(2) * Y.real
    # m<0: 虚部を取り √2 倍 → sin(|m|φ) 成分（例: p_y, d_{xy}）
    elif m < 0: return np.sqrt(2) * Y.imag
    # m=0: 実部のみ（元から実数、例: p_z, d_{z²}）
    return Y.real

def Yc(l, m):
    """複素球面調和関数 Y_l^m をそのまま返す（戻り値は複素数配列）"""
    # scipy の引数順: sph_harm(m, l, φ, θ)
    return sph_harm(m, l, P, T)

def plot_surface(ax, vals, color_vals, cmap, title):
    """球面プロット: 動径 r=|Y| で形を、color_vals で色を決定"""
    R = np.abs(vals)                    # 動径 = 球面調和関数の絶対値
    # 極座標 → デカルト座標変換: x=r sinθ cosφ, y=r sinθ sinφ, z=r cosθ
    x, y, z = R*np.sin(T)*np.cos(P), R*np.sin(T)*np.sin(P), R*np.cos(T)
    # color_vals を [0, 1] に正規化してカラーマップに渡す
    norm = plt.Normalize(color_vals.min(), color_vals.max())
    # 3Dサーフェスを描画（linewidth=0 で格子線なし、alpha で半透明）
    ax.plot_surface(x, y, z, facecolors=cmap(norm(color_vals)), linewidth=0, alpha=0.9)
    ax.set_title(title, fontsize=8)     # サブプロットのタイトルを設定
    ax.set_axis_off()                   # 軸・目盛りを非表示にする

# 描画する (l, m) の組み合わせ: l=0,1,2 の全量子数
cases = [(0,0), (1,-1),(1,0),(1,1), (2,-2),(2,-1),(2,0),(2,1),(2,2)]
n = len(cases)                          # 列数（= cases の個数）
fig = plt.figure(figsize=(n*2, 5))     # 全体の figure サイズを設定

for i, (l, m) in enumerate(cases):
    yr = Yr(l, m)                       # 実球面調和関数を計算
    yc = Yc(l, m)                       # 複素球面調和関数を計算

    # 上段: 実形式を描画（色 = 関数値の正負、赤=正・青=負）
    plot_surface(fig.add_subplot(2, n, i+1, projection='3d'),
                 yr, yr, plt.cm.RdBu, f'$Y_{{{l}}}^{{{m}}}$ real')

    # 下段: 複素形式を描画（色 = 位相 arg(Y)、e^{imφ} の回転を可視化）
    plot_surface(fig.add_subplot(2, n, n+i+1, projection='3d'),
                 yc, np.angle(yc), plt.cm.hsv, f'$Y_{{{l}}}^{{{m}}}$ complex')

# 図全体のタイトルを設定
plt.suptitle('Spherical Harmonics $Y_l^m$  (top: real / bottom: complex, color=phase)', fontsize=11)
plt.tight_layout()                      # サブプロット間の余白を自動調整
plt.savefig('sph_harm.png', dpi=120, bbox_inches='tight')  # PNG として保存
plt.show()                              # 画面に表示
