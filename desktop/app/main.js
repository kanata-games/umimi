// ウミミ デスクトップ — main process
const { app, BrowserWindow, screen, Tray, Menu, ipcMain, nativeImage } = require('electron');
const path = require('path');
const fs = require('fs');

const HEIGHTS = { small: 160, medium: 200, large: 260 };
const DEFAULTS = { size: 'medium', eco: true, onTop: true, sound: false, timeMode: 'auto', profileOnTap: true };
let win = null, tray = null, cfg = { ...DEFAULTS };

const cfgPath = () => path.join(app.getPath('userData'), 'settings.json');
function loadCfg() {
  try { cfg = { ...DEFAULTS, ...JSON.parse(fs.readFileSync(cfgPath(), 'utf8')) }; }
  catch (e) { cfg = { ...DEFAULTS }; }
}
function saveCfg() { try { fs.writeFileSync(cfgPath(), JSON.stringify(cfg, null, 2)); } catch (e) {} }

function stripBounds() {
  const wa = screen.getPrimaryDisplay().workArea;          // area above the taskbar
  const h = HEIGHTS[cfg.size] || HEIGHTS.medium;
  return { x: wa.x, y: wa.y + wa.height - h, width: wa.width, height: h };
}

function applyTop() {
  if (!win) return;
  win.setAlwaysOnTop(!!cfg.onTop, 'floating');
}

function sendCfg() { if (win) win.webContents.send('cfg', cfg); }

function createWindow() {
  win = new BrowserWindow({
    ...stripBounds(),
    frame: false,
    transparent: true,
    backgroundColor: '#00000000',
    resizable: false,
    movable: false,
    minimizable: false,
    maximizable: false,
    fullscreenable: false,
    skipTaskbar: true,
    hasShadow: false,
    show: false,
    icon: path.join(__dirname, 'icon.png'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      backgroundThrottling: true,
      spellcheck: false,
    },
  });
  applyTop();
  // clicks pass through to the desktop until the pointer is over the tank or an Umimi
  win.setIgnoreMouseEvents(true, { forward: true });
  win.loadFile(path.join(__dirname, 'index.html'));
  win.webContents.on('did-finish-load', sendCfg);
  win.once('ready-to-show', () => win.showInactive());
  // links (none expected) open outside
  win.webContents.setWindowOpenHandler(() => ({ action: 'deny' }));
  const refit = () => { if (win) win.setBounds(stripBounds()); };
  screen.on('display-metrics-changed', refit);
  screen.on('display-added', refit);
  screen.on('display-removed', refit);
}

function toggleShow() {
  if (!win) return;
  if (win.isVisible()) win.hide(); else { win.showInactive(); applyTop(); }
  buildMenu();
}

function set(patch) {
  Object.assign(cfg, patch);
  saveCfg();
  if ('size' in patch && win) win.setBounds(stripBounds());
  if ('onTop' in patch) applyTop();
  sendCfg();
  buildMenu();
}

function buildMenu() {
  const radio = (label, key, value) => ({ label, type: 'radio', checked: cfg[key] === value, click: () => set({ [key]: value }) });
  let openAtLogin = false;
  try { openAtLogin = app.getLoginItemSettings().openAtLogin; } catch (e) {}
  const menu = Menu.buildFromTemplate([
    { label: win && win.isVisible() ? 'ウミミをかくす' : 'ウミミを出す', click: toggleShow },
    { type: 'separator' },
    { label: '水そうの大きさ', submenu: [radio('小さめ', 'size', 'small'), radio('ふつう', 'size', 'medium'), radio('大きめ', 'size', 'large')] },
    { label: 'うごき', submenu: [radio('省エネ（かるい）', 'eco', true), radio('なめらか（きれい）', 'eco', false)] },
    { label: '時間帯', submenu: [radio('じどう（PCの時計）', 'timeMode', 'auto'), radio('ひる', 'timeMode', 'day'), radio('ゆうがた', 'timeMode', 'dusk'), radio('よる', 'timeMode', 'night')] },
    { label: 'タップでプロフィールを出す', type: 'checkbox', checked: cfg.profileOnTap !== false, click: (i) => set({ profileOnTap: i.checked }) },
    { label: 'おと', type: 'checkbox', checked: !!cfg.sound, click: (i) => set({ sound: i.checked }) },
    { label: 'いつも手前に表示', type: 'checkbox', checked: !!cfg.onTop, click: (i) => set({ onTop: i.checked }) },
    { label: 'パソコン起動時にひらく', type: 'checkbox', checked: openAtLogin, click: (i) => { try { app.setLoginItemSettings({ openAtLogin: i.checked }); } catch (e) {} buildMenu(); } },
    { type: 'separator' },
    { label: 'おわる', click: () => { app.quit(); } },
  ]);
  if (tray) { tray.setContextMenu(menu); tray.setToolTip('ウミミ デスクトップ'); }
}

// only one Umimi tank at a time
if (!app.requestSingleInstanceLock()) {
  app.quit();
} else {
  app.on('second-instance', () => { if (win) { win.showInactive(); applyTop(); buildMenu(); } });
  app.whenReady().then(() => {
    loadCfg();
    createWindow();
    const img = nativeImage.createFromPath(path.join(__dirname, 'tray.png'));
    tray = new Tray(img);
    tray.on('click', toggleShow);
    buildMenu();
  });
  app.on('window-all-closed', () => app.quit());
}

ipcMain.handle('save-photo', async (e, name, dataUrl) => {
  try {
    const dir = path.join(app.getPath('pictures'), 'UmimiDesktop');
    fs.mkdirSync(dir, { recursive: true });
    const safe = String(name).replace(/[^\w.-]/g, '_');
    let file = path.join(dir, safe), i = 1;
    while (fs.existsSync(file)) file = path.join(dir, safe.replace(/\.jpg$/, `-${i++}.jpg`));
    fs.writeFileSync(file, Buffer.from(String(dataUrl).split(',')[1], 'base64'));
    return file;
  } catch (err) { return null; }
});

ipcMain.on('interactive', (e, on) => {
  if (!win) return;
  if (on) win.setIgnoreMouseEvents(false);
  else win.setIgnoreMouseEvents(true, { forward: true });
});
