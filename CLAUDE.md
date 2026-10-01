# ウミミの箱庭 — 引き継ぎメモ

新しい会話でこのプロジェクトを続けるときは、まずこのファイルを読んでください。

## 概要
- ユーザー：kanata-games（**返答は必ず日本語で**）。Windows。PCは古めなので、軽さを優先する
- ウミミ：ユーザーのキャラ。白い「月のウミウシうさぎ」で、おでこに三日月がある。生みの親は**リリィさん（誕生日 9/29）**
- 遊び方：友達10人くらいとリリィさんが、claude.ai の**本番アーティファクトのリンク**で遊んでいる。GitHub Pages は予備（移行の告知はしない方針）
- 画像（ウミミ・衣装・訪問者）は、ユーザーが Grok で作った緑背景のドット絵を、こちらで背景抜き・位置合わせしている

## ★新しい会話で続けるとき（最初に読む）
- 作業場所：このリポジトリを clone（例 /home/claude/umimi-repo）。本体は `source/game.html`、画像は直下の png
- **本番・開発版のリンクは絶対に変えない**。Artifact を公開するときは必ず `url` に下の既存URLを渡す（url なしで公開すると別リンクが新しくできてしまう）。別の会話から更新する前に、いったん `action: "read"` でその URL を読む
- 公開するとき、画像は `files` に**絶対パス**で全部渡す：`c_animal.png` `c_food.png` `c_season.png` `c_work.png` `c_fashion.png` `c_relax.png` `c_dream.png` `umimi-sprites.png` `visitors.png` `roomtex.png` `f_base.png` `f_pearl.png` `f_autumn.png` `f_halloween.png`。capability は `downloads`（前のバージョンから引き継がれる）
- 開発版は `<title>ウミミの箱庭</title>` を `<title>ウミミの箱庭 開発版</title>` に置き換えたものを公開する
- 確認用：ローカルで `python3 -m http.server` を立て、`<!doctype html><meta charset=utf-8>` を先頭に付けた試験用コピーを Playwright（/opt/pw-browsers）で開く。本体は IIFE なので、試すときは試験用コピーにだけ window.__xxx のフックを足す
- 公開するときは「開発版か本番か」を必ずユーザーに伝える。本番は OK が出てから

## 公開先
| 名前 | URL | 備考 |
|---|---|---|
| 本番 | https://claude.ai/artifact/NnwrAc1v6XpEGsrDqoFUuw | リンクを知っている人は誰でも見られる。友達が遊んでいる |
| 開発版 | https://claude.ai/artifact/LcJJkvKnfMuLo1P3um42CU | 非公開。タイトルは「ウミミの箱庭 開発版」 |
| GitHub Pages | https://kanata-games.github.io/umimi/ | main ブランチの /(root) |

- アーティファクトは `source/game.html`（doctype なしの本体）を公開する。png は `files` で同梱する：おきがえの `c_*.png`（7枚）`umimi-sprites.png` `visitors.png` ほか（絶対パスで指定）。アーティファクトに古い costumes.png が残っているが使っていない
- capability は `downloads`（写真の保存に使う）
- 開発版は、title を `ウミミの箱庭 開発版` に置き換えたものを公開する
- 公開するときは、**開発版か本番か**を必ずユーザーに伝える（本番に出すと思われて止められたことがある）

## 進め方（毎回これ）
1. 開発版で実装し、ユーザーに確認してもらう
2. OK が出たら、本番アーティファクト → このリポジトリ（index.html を作り直す） → デスクトップ版の zip の順に反映する
3. **セーブ互換は絶対に守る**：localStorage `umimi-hakoniwa-v1`（写真は `umimi-photos-v1`、デスクトップ版は `umimi-desktop-v1`）。項目を追加するときは、`defaultState()` と boot 時の補完で古いデータに初期値を入れる。好感度などが消えないようにする
4. ひきつぎコード：`UMIMI1-` + base64(JSON)。PC とスマホの間の移動用

## いまの状態（2026-10-01 時点）
- 開発中（ブランチ dev-closet-tabs）：おきがえシートを分類ごとに分割＋コレクションに分類タブ。開発版に公開済み、本番はまだ
- 本番＝開発版とほぼ同じ。`source/game.html` には、デスクトップ版の「画面一周ダービー」用のコード（`DESK_RING` が true のときだけ動く）が入っているが、ブラウザ版では何もしない。本番アーティファクトと GitHub Pages の index.html はその1つ前（ブラウザ上の動きは同じ）
- デスクトップ版の最新は 0.9.9（画面一周ダービーの試作。ユーザーがPCで試している途中）
- ピッちゃん（ChatGPT）が家具・飾り・衣装の絵を作ってくれる。届いたら背景を抜いてシリーズ別シートに追加する
- 今後の候補：おへやコード（部屋の見せ合い）、デスクトップ版でおけいこ・おへやをウインドウで開く、配信モード

## ファイル
- `index.html` … Pages 用。`source/game.html` の前に head（PWA タグ、manifest、icon）を付け、最後に `</body></html>` を足したもの。今の index.html の先頭14行が head
- `source/game.html` … 本体。1ファイル（HTML と canvas、全体が IIFE）
- `umimi-sprites.png` … ウミミ10コマ（セル 245x222、目の位置合わせ済み）。作り直すときは `source/sprites/build_sprites.py`（元画像は src.png）
- `c_<分類>.png` … おきがえ46枚を分類ごとに分けたシート（animal/food/season/work/fashion/relax/dream、4列、セル 240x208、scale .8）。**使うときだけ読み込む**（`cosImgFor()`、色変えも分類×色ごと）。作り直すときは `source/costumes/build_all.py`（元画像は src/。新しい衣装は SRC と CAT の両方に足す）。出力された costumes.json の中身を、game.html の `const COS = {...}` に貼る（m[k].s が分類、i はシート内の番号）
  - おきがえコレクションの分類タブは `OCATS`。シートのない normal/cape/choco の分類は `OCAT_EXTRA`
  - 目が自動で見つからない衣装は `MANEYE`、大きさの補正は `SCALEFIX`
  - 緑色の衣装は Grok でマゼンタ背景にしてもらう
  - ウミミの色に合わせた色変え：`recolorSheet()`。色を変えない衣装は `COS_KEEP`。チョコとマントはコードで描いている
- `visitors.png` … 訪問者10種×2コマ。作り直すときは `source/visitors/build_visitors.py`。出力された visitors_meta.json を game.html の `const VIS_SPR = {...}` に貼る。絵がまだ読み込まれていないときは、コードで描いた旧訪問者を表示する
- `f_base.png` `f_pearl.png` `f_autumn.png` `f_halloween.png` … 家具・飾りのシリーズ別シート（ピッちゃん=ChatGPT作の絵を背景抜き・色数圧縮）。**使うときだけ読み込む**（`fsheet()`）。作り直しは `source/furniture/build_furniture2.py`（SERIES に「キー:(おへや幅, 水そう幅[, コマ数, 基準])」を足す）→ 出力 furniture_meta.json を game.html の `const FIMG = {m:...}` に貼る（jbox/chandelier は _0 のエイリアスも）
- `roomtex.png` … おへやの壁紙・床の模様タイル4枚（`source/furniture/build_tex.py`）
- デスクトップ版の「画面一周ダービー」：水そうの「ダービー」ボタン → main.js が作業領域いっぱいの透明ウインドウを `index.html#derby` で開く（`DESK_RING`）。予想の画面は真ん中、スタートするとクリックが下のアプリに通る。5匹は画面のいちばん外側を1列で一周（左下がスタート・ゴール、水そうの上も通る）。名前は出さず、賭けた子が金色に光る。閉じると水そうが読み込み直して結果を反映（開いているあいだは水そう側は保存しない `window.__noSave`）。Esc で閉じる
- `desktop/` … Windows デスクトップ版（Electron）。`python3 build_desktop.py` で、game.html から画面の下に出る細長い水そう版の `desktop/app/index.html` を作る（ウミミ・訪問者・おきがえ c_*.png は data URI で埋め込む＝色変えのため。家具 f_*.png と roomtex.png は app に png をコピー。どこから実行してもよい。index.html から作るので、先に index.html を作り直す。置き換える文字列が合わないと assert で止まるので、本体を変えたら置き換え側も直す）
  - 配布は小さい zip：`はじめにダブルクリック.bat` を実行すると `_files/setup.ps1` が Electron v33.2.1 を取ってくる（SHA256 で確認）。更新のときは `_files/app/index.html` を差し替えるだけ。最新は 0.9.9（家具の画像は app フォルダに png として同梱。setup zip は desktop/setup の3ファイル＋ `_files/app` に desktop/app の中身を入れて作る）

## ゲームの中身（game.html の主な定数）
- `OUTFITS` おきがえ49種、`HEADWEAR`、`PERS` 性格、`DECOR` 飾り、`RECOLOR`/`PALS` ウミミの色
- `MILESTONES` 記念日（7, 30, 50, 100, 200, 500, 1000日と毎年）、アルバム、日記
- 写真：`FILTERS`/`FRAMES`/`STAMPS`。撮るときは、写す子・ピント・集合・人数・笑顔を選べる
- `EV` 季節イベント：お月見 9/15–10/10、ハロウィン 10月、クリスマス 12/1–25、正月 1/1–7（おみくじ）、バレンタイン 2/7–14、ひな祭り 2/25–3/3、お花見 3/20–4/15、こどもの日 4/25–5/5、七夕 7/1–7、夏祭り 8月
- 誕生日：リリィさん 9/29 はパーティー。プレイヤー自身の誕生日は `S.myBday {m,d,name}`（名前はそのまま使われる。例：「カナタさん」）
- `VISITORS` 訪問者10種：クラゲ、ヒトデ、タツノオトシゴ、カニ、イルカ、ペンギン、ウミガメ、タコ、フグ、ラッコ。2時間おきに1種ランダムで来て、1時間いる（`VISIT_GAP` と `VISIT_STAY`）。触らなくても時間になったら帰る。初めて会うとおみやげの飾りをくれる。それ以降は1日3回まで、かけらを3こくれる
- ウミミダービー（ヘッダーの「ダービー」）：うちの子最大3＋ゲストで5匹。倍率はレースを裏で500回シミュレーションして決める。ひとりで＝賭け方5種（1着あて／2着まで／1・2着ペア／1→2着／1→2→3着）、みんなで＝最大20人・1着あてのみ・まとめて入力（「カナ 3 50」）。ダービーメダルは人ごと（初期100、10未満で次レースにおこづかい30）、`S.derby.pstats[名前].medals`。こうかんじょ（ロゼット150／ゴールフラッグ250／トロフィー300／ひょうしょうだい450）はプレイヤー1人目のメダルで交換。つきのかけらは1日3回まで。成績は u.wins / u.druns / u.dbest（アルバムに表示）。スマホ（幅700px以下）はダービー画面が全画面。デスクトップ版は高さが足りないのでダービーボタンを隠している
- あそびば（ヘッダー「あそびば」）：ウミミダービー／おけいこ／おへや をまとめたメニュー
- おけいこ：うちの子に芸（ジャンプ・くるくる・おじぎ・ぷかぷか・ぴょんぴょん・ハートぽわぽわ）を1日1回練習。5ポイントで習得し水そうで自分から披露。性格ごとに得意芸。u.tricks / u.learned / u.lessonDay
- おへや：うちの子ごとの部屋（u.room = {wall, floor, items:[{k,x,y,id,on,dx}]}）。家具は FURN、購入済みは S.furn（つきのかけらで1回買えば全員の部屋で使える）。壁紙・床は WALLS / FLOORS（tex は roomtex の番号）。ベッド・椅子・クッションで休む（REST）。写真をアルバムへ
- 水そうの飾り DECOR：img:1 の物は画像。かざるはシリーズタブ（DSERIES：きほん/おみやげ/ダービー/パール/あきまつり/ハロウィン）
- テーブルの上に小物を置ける：テーブル=SURF（shelltable, table）、小物=SMALLS。水そうは o.on=テーブルid, o.dx、おへやは it.on, it.dx
- 動く家具はコマ切り替えだけ（animKey：かぼちゃびっくりばこ）。シャンデリアは静止に変更済み
- テスト用のハッシュ：`#birthday` `#mybday` `#ev-<イベント名>` `#visit-<訪問者>` `#okeiko`（おけいこの1日1回制限を外す）（例 `#visit-crab`）

## Grok 用のプロンプト（新しい素材を頼むとき）
- 衣装：「Pixel art sprite sheet of this exact character (attached Umimi)… Wearing 〔衣装〕. 2 frames side by side, idle, side view facing left… Solid pure green background (#00FF00), no shadows, no effects, no text.」
- 訪問者：同じ形で「a cute sea creature… same pixel style as the reference… Character: 〔生き物〕… 2 frames… facing left… green background」
- 緑色のものはマゼンタ背景（#FF00FF）にしてもらう。サイズや位置はこちらでそろえるので、ばらばらでもよい

## やってはいけないこと
- GitHub は **kanata-games/umimi だけ**触る（meteo-flick、rockside、konkantan は Grok や ChatGPT が使っているので触らない）
- 新しいリポジトリの作成はポリシーで 403 になる。再試行しない
- 本番への公開は、ユーザーの OK が出てから
- コミットの末尾には、指示された Co-Authored-By と Claude-Session の行を付ける
