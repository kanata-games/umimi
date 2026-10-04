// ウミミの箱庭 オフライン用（build_pages.py が作る。直接書きかえない）
const VERSION = '4720a5898e';
const CACHE = 'hakoniwa-' + VERSION;   // 同じサイトの umimi-portal と かぶらない名前
const FONTS = 'hakoniwa-fonts';
const ASSETS = [
  './',
  'index.html',
  'manifest.json',
  'c_adv.png',
  'c_adv2.png',
  'c_animal.png',
  'c_animal2.png',
  'c_dream.png',
  'c_dream2.png',
  'c_fashion.png',
  'c_fashion2.png',
  'c_food.png',
  'c_food2.png',
  'c_princess.png',
  'c_princess2.png',
  'c_relax.png',
  'c_relax2.png',
  'c_season.png',
  'c_season2.png',
  'c_work.png',
  'c_work2.png',
  'f_autumn.png',
  'f_base.png',
  'f_halloween.png',
  'f_pearl.png',
  'icon-180.png',
  'icon-192.png',
  'icon-512.png',
  'roomtex.png',
  'umimi-sprites.png',
  'visitors.png'
];
self.addEventListener('install', e => {
  // 全部そろってから入れかえる（絵と本体の版がずれないように）
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS.map(u => new Request(u, {cache:'reload'})))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  // 消すのは箱庭の古い版だけ（hakoniwa-…、前の名前の umimi-<10けた> / umimi-fonts）。ポータルなど ほかのものには さわらない
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE && k !== FONTS && (k.startsWith('hakoniwa-') || /^umimi-([0-9a-f]{10}x?|fonts)$/.test(k))).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request; if(req.method !== 'GET') return;
  const url = new URL(req.url);
  // 文字のフォント（Google Fonts）：あれば使い、なければ取ってきて とっておく
  if(url.host === 'fonts.googleapis.com' || url.host === 'fonts.gstatic.com'){
    e.respondWith(caches.open(FONTS).then(c => c.match(req).then(hit => hit || fetch(req).then(r => { c.put(req, r.clone()); return r; }).catch(() => hit))));
    return;
  }
  if(url.origin !== location.origin) return;
  // ゲームの本体と絵：とっておいた版を使う（オフラインでも動く）。ページ自体は ? 付きでも同じ版を返す
  const isPage = req.mode === 'navigate';
  e.respondWith(caches.open(CACHE).then(c => c.match(isPage ? 'index.html' : req, {ignoreSearch: isPage}).then(hit => hit || fetch(req).then(r => { if(r.ok && !isPage) c.put(req, r.clone()); return r; }).catch(() => isPage ? c.match('index.html') : Response.error()))));
});
