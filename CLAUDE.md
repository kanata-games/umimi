# ウミミの箱庭

ユーザー（kanata-games）のキャラ「ウミミ」の癒し系箱庭ゲーム。ウミミの生みの親はリリィさん（誕生日 9/29）。

## ファイル
- `index.html` … GitHub Pages で公開している本体（`source/game.html` に head/body とPWA用タグを付けたもの）
- `source/game.html` … 本体の元。claude.ai のアーティファクト（本番・開発版）はこれを公開している
- `umimi-sprites.png` … ウミミ本体の10コマ（245x222 セル、Grokで作った元絵を緑背景抜き・目の位置合わせ済み）
- `costumes.png` … おきがえ46種の1枚シート（座標メタは game.html 内の `COS`）
- `visitors.png` … 訪問者10種×2コマのシート（Grok画像を背景抜き。作り直しは `source/visitors/build_visitors.py`、メタは game.html 内の `VIS_SPR`）。開発版URL末尾に `#visit-crab` などで即呼び出し
- `desktop/` … Windows用デスクトップ版（Electron）の元。`build_desktop.py` で `source/game.html` から画面下の細長い水そう版を生成
- `manifest.json` / `icon-*.png` … ホーム画面に追加用

## 進め方
- 新機能はまず claude.ai の「開発版」アーティファクトで確認 → OKが出たら本番アーティファクトとこのリポジトリに反映
- セーブは localStorage `umimi-hakoniwa-v1`（写真は `umimi-photos-v1`）。更新でデータが消えないよう、項目追加時は古いデータに初期値を補う
- ユーザーのPCは古めなので、デスクトップ版は軽さ優先
- 返答は日本語で
- 公開先：本番 https://claude.ai/artifact/NnwrAc1v6XpEGsrDqoFUuw （友達に共有中）／開発版 https://claude.ai/artifact/LcJJkvKnfMuLo1P3um42CU 。どちらもpngは `files` で同梱、capability `downloads`
- デスクトップ版は小さいセットアップzip（はじめにダブルクリック.bat → _files/setup.ps1 がElectronを取得）で配布
- テスト用：`#birthday` `#mybday` `#ev-<イベント名>` `#visit-<訪問者>`
