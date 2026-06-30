# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

単一ファイル (`index.html`) で完結する、水素原子の球面調和関数 Y_l^m のインタラクティブ3D可視化ツール。外部ライブラリへの依存は一切なく、ブラウザで直接開くだけで動作する。

- **公開URL**: https://sayuri-miyake.github.io/hydrogen-e-orbit/
- **リポジトリ**: https://github.com/Sayuri-Miyake/hydrogen-e-orbit

## ファイル構成

```
index.html        — Webアプリ全体（CSS・HTML・JavaScript をすべて内包）
plot_sph_harm.py  — 球面調和関数の3Dプロット（Python / matplotlib）
sph_harm.png      — plot_sph_harm.py の出力画像
.gitignore        — macOS の .DS_Store を除外
```

### plot_sph_harm.py の実行

```bash
pip3 install matplotlib scipy  # 初回のみ
python3 plot_sph_harm.py       # sph_harm.png を生成して画面表示
```

- 上段: 実球面調和関数（色 = 正負の符号、赤=正・青=負）
- 下段: 複素球面調和関数（色 = 位相 arg(Y)、HSVカラーマップ）
- `scipy.special.sph_harm` を使用。引数順は `sph_harm(m, l, φ, θ)`（index.html 内の独自実装とは別物）。

## コードの構成（index.html 内部）

`index.html` は以下の6ブロックで構成されている。

| ブロック | 内容 |
|---|---|
| `<style>` | レイアウト・ボタン・数式ボックスのCSS。CSSカスタムプロパティ（`--bg`, `--accent` 等）でカラーパレットを管理。 |
| `<body>` HTML | 左サイドパネル `#panel`（コントロール）＋ 右 `#canvas-area`（Canvas + 情報バー）の2カラム構成。 |
| 【1】State `S` | UI状態と回転角をまとめたオブジェクト。すべての処理がこれを参照する。 |
| 【2】数学関数 | `fact` / `Plm` / `N` / `Yc` / `Yr` — 球面調和関数の計算。コンドン-ショートレー位相規則を採用。 |
| 【3】3Dレンダラー | Canvas 2D API によるメッシュ生成・透視投影・ペインターズアルゴリズム描画。メッシュは `MC` オブジェクトにキャッシュ。 |
| 【4】数式DB | `FTEXT`（解析式）/ `REL`（Lz 固有値の説明）/ `ONAMES`（軌道名）の参照テーブル。 |
| 【5】UI制御 | ボタンのイベントリスナー・数式ボックス・凡例の更新関数。 |
| 【6】初期化 | ページ読み込み時の初期状態設定と描画ループ開始。 |

## 座標系の規約

- 画面 x = 物理 x = r·sinθ·cosφ
- 画面 y = 物理 z = r·cosθ （**量子化軸が画面上方向**）
- 画面奥行き = 物理 y = r·sinθ·sinφ

座標軸の色: x=赤, z=緑（量子化軸）, y=青。

## 球面調和関数の実装規約

- 連関ルジャンドル多項式 `Plm(l,m,x)` はコンドン-ショートレー位相を含む（m > 0 のとき (−1)^m 倍）。
- 複素形式 `Yc` は `[re, im]` の配列を返す。
- 実形式 `Yr` は m > 0 で cos(mφ)、m < 0 で sin(|m|φ) の組み合わせを返す。
- `getMesh` のキャッシュキーは `"l,m,real,sq"` の文字列。表示量 `sq` を変更した際はキャッシュを全クリアする。

## 変更時の注意点

- **数式DBの追加・修正** (`FTEXT`/`REL`/`ONAMES`): l=4 以上を追加する場合は3つすべてのテーブルを更新する。
- **レンダラーの変更**: `getMesh` のキャッシュ (`MC`) を適切にクリアしないと古いメッシュが残る。
- **座標系の変更**: `getMesh` 内の頂点計算と `drawAxes` のラベルを同時に変更する必要がある。
- **デプロイ**: `git push` するだけで GitHub Pages が自動更新される（ビルド不要）。
