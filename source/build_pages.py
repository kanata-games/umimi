# GitHub Pages 用の index.html と sw.js（オフライン用）を作る。
#   python3 source/build_pages.py   （どこから実行してもよい）
# index.html = 先頭の head（PWA タグ）＋ source/game.html ＋ サービスワーカーの登録 ＋ </body></html>
# sw.js の VERSION は中身から自動で決まる（ゲームや画像を変えると、自動で新しい版として配られる）
import os, glob, hashlib
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HEAD = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#7f8fe0">
<link rel="manifest" href="manifest.json">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="ウミミ">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}</style>
</head>
<body>
"""
REG = """<div id="a2hs" hidden style="position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));z-index:50;max-width:460px;margin:0 auto;background:rgba(249,249,255,.97);border:1.5px solid #d9dcf5;border-radius:16px;padding:10px 38px 10px 14px;box-shadow:0 6px 20px rgba(80,90,170,.25);font:13.5px/1.6 'Zen Maru Gothic',sans-serif;color:#4a4f7a">
<b style="color:#5b64b8">アプリみたいに あそべます</b><br><span id="a2hsTxt"></span>
<button type="button" id="a2hsX" aria-label="とじる" style="position:absolute;right:8px;top:6px;border:0;background:none;font-size:20px;color:#8a8fb8;cursor:pointer">×</button></div>
<script>
/* ホーム画面に追加の案内（ブラウザで開いているときだけ、1回だけ） */
(function(){
  try{
    var standalone = window.navigator.standalone || (window.matchMedia && matchMedia('(display-mode: standalone)').matches);
    if(standalone || localStorage.getItem('umimi-a2hs-seen')) return;
    var ios = /iPhone|iPad|iPod/.test(navigator.userAgent), android = /Android/.test(navigator.userAgent);
    if(!ios && !android) return;
    document.getElementById('a2hsTxt').textContent = ios
      ? 'Safari の 共有ボタン（□に↑）→「ホーム画面に追加」で、全画面で開けて、電波がなくても あそべます。データも消えにくくなります。'
      : 'ブラウザの メニュー（︙）→「ホーム画面に追加」で、全画面で開けて、電波がなくても あそべます。';
    var box=document.getElementById('a2hs'); setTimeout(function(){ box.hidden=false; }, 2500);
    document.getElementById('a2hsX').onclick=function(){ box.hidden=true; try{ localStorage.setItem('umimi-a2hs-seen','1'); }catch(e){} };
  }catch(e){}
})();
</script>
<script>
/* オフライン用（GitHub Pages のときだけ）。新しい版が入ったら、次にアプリに戻ってきたときに読み込み直す */
(function(){
  if(!('serviceWorker' in navigator) || !(location.protocol==='https:' || location.hostname==='localhost')) return;
  var t0=Date.now(), had=!!navigator.serviceWorker.controller, pending=false;
  var reg=null; navigator.serviceWorker.register('sw.js').then(function(r){ reg=r; r.update().catch(function(){}); }).catch(function(){});
  navigator.serviceWorker.addEventListener('controllerchange', function(){
    if(!had) return;                              /* はじめて入ったときは、もう新しい版を開いているので何もしない */
    if(Date.now()-t0 < 20000) location.reload();  /* 開いたばかりなら すぐ新しい版に */
    else pending=true;                            /* 遊んでいる途中なら、次に戻ってきたときに */
  });
  document.addEventListener('visibilitychange', function(){ if(document.hidden) return; if(pending) location.reload(); else if(reg) reg.update().catch(function(){}); });  /* アプリに戻ってきたら 新しい版がないか見る */
})();
</script>
"""
game = open('source/game.html', encoding='utf-8').read()
html = HEAD + game + REG + "</body></html>\n"
open('index.html','w',encoding='utf-8').write(html)
assets = ['./', 'index.html', 'manifest.json'] + sorted(f for f in glob.glob('*.png'))
h = hashlib.sha1(html.encode())
for f in sorted(glob.glob('*.png')) + ['manifest.json', 'source/sw_template.js']: h.update(open(f,'rb').read())
ver = h.hexdigest()[:10]
sw = open('source/sw_template.js', encoding='utf-8').read().replace('__VERSION__', ver).replace('__ASSETS__', ',\n  '.join("'%s'" % a for a in assets))
open('sw.js','w',encoding='utf-8').write(sw)
print('index.html', len(html), 'bytes / sw.js version', ver, '/', len(assets), 'files')
