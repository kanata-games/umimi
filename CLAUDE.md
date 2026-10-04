# ウミミの箱庭 — 引き継ぎメモ

新しい会話でこのプロジェクトを続けるときは、まずこのファイルを読んでください。

## 概要
- ユーザー：kanata-games（**返答は必ず日本語で**）。Windows。PCは古めなので、軽さを優先する
- ウミミ：ユーザーのキャラ。白い「月のウミウシうさぎ」で、おでこに三日月がある。生みの親は**リリィさん（誕生日 9/29）**
- 遊び方：友達10人くらいとリリィさんが、claude.ai の**本番アーティファクトのリンク**で遊んでいた。2026-10-04 から、オフラインで遊べてデータも消えにくい **GitHub Pages のホーム画面版**への移行を、ユーザーが友達に呼びかけている（claude.ai 版も残して更新は続ける）
- 画像（ウミミ・衣装・訪問者）は、ユーザーが Grok で作った緑背景のドット絵を、こちらで背景抜き・位置合わせしている

## ★新しい会話で続けるとき（最初に読む）
- 作業場所：このリポジトリを clone（例 /home/claude/umimi-repo）。本体は `source/game.html`、画像は直下の png
- **本番・開発版のリンクは絶対に変えない**。Artifact を公開するときは必ず `url` に下の既存URLを渡す（url なしで公開すると別リンクが新しくできてしまう）。別の会話から更新する前に、いったん `action: "read"` でその URL を読む
- 公開するとき、画像は `files` に**絶対パス**で全部渡す：`c_animal.png` `c_food.png` `c_season.png` `c_work.png` `c_fashion.png` `c_relax.png` `c_dream.png` `c_adv.png` `c_princess.png`、2コマ目の `c_<分類>2.png`（9枚）、`umimi-sprites.png` `visitors.png` `roomtex.png` `f_base.png` `f_pearl.png` `f_autumn.png` `f_halloween.png`。capability は `downloads`（前のバージョンから引き継がれる）
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
2. OK が出たら、本番アーティファクト → このリポジトリ（`python3 source/build_pages.py` で index.html と sw.js を作り直して main に push ＝ Pages のホーム画面版も更新） → デスクトップ版の zip の順に反映する
3. **セーブ互換は絶対に守る**：localStorage `umimi-hakoniwa-v1`（写真は `umimi-photos-v1`、デスクトップ版は `umimi-desktop-v1`）。項目を追加するときは、`defaultState()` と boot 時の補完で古いデータに初期値を入れる。好感度などが消えないようにする
4. ひきつぎコード：`UMIMI2-`（圧縮）か `UMIMI1-` + base64(JSON)。PC とスマホの間の移動用。写真は入らない

## いまの状態（2026-10-04 時点）
- 本番＝開発版＝GitHub Pages＝`source/game.html`（バックアップ・みじかいコード・ホーム画面版・ながめモードまで反映済み）。`DESK_RING` のコードはブラウザ版では何もしない
- デスクトップ版の最新は 0.15.0（ながめモードのボタンは無し。バックアップ・みじかいコード・2コマ目のキラキラ・おきがえ123種・BGM・おきがえ分類タブ入り。画面一周ダービーもそのまま。画面一周の窓ではBGMは鳴らさない）。デスクトップの画面は `desktop/desktop_head.html` が別にあるので、本体に要素を足したらこちらにも足す（足りないと getElementById が null で止まる）
- おきがえを増やすとき：1枚のシートは50種くらいまでを目安に。超えそうなら分類を分ける（例：きせつ → はるなつ／あきふゆ）。シートの中身は `CAT`（build_all.py）、タブは `OCATS`（game.html）
- ピッちゃん（ChatGPT）が家具・飾り・衣装の絵を作ってくれる。届いたら背景を抜いてシリーズ別シートに追加する
- じどうバックアップ（`umimi-hakoniwa-v1-bk`、3世代・8時間に1回まで・セーブが読めないと自動で戻す、壊れたセーブは `-broken` にとっておく）、ファイルに保存/読み込み（txt。中身はふつうのコード）、1週間ファイル保存していないと3日に1回声かけ（S.lastExport / S.bkNagAt）。ひきつぎコードは `UMIMI2-`（deflate-raw 圧縮＋base64、約1/8〜1/11）と `UMIMI1-`（ふつう）を選べ、読み込みはどちらも自動判別
- ながめモード（ヘッダー「ながめる」）：body.nagame で水そうだけを全画面、右上「もどる」は3秒で消えタップで出る、Esc でも戻る。Wake Lock で画面が消えない、お知らせは出さない、PCはカーソルが隠れる。左上に時計（タップでうすく、localStorage `umimi-nagclock`）。デスクトップ版には付けていない（要素が無いので if で守っている）
- 今後の候補（ながめモード）：おやすみタイマー（BGMをゆっくり消す）、ゆっくりカメラ
- 今後の候補：毎日のお題（おしゃれコンテスト）、ウミミどうしの暮らし、クリスマスの素材を11月中に頼む、おへやコード（部屋の見せ合い）、デスクトップ版でおけいこ・おへやをウインドウで開く、配信モード

## ファイル
- `index.html` と `sw.js` … Pages 用（ホーム画面版）。**`python3 source/build_pages.py` で作る**（手で組み立てない）。head（PWA タグ）＋ game.html ＋「ホーム画面に追加」の案内（スマホのブラウザで1回だけ）＋ サービスワーカーの登録。sw.js は `source/sw_template.js` から作られ、VERSION は中身のハッシュで自動（ゲームや画像を変えると自動で新しい版が配られる）。全部の png を最初にまとめて保存するので、電波がなくても遊べる。新しい版は「開いて20秒以内なら すぐ読み込み直し／遊んでいる途中なら 次にアプリに戻ったとき」に切り替わる。png を足したら build_pages.py が自動で拾う
  - 更新のたびに全部（今は約4MB）を取り直す方式。差分アップデート（変わったファイルだけ）は、ユーザーと相談のうえ保留中。画像が20MBを超えるか、通信量の声が出たら切り替えを考える
  - **umimi-portal と同じサイト（kanata-games.github.io）**なので、ブラウザで開くと localStorage とオフライン用キャッシュの置き場所を共有する。ポータル側は `umimi-hakoniwa-*` のキーと `hakoniwa-*` のキャッシュ名を使わないこと。箱庭の sw.js は `hakoniwa-<版>` と `hakoniwa-fonts` を使い、掃除するのは自分の古い版（と前の名前の `umimi-<10桁>` / `umimi-fonts`）だけ。iPhone のホーム画面版どうしは置き場所が別なので、連動はコードやファイルで
  - ホーム画面版のデータは Safari 本体と別で、7日ルールで消されない。ただしアイコン削除・容量不足・機種変更では消えるので、ファイル保存のバックアップとセット
- `source/game.html` … 本体。1ファイル（HTML と canvas、全体が IIFE）
- `umimi-sprites.png` … ウミミ10コマ（セル 245x222、目の位置合わせ済み）。作り直すときは `source/sprites/build_sprites.py`（元画像は src.png）
- `c_<分類>.png` … おきがえ120枚を分類ごとに分けたシート（animal/food/season/work/fashion/relax/dream/adv=ぼうけん/princess=おひめさま、4列、セル 240x208、scale .8）。**使うときだけ読み込む**（`cosImgFor()`、色変えも分類×色ごと）。作り直すときは `source/costumes/build_all.py`（元画像は src/。新しい衣装は SRC と CAT の両方に足す）。出力された costumes.json の中身を、game.html の `const COS = {...}` に貼る（m[k].s が分類、i はシート内の番号）
  - おきがえコレクションの分類タブは `OCATS`。シートのない normal/cape/choco の分類は `OCAT_EXTRA`
  - 目が自動で見つからない衣装は `MANEYE`、大きさの補正は `SCALEFIX`
  - 緑色の衣装は Grok でマゼンタ背景にしてもらう
  - 2026-10 にピッちゃん（ChatGPT）から74種。1枚に「4種×2コマ」（2行×4列）で届く。切り出して src/<キー>.png にし、目の座標は MANEYE に入れた（`NEWSET` は体だけ残してとなりのコマの切れはしを消す）。顔がかくれている衣装は `NOEYE`（体の幅で大きさを合わせ、ゲームでは meta の ne:1 でまばたきを描かない）
  - 衣装が青・紫だと色変えで染まるので、そういう衣装は `COS_KEEP` に入れる（耳の色も変わらなくなる）
  - 2コマ目（キラキラ・エフェクト）は `c_<分類>2.png`（同じ並び。meta の f2:1 がある子だけ）。build_all.py が体の下6割どうしを重ねて1コマ目の位置に合わせる。ゲームでは、うれしい・光る・芸のときと、水そうで10秒に1回くらい2コマ目になる（コレクションの絵は1コマ目のまま）。2コマ目で触角（耳）が折れる衣装は `NOF2` に入れて使わない（ユーザーの希望）。新しく頼むときは「2コマ目は耳を動かさず、エフェクトだけ足して」と伝える
  - うさぎのきぐるみは10コマ分（ふつうのウミミと同じ並び）が届いているので、将来アニメに使える
  - ウミミの色に合わせた色変え：`recolorSheet()`。色を変えない衣装は `COS_KEEP`。チョコとマントはコードで描いている
- `visitors.png` … 訪問者10種×2コマ。作り直すときは `source/visitors/build_visitors.py`。出力された visitors_meta.json を game.html の `const VIS_SPR = {...}` に貼る。絵がまだ読み込まれていないときは、コードで描いた旧訪問者を表示する
- `f_base.png` `f_pearl.png` `f_autumn.png` `f_halloween.png` … 家具・飾りのシリーズ別シート（ピッちゃん=ChatGPT作の絵を背景抜き・色数圧縮）。**使うときだけ読み込む**（`fsheet()`）。作り直しは `source/furniture/build_furniture2.py`（SERIES に「キー:(おへや幅, 水そう幅[, コマ数, 基準])」を足す）→ 出力 furniture_meta.json を game.html の `const FIMG = {m:...}` に貼る（jbox/chandelier は _0 のエイリアスも）
- `roomtex.png` … おへやの壁紙・床の模様タイル4枚（`source/furniture/build_tex.py`）
- デスクトップ版の「画面一周ダービー」：水そうの「ダービー」ボタン → main.js が作業領域いっぱいの透明ウインドウを `index.html#derby` で開く（`DESK_RING`）。予想の画面は真ん中、スタートするとクリックが下のアプリに通る。5匹は画面のいちばん外側を1列で一周（左下がスタート・ゴール、水そうの上も通る）。名前は出さず、賭けた子が金色に光る。閉じると水そうが読み込み直して結果を反映（開いているあいだは水そう側は保存しない `window.__noSave`）。Esc で閉じる
- `desktop/` … Windows デスクトップ版（Electron）。`python3 build_desktop.py` で、game.html から画面の下に出る細長い水そう版の `desktop/app/index.html` を作る（ウミミ・訪問者・おきがえ c_*.png は data URI で埋め込む＝色変えのため。家具 f_*.png と roomtex.png は app に png をコピー。どこから実行してもよい。index.html から作るので、先に index.html を作り直す。置き換える文字列が合わないと assert で止まるので、本体を変えたら置き換え側も直す）
  - zip は **Python の zipfile で作る**（Linux の zip コマンドだと日本語のファイル名に UTF-8 の印が付かず、Windows で解凍すると文字化けする）
  - 配布は小さい zip（最新 0.15.0）：`はじめにダブルクリック.bat` を実行すると `_files/setup.ps1` が Electron v33.2.1 を取ってくる（SHA256 で確認）。更新のときは `_files/app/index.html` を差し替えるだけ。（家具の画像は app フォルダに png として同梱。setup zip は desktop/setup の3ファイル＋ `_files/app` に desktop/app の中身を入れて作る）

## エリア（2026-10-05 開発版で追加。本番はまだ）
- 方針：A＝いつもの海（いままでの水そう、そのまま）／B＝サンゴの森（素材・クラフト・畑の場所）／C＝イベント・特別な景観（いまは「？？？」でロック）
- 水そうの左上のタブで切り替え（パネルを開いているあいだは隠れる）（`buildAreaTabs()`。`nav.tools` が無いデスクトップ版では作らない＝`areaUI()`）。B のときは body.areaB でツールを隠し、トレイは `renderTrayB()`（おでかけする子をえらぶ）
- B は同じキャンバスに `drawAreaB()` で描く。A の `update()` は B を見ているあいだも動き続ける（A の暮らしはそのまま）
- おでかけ：えらんだ子（最大 `B_MAX`=3）の**コピー**が B を歩く（A にもいる）。`S.areaB = {members:[id], visited}`、いま見ているエリアは `S.area`（'a'|'b'）。コピーは `bCopies`（保存しない）、パーティクルは `pB`
- B の作業台（`B_BENCH`）・貝殻窯（`B_KILN`）・看板はまだ飾り（タップで「もうすぐ」）。砂の上の貝・海ガラス・流木は見た目だけ（次に素材として拾えるようにする予定）
- 次の予定：②素材が手に入る（流れ着く・おでかけの子が拾う）→ ③作業台でクラフト（2〜3素材で家具1つ）→ ④作った家具を置く → ⑤畑 → ⑥C エリア

## ゲームの中身（game.html の主な定数）
- `OUTFITS` おきがえ123種、`HEADWEAR`、`PERS` 性格、`DECOR` 飾り、`RECOLOR`/`PALS` ウミミの色
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
- BGM（`const BGM`）：音のファイルは使わず Web Audio でその場で鳴らす（数KB）。曲は `SONGS`：base（水そうのオルゴール。ひる72/ゆうがた64/よる56 BPM）、derby（待ち時間。オーケストラ風）、derbyRace（レース中）、room（木琴）、lesson（ピチカート）、halloween、tsukimi、xmas、wa（正月・ひなまつり・お花見・こどもの日）、natsu（七夕・夏祭り）。バレンタインは base。10月はじめのハロウィン＋お月見は、夜だけ tsukimi
  - 1曲＝8小節×8分音符8つ。`ch`=小節ごとの[ベース, 和音の音…]（MIDI番号）、`mel`=小節ごとの[8分の位置, 音, (長さ8分)]、`acc()`=伴奏とリズム。楽器は `INST`（box/mari/pluck/bell/sub/koto/str/brass/spic）と `ORC`・`PERC`
  - 場面は `scene()` で決まり、変わると0.5秒でフェードして次の曲へ。曲ごとの音量は `gain`。ダービーのゴールで `BGM.fanfare(当たり)`（別の出口 fxIn で鳴らすので切り替えで消えない）
  - おとボタンは OFF → ON ♪（BGMあり）→ ON（こうかおんだけ）→ OFF。`S.bgm`（古いセーブは true 扱い）
  - 新しい曲の音量は、Playwright で `--autoplay-policy=no-user-gesture-required` にして MediaRecorder で録音し、ffmpeg の volumedetect で平均 -31〜-35dB にそろえた
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
