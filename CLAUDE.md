# ウミミの箱庭

ユーザー（kanata-games）のキャラ「ウミミ」の癒し系箱庭ゲーム。ウミミの生みの親はリリィさん（誕生日 9/29）。

## ファイル
- `index.html` … GitHub Pages で公開している本体（`source/game.html` に head/body とPWA用タグを付けたもの）
- `source/game.html` … 本体の元。claude.ai のアーティファクト（本番・開発版）はこれを公開している
- `umimi-sprites.png` … ウミミ本体の10コマ（245x222 セル、Grokで作った元絵を緑背景抜き・目の位置合わせ済み）
- `costumes.png` … おきがえ46種の1枚シート（座標メタは game.html 内の `COS`）
- `desktop/` … Windows用デスクトップ版（Electron）の元。`build_desktop.py` で `source/game.html` から画面下の細長い水そう版を生成
- `manifest.json` / `icon-*.png` … ホーム画面に追加用

## 進め方
- 新機能はまず claude.ai の「開発版」アーティファクトで確認 → OKが出たら本番アーティファクトとこのリポジトリに反映
- セーブは localStorage `umimi-hakoniwa-v1`（写真は `umimi-photos-v1`）。更新でデータが消えないよう、項目追加時は古いデータに初期値を補う
- ユーザーのPCは古めなので、デスクトップ版は軽さ優先
- 返答は日本語で
