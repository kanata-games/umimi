import re, base64, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # どこから実行してもリポジトリ直下で動く
src = open('index.html').read()
script = src[src.index('<script>')+8 : src.index('</script>')]
s = script
def R(a,b,cnt=1):
    global s
    assert s.count(a)==cnt, (s.count(a), a[:100])
    s = s.replace(a,b)

# ---- world width becomes variable ----
R("const W = 1000;", "let W = 1000, tankTop = 60;\nlet SET = {size:'medium', eco:true, onTop:true, sound:false, timeMode:'auto'};")
# x ranges
for a,b in [("clamp(u.x,50,950)","clamp(u.x,50,W-50)"),
            ("clamp(u.x+rand(-320,320),60,940)","clamp(u.x+rand(-320,320),60,W-60)"),
            ("*rand(90,170),60,940)","*rand(90,170),60,W-60)"),
            ("clamp(u.x+rand(-360,360),60,940)","clamp(u.x+rand(-360,360),60,W-60)"),
            ("clamp(f.x+side*off,50,950)","clamp(f.x+side*off,50,W-50)"),
            ("clamp(u.x+rand(-380,380),60,940)","clamp(u.x+rand(-380,380),60,W-60)"),
            ("clamp(L.x - L.dir*85*scaleD(L.d),50,950)","clamp(L.x - L.dir*85*scaleD(L.d),50,W-50)"),
            ("clamp(u.x-u.dir*70*scaleD(u.d),40,960)","clamp(u.x-u.dir*70*scaleD(u.d),40,W-40)"),
            ("x:rand(80,920),d:rand(.05,.95),pop:1","x:rand(80,W-80),d:rand(.05,.95),pop:1"),
            ("(L.x<500?1:-1)*rand(250,400),60,940)","(L.x<W/2?1:-1)*rand(250,400),60,W-60)"),
            ("x:rand(20,980),y:floorY(rand(0,1))","x:rand(20,W-20),y:floorY(rand(0,1))"),
            ("star={x:rand(60,520),y:rand(26,80)","star={x:rand(60,W*.5),y:tankTop+rand(8,30)"),
            ("bigB={x:rand(120,880),y:floorTop+rand(30,90)","bigB={x:rand(120,W-120),y:floorTop+rand(10,50)"),
            ("rand(110,170)):0, tx:rand(260,740)","rand(30,55)):0, tx:rand(W*.26,W*.74)"),
            ("v.tx=clamp(v.x+rand(-120,120),120,880)","v.tx=clamp(v.x+rand(-120,120),120,W-120)"),
            ("cake = {x:500, d:.3,","cake = {x:W/2, d:.3,"),
            ("return {x:rand(40,960),","return {x:rand(40,W-40),"),
            ("confetti(500,H*.35,70,340)","confetti(W/2,H*.4,70,340)"),
            ("confetti(500,H*.3,90,380)","confetti(W/2,H*.4,90,380)"),
            ("confetti(rand(200,400),H*.3,60,300)","confetti(rand(W*.2,W*.4),H*.4,60,300)"),
            ("confetti(rand(600,800),H*.3,60,300)","confetti(rand(W*.6,W*.8),H*.4,60,300)"),
            ("u.x=clamp(p.x,40,960);","u.x=clamp(p.x,40,W-40);"),
            ("const px=clamp(p.x,20,980);","const px=clamp(p.x,20,W-20);"),
            ("u.tx=clamp(p.x+rand(-70,70),60,940)","u.tx=clamp(p.x+rand(-70,70),60,W-60)"),
            ("x:clamp(p.x,30,970), y:","x:clamp(p.x,30,W-30), y:"),
            ("x:clamp(p.x,20,980), d};","x:clamp(p.x,20,W-20), d};"),
            ("x:rand(150,850), d, aff:0","x:rand(150,W-150), d, aff:0"),
           ]:
    R(a,b)
# swimming height limited to the tank
R("u.swimH=rand(60,Math.max(90,(floorY(u.d)-60)*.55));","u.swimH=rand(20,Math.max(26,floorY(u.d)-tankTop-95*scaleD(u.d)));")
# vertical: bubbles pop at surface, big bubble surface, weather spawn
R("if(p.y<20) p.life=0;","if(p.y<tankTop+6) p.life=0;")
R("if(bigB.y<30){","if(bigB.y<tankTop+14){")
R("addP({type:'snow',x:rand(0,W),y:-5,","addP({type:'snow',x:rand(0,W),y:tankTop+2,")
R("addP({type:'spark',x:rand(0,W),y:-5,","addP({type:'spark',x:rand(0,W),y:tankTop+2,")
R("if(Math.random()<dt*6) addP({type:'conf',","if(Math.random()<dt*6*W/1000) addP({type:'conf',")
# ---- resize for a strip ----
R("""function resize(){
  const r = stage.getBoundingClientRect();
  dpr = Math.min(2, window.devicePixelRatio || 1);
  cv.width = Math.max(1, Math.round(r.width * dpr)); cv.height = Math.max(1, Math.round(r.height * dpr));
  k = r.width / W; H = r.height / k;
  SIZE = H > W * 0.9 ? 1.4 : (H > W * 0.7 ? 1.15 : 1);
  floorTop = H * (H > W ? 0.58 : 0.54); floorBot = H - 16;
  buildScenery();
}""","""function resize(){
  const r = stage.getBoundingClientRect();
  dpr = SET.eco ? 1 : Math.min(2, window.devicePixelRatio || 1);
  cv.width = Math.max(1, Math.round(r.width * dpr)); cv.height = Math.max(1, Math.round(r.height * dpr));
  H = 300; k = r.height / H; W = Math.max(600, r.width / k);
  SIZE = 1; tankTop = 58; floorTop = 150; floorBot = H - 8;
  buildScenery();
  if(S){ S.umimi.forEach(u=>{ u.x=clamp(u.x,50,W-50); }); S.decor.forEach(o=>{ o.x=clamp(o.x,20,W-20); }); S.ground.forEach(g=>{ g.x=clamp(g.x,40,W-40); }); if(cake) cake.x=W/2; }
}""")
R("kelp = [{x:24,h:floorTop*0.9,ph:0},{x:62,h:floorTop*0.62,ph:1.4},{x:972,h:floorTop*0.8,ph:2.2}];",
  "const kh=floorTop-tankTop; kelp = [{x:24,h:kh*0.9,ph:0},{x:62,h:kh*0.62,ph:1.4},{x:W-28,h:kh*0.8,ph:2.2}];")
R("for(let i=0;i<13;i++) farShapes.push(","for(let i=0;i<Math.round(13*W/1000);i++) farShapes.push(")
R("for(let i=0;i<170;i++) sandDots.push(","for(let i=0;i<Math.round(170*W/1000);i++) sandDots.push(")
R("sandDots = []; for","sandDots = []; for")
# ---- background: transparent above a tank ----
R("""  let g = c.createLinearGradient(0,0,0,floorTop+40); g.addColorStop(0,p.wt); g.addColorStop(1,p.wb);
  c.fillStyle = g; c.fillRect(0,0,W,H);
  const moonX = W*0.8, moonY = 56;""","""  c.clearRect(0,0,W,H);
  c.save();
  c.beginPath(); c.moveTo(0,H); for(let x=0;x<=W;x+=20) c.lineTo(x, tankTop+Math.sin(x*.02+T*1.2)*3+Math.sin(x*.047-T)*2); c.lineTo(W,H); c.closePath(); c.clip();
  let g = c.createLinearGradient(0,tankTop,0,floorTop+40); g.addColorStop(0,p.wt); g.addColorStop(1,p.wb);
  c.fillStyle = g; c.fillRect(0,0,W,H);
  const moonX = W*0.86, moonY = tankTop+26;""")
R("const gr = c.createLinearGradient(0,0,0,floorTop+60);","const gr = c.createLinearGradient(0,tankTop,0,floorTop+60);")
R("c.moveTo(x0-18,0); c.lineTo(x0+26,0);","c.moveTo(x0-18,tankTop); c.lineTo(x0+26,tankTop);")
R("for(let i=0;i<6;i++){\n    const day = p.ray","for(let i=0;i<Math.round(6*W/1000);i++){\n    const day = p.ray")
R("g = c.createLinearGradient(0,0,0,46);","g = c.createLinearGradient(0,tankTop,0,tankTop+30);")
R("c.fillStyle = g; c.fillRect(0,0,W,46);","c.fillStyle = g; c.fillRect(0,tankTop-6,W,36);")
R("for(let x=0;x<=W;x+=20) c.lineTo(x, 16+Math.sin(x*.02+T*1.2)*3+Math.sin(x*.047-T)*2); c.stroke();","for(let x=0;x<=W;x+=20) c.lineTo(x, tankTop+Math.sin(x*.02+T*1.2)*3+Math.sin(x*.047-T)*2); c.stroke();")
# close clip at end of drawBackground: after sand dots
R("""  sandDots.forEach(d => { c.fillStyle = d.l ? 'rgba(255,255,255,.55)' : 'rgba(140,130,200,.16)'; c.beginPath(); c.ellipse(d.x, floorTop+16+d.f*(H-floorTop-16), d.r*1.6, d.r*.8, 0, 0, TAU); c.fill(); });
}""","""  sandDots.forEach(d => { c.fillStyle = d.l ? 'rgba(255,255,255,.55)' : 'rgba(140,130,200,.16)'; c.beginPath(); c.ellipse(d.x, floorTop+16+d.f*(H-floorTop-16), d.r*1.6, d.r*.8, 0, 0, TAU); c.fill(); });
  c.restore();
  c.strokeStyle = 'rgba(255,255,255,.85)'; c.lineWidth = 2; c.beginPath();
  for(let x=0;x<=W;x+=20) c.lineTo(x, tankTop+Math.sin(x*.02+T*1.2)*3+Math.sin(x*.047-T)*2); c.stroke();
}""")
R("`rgba(16,18,54,${veil})`; c.fillRect(0,0,W,H); }","`rgba(16,18,54,${veil})`; c.fillRect(0,tankTop,W,H-tankTop); }")
R("const x=pl.x, y=30+pl.y*(H-60);","const x=pl.x, y=tankTop+10+pl.y*(H-tankTop-20);")
R("if(!plankton.length) for(let i=0;i<46;i++)","if(!plankton.length) for(let i=0;i<Math.round(46*W/1000);i++)")
# bunting compact
R("const n = BUNT.length, x0 = W*.08, x1 = W*.92, sag = 34, yTop = 34;","const n = BUNT.length, span = Math.min(W*.8, 760), x0 = W/2-span/2, x1 = W/2+span/2, sag = 14, yTop = 6;")
R("const ty = yTop + sag + fw*1.15 + 34*SIZE;","const ty = tankTop + 30;")
R("c.font=`600 ${Math.round(30*SIZE)}px","c.font=`600 ${Math.round(22*SIZE)}px")
# balloons count relative to width
R("if(!balloons.length) for(let i=0;i<7;i++)","if(!balloons.length) for(let i=0;i<Math.min(14,Math.round(6*W/1000));i++)")
R("r:rand(22,30)*SIZE,","r:rand(16,22)*SIZE,")
# tray: no hints in desktop
import re as _re
m=_re.search(r"  if\(mode==='pet'\)\{ tr\.innerHTML = .*?\n  if\(mode==='food'\)\{ tr\.innerHTML = [^\n]*\n", s, _re.S)
assert m
s = s[:m.start()] + "  if(mode==='pet' || mode==='food') return;\n" + s[m.end():]
# storage key
s = s.replace("'umimi-hakoniwa-v1'","'umimi-desktop-v1'")
# default state positions relative to width
R("""    umimi:[{id:1,name:'ウミミ',color:'lavender',x:380,d:0.6,aff:0},{id:2,name:'ミナモ',color:'sky',x:650,d:0.32,aff:0}],
    decor:[{id:1,type:'grass',x:110,d:0.12},{id:2,type:'coral',x:880,d:0.06},{id:3,type:'grass',x:940,d:0.5},
           {id:4,type:'shell',x:250,d:0.88},{id:5,type:'pebble',x:720,d:0.8},{id:6,type:'lamp',x:520,d:0.04}],
    ground:[{x:180,d:0.55}],""","""    umimi:[{id:1,name:'ウミミ',color:'lavender',x:W*.4,d:0.6,aff:0},{id:2,name:'ミナモ',color:'sky',x:W*.6,d:0.32,aff:0}],
    decor:[{id:1,type:'grass',x:W*.05,d:0.12},{id:2,type:'coral',x:W*.9,d:0.06},{id:3,type:'grass',x:W*.94,d:0.5},
           {id:4,type:'shell',x:W*.25,d:0.88},{id:5,type:'pebble',x:W*.72,d:0.8},{id:6,type:'lamp',x:W*.52,d:0.04}],
    ground:[{x:W*.18,d:0.55}],""")
# frame rate cap + pause when hidden
R("function frame(now){ const dt=Math.min(.05,(now-last)/1000); last=now; T+=dt; update(dt); draw(); if(derby) updateDerby(dt); updateLesson(dt); updateRoom(dt); requestAnimationFrame(frame); }",
  """function frame(now){ requestAnimationFrame(frame);
  const minGap = SET.eco ? 1000/24 : 1000/60; if(now-last < minGap-2) return;
  const dt=Math.min(.08,(now-last)/1000); last=now; if(document.hidden) return; T+=dt; if(DESK_RING){ if(derby) updateDerby(dt); return; } update(dt); draw(); if(derby) updateDerby(dt); updateLesson(dt); updateRoom(dt); }""")
# boot: resize before state, desktop hooks
R("""  S = Object.assign(defaultState(), saved || {});""","""  resize();
  S = Object.assign(defaultState(), saved || {});""")
R("""  if(!S.welcomed && !isBirthday()){ S.welcomed=true; setTimeout(()=>toast(night>.5 ? 'ようこそ。夜なので、みんな少しねむそう' : 'ようこそ、ウミミの箱庭へ。タップでなでてあげてね'),600); }""",
  """  if(!S.welcomed && !isBirthday()){ S.welcomed=true; setTimeout(()=>toast('ウミミが デスクトップに やってきたよ。右下のメニューで あそべるよ'),600); }""")
R("""  new ResizeObserver(resize).observe(stage);""","""  new ResizeObserver(resize).observe(stage);
  if(DESK_RING){ document.body.classList.add('ring'); document.body.appendChild($('derby')); setTimeout(openDerby, 50); } else deskHooks();""")
# selection of the sprite from data URI
b64 = base64.b64encode(open('umimi-sprites.png','rb').read()).decode()
R("sprImg.src = 'umimi-sprites.png';", "sprImg.src = SPRITE_DATA;")
# おきがえは色変え（getImageData）を使うので、file:// で読まず data URI で埋め込む（読み込みは使うときだけ）
import glob as _g0
R("im.src='c_'+cat+'.png';", "im.src=COS_DATA[cat];")
s = "const COS_DATA = {" + ",".join("%s:'data:image/png;base64,%s'" % (f[2:-4], base64.b64encode(open(f,'rb').read()).decode()) for f in sorted(_g0.glob('c_*.png'))) + "};\n" + s
R("const DESK_RING = false;", "const DESK_RING = location.hash==='#derby';")
R("visImg.src = 'visitors.png';", "visImg.src = VIS_DATA;")
s = "const VIS_DATA = 'data:image/png;base64," + base64.b64encode(open('visitors.png','rb').read()).decode() + "';\n" + s
# desktop hooks: settings, click-through
R("""// ---------- boot ----------""","""// ---------- desktop hooks ----------
let interactive = null;
function setInter(v){ if(v===interactive) return; interactive=v; try{ window.desk && window.desk.setInteractive(v); }catch(e){} }
function overItems(p){
  if(hitUmimi(p) || hitShard(p)) return true;
  if(PARTY && balloons.some(b => Math.hypot(p.x-b.x,(p.y-b.y)*.9) < b.r*1.2)) return true;
  if(star && Math.hypot(p.x-star.x,p.y-star.y) < 90) return true;
  return false;
}
function deskHooks(){
  window.addEventListener('mousemove', e => {
    if(drag){ setInter(true); return; }
    const el = document.elementFromPoint(e.clientX, e.clientY);
    if(el && el !== cv && el.closest('.ui')){ setInter(true); return; }
    const p = toWorld(e);
    setInter(p.y > tankTop - 6 || overItems(p));
  });
  document.addEventListener('mouseleave', () => { if(!drag) setInter(false); });
  if(window.desk){
    if(window.desk.onDerbyClosed) window.desk.onDerbyClosed(() => location.reload());
    window.desk.onCfg(c => {
      const ecoChanged = SET.eco !== c.eco; SET = Object.assign(SET, c);
      S.sound = !!c.sound; S.timeMode = c.timeMode || 'auto'; S.profileOnTap = c.profileOnTap !== false; if(!S.profileOnTap) closeCard(); tPhase = targetPhase(); updateTimeBtn();
      if(S.sound) ensureAudio();
      if(ecoChanged) resize();
    });
  }
}

// ---------- boot ----------""")
s = "const SPRITE_DATA = 'data:image/png;base64," + b64 + "';\n" + s

head = open('desktop/desktop_head.html').read()
import re as _re
css_src = src.split('<style>')[1].split('</style>')[0]
pat = _re.compile(r'^(\.derby|\.dgrid|\.dcard|\.dbar|\.dbtn|\.dres|\.dmsg|\.dmode|\.dm[{.:]|\.dplayers|\.dpl|\.dedit|\.who|\.dstat|\.dsbox|\.dh3|\.dmedal|\.dbet|\.dmt|\.dmth|\.dmr|\.dshop|\.dsrow|\.dsi|\.dbt|\.dbtrow|\.dsum|\.dbulk|#derbyBody)')
dcss = '\n'.join(l for l in css_src.split('\n') if pat.match(l))
dcss += '''
body.ring{background:transparent!important}
body.ring main{display:none!important}
body.ring #derby{position:fixed;inset:auto;left:50%;top:50%;transform:translate(-50%,-50%);width:min(860px,92vw);max-height:84vh;overflow:auto;z-index:10;font-size:14px}
body.ring #derby.racing{display:none!important}
#derby .x{position:absolute;right:8px;top:6px;border:0;background:none;font-size:22px;cursor:pointer;color:var(--ink2)}
'''
head = head.replace('</style>', dcss + '\n</style>', 1)
# 家具（f_*.png）と模様は app フォルダに png のまま同梱する（使うときだけ読み込む）
import glob as _glob, shutil as _sh
for _f in _glob.glob('f_*.png')+['roomtex.png']: _sh.copy(_f, 'desktop/app/'+_f)
open('desktop/app/index.html','w').write(head + "\n<script>" + s + "</script>\n</body></html>\n")
print('built', len(s))
