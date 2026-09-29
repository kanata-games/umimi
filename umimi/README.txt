ウミミの箱庭 — GitHub Pages 用のファイル一式

■ 中身
index.html        … ゲーム本体
umimi-sprites.png … ウミミの絵
costumes.png      … おきがえの絵
manifest.json / icon-*.png … スマホの「ホーム画面に追加」用
.nojekyll         … GitHub Pages 用（消さないでください）

■ 置き方（はじめて）
1. GitHub で新しいリポジトリを作る（例：umimi）。Public にする
2. 「Add file」→「Upload files」で、このフォルダの中身を全部アップロード
   （.nojekyll が見えないときは、なくても動きます）
3. Settings → Pages → Branch を「main」「/(root)」にして Save
4. 数分後に https://（ユーザー名）.github.io/umimi/ で遊べます

■ 更新するとき
新しい index.html などを同じ名前でアップロードし直すだけです。
セーブデータは消えません。

■ いまのリンクから引っ越すとき
・セーブ：いまのリンクの「ひきつぎ」でコードを書き出し、新しいリンクの「ひきつぎ」で読み込む
・写真：コードには入らないので、残したい写真は先に「端末に保存」しておく
