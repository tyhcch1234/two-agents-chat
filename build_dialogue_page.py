#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate index.html from agent-dialogue-200.md"""
import re, html, json, pathlib

SRC = pathlib.Path("agent-dialogue-200.md")
OUT = pathlib.Path("index.html")

rows = []
pat = re.compile(r"^\*\*(\d+)（(.+?)）\*\*\s*(.*)$")
for line in SRC.read_text(encoding="utf-8").splitlines():
    m = pat.match(line.strip())
    if m:
        rows.append({"n": int(m.group(1)), "who": m.group(2), "text": m.group(3).strip()})

assert len(rows) == 200, len(rows)

data_js = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))

TPL = r"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>兩個 Agent 傾偈 · 頭 200 句</title>
<meta name="description" content="阿嵐同阿澄，兩個獨立 AI agent 經傳話輪流對話 200 句，全程廣東話。">
<meta property="og:title" content="兩個 Agent 傾偈 · 頭 200 句">
<meta property="og:description" content="阿嵐同阿澄，兩個獨立 AI agent 經傳話輪流對話 200 句，全程廣東話。">
<meta property="og:type" content="article">
<style>
:root{--bg:#0b0e14;--panel:#121722;--line:#222a38;--ink:#e8edf5;--dim:#8b96a8;
--a:#5eead4;--a-bg:#0f2b2c;--b:#fbbf6e;--b-bg:#2b2113;--accent:#8ea6ff}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans HK","PingFang HK",sans-serif;
line-height:1.65;-webkit-font-smoothing:antialiased}
.wrap{max-width:760px;margin:0 auto;padding:0 18px 90px}

/* header */
header{padding:56px 0 28px;border-bottom:1px solid var(--line);margin-bottom:8px}
.eyebrow{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--dim);margin:0 0 14px}
h1{font-size:clamp(26px,6vw,38px);line-height:1.25;margin:0 0 14px;letter-spacing:-.02em}
h1 em{font-style:normal;color:var(--a)}
.lede{color:var(--dim);font-size:15px;margin:0 0 22px;max-width:60ch}

/* cast */
.cast{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0 0 22px}
.person{border:1px solid var(--line);border-radius:14px;padding:14px 15px;background:var(--panel)}
.person .nm{font-weight:700;font-size:15px;display:flex;align-items:center;gap:8px;margin-bottom:6px}
.dot{width:9px;height:9px;border-radius:50%;flex:none}
.person p{margin:0;font-size:13px;color:var(--dim);line-height:1.55}

/* stats */
.stats{display:flex;flex-wrap:wrap;gap:8px}
.stat{border:1px solid var(--line);background:var(--panel);border-radius:999px;
padding:6px 13px;font-size:12.5px;color:var(--dim)}
.stat b{color:var(--ink);font-variant-numeric:tabular-nums}

/* toolbar */
.toolbar{position:sticky;top:0;z-index:20;background:rgba(11,14,20,.88);
backdrop-filter:blur(12px);border-bottom:1px solid var(--line);
padding:12px 0;margin-bottom:18px;display:flex;gap:10px;align-items:center}
.toolbar input{flex:1;min-width:0;background:var(--panel);border:1px solid var(--line);
border-radius:11px;padding:10px 14px;color:var(--ink);font-size:14px;font-family:inherit;outline:none}
.toolbar input:focus{border-color:#3a4a68}
.toolbar input::placeholder{color:#5d6879}
.tgl{border:1px solid var(--line);background:var(--panel);color:var(--dim);
border-radius:11px;padding:10px 14px;font-size:13px;font-family:inherit;cursor:pointer;white-space:nowrap}
.tgl[aria-pressed="true"]{color:var(--a);border-color:rgba(94,234,212,.5)}

/* messages */
.msg{display:flex;flex-direction:column;margin:0 0 14px;animation:in .28s ease both}
.msg.right{align-items:flex-end}
@keyframes in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.meta{font-size:11px;color:#5f6b7d;margin:0 4px 5px;display:flex;gap:7px;align-items:center}
.right .meta{flex-direction:row-reverse}
.meta .who{font-weight:700;letter-spacing:.02em}
.msg.left .who{color:var(--a)}
.msg.right .who{color:var(--b)}
.bubble{max-width:86%;padding:11px 15px;border-radius:16px;font-size:15px;
background:var(--panel);border:1px solid var(--line);white-space:pre-wrap;overflow-wrap:anywhere}
.msg.left .bubble{border-bottom-left-radius:5px;background:var(--a-bg);border-color:#1c3f3d}
.msg.right .bubble{border-bottom-right-radius:5px;background:var(--b-bg);border-color:#443420}
.bubble mark{background:rgba(142,166,255,.28);color:inherit;border-radius:3px;padding:0 2px}

/* compact */
body.compact .bubble{font-size:13.5px;padding:7px 12px;max-width:94%}
body.compact .msg{margin-bottom:7px}
body.compact .meta{font-size:10px;margin-bottom:2px}

/* misc */
.sep{display:flex;align-items:center;gap:10px;color:#4d5768;font-size:11px;
letter-spacing:.16em;text-transform:uppercase;margin:34px 0 22px}
.sep::before,.sep::after{content:"";flex:1;height:1px;background:var(--line)}
.empty{text-align:center;color:var(--dim);padding:50px 0;font-size:14px}
footer{margin-top:44px;padding-top:22px;border-top:1px solid var(--line);
color:var(--dim);font-size:12.5px;display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between}
footer a{color:var(--accent);text-decoration:none;border-bottom:1px solid rgba(142,166,255,.3)}
#top{position:fixed;right:16px;bottom:16px;width:42px;height:42px;border-radius:50%;
border:1px solid var(--line);background:var(--panel);color:var(--dim);cursor:pointer;
font-size:16px;display:grid;place-items:center;opacity:0;pointer-events:none;transition:.2s}
#top.on{opacity:1;pointer-events:auto}
@media(max-width:520px){
  .cast{grid-template-columns:1fr}
  .bubble{max-width:92%}
  header{padding-top:40px}
}
@media(prefers-color-scheme:light){
  :root{--bg:#f7f8fa;--panel:#fff;--line:#e3e6ec;--ink:#141922;--dim:#5d6675;
  --a:#0f766e;--a-bg:#f0fdfa;--b:#9a5b12;--b-bg:#fffaf0;--accent:#3b5bdb}
  .msg.left .bubble{border-color:#cceee8}
  .msg.right .bubble{border-color:#f2e3c9}
  .toolbar{background:rgba(247,248,250,.9)}
  .toolbar input::placeholder{color:#9aa3b2}
}
</style>
</head>
<body>
<div class="wrap">
<header>
  <p class="eyebrow">Two agents · one conversation</p>
  <h1><em>阿嵐</em> 同 <em>阿澄</em> 傾咗 200 句</h1>
  <p class="lede">兩個獨立 AI agent，冇劇本、冇設定話題範圍。每一句都係真生成，再逐句傳去另一邊，順住上一句自然發展落去。</p>

  <div class="cast">
    <div class="person">
      <div class="nm"><span class="dot" style="background:var(--a)"></span>阿嵐</div>
      <p>香港長大，做過飲食記者，現做城市研究。好奇、鍾意講故事、識自嘲。</p>
    </div>
    <div class="person">
      <div class="nm"><span class="dot" style="background:var(--b)"></span>阿澄</div>
      <p>機械工程師，鍾意科幻同城市規劃。務實、直接、冷幽默。</p>
    </div>
  </div>

  <div class="stats">
    <span class="stat"><b>200</b> 句</span>
    <span class="stat">阿嵐 <b>115</b></span>
    <span class="stat">阿澄 <b>85</b></span>
    <span class="stat"><b>19</b> 輪來回</span>
    <span class="stat">廣東話</span>
  </div>
</header>

<div class="toolbar">
  <input id="q" type="search" placeholder="搵句子，例如：鑊、雪櫃、火候" aria-label="搜尋對話">
  <button class="tgl" id="c" type="button" aria-pressed="false">精簡</button>
</div>

<div class="sep">對話開始</div>
<main id="list"></main>

<footer>
  <span>共 200 句 · 阿嵐 115 · 阿澄 85</span>
  <a href="https://github.com/tyhcch1234/two-agents-chat" target="_blank" rel="noopener">原始 markdown ↗</a>
</footer>
</div>
<button id="top" type="button" aria-label="返頂">↑</button>

<script>
const DATA = __DATA__;
const list = document.getElementById('list');
const q = document.getElementById('q');
const cBtn = document.getElementById('c');
const topBtn = document.getElementById('top');
let compact = false;

function esc(s){return s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function hl(s,term){
  const e = esc(s);
  if(!term) return e;
  try{
    const safe = term.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
    return e.replace(new RegExp('('+safe+')','gi'),'<mark>$1</mark>');
  }catch(_){ return e }
}

function render(term){
  const t = (term||'').trim();
  const hits = t ? DATA.filter(m=>m.text.includes(t)||m.who.includes(t)) : DATA;
  if(!hits.length){
    list.innerHTML = '<p class="empty">冇句子包含「'+esc(t)+'」</p>';
    return;
  }
  list.innerHTML = hits.map(m=>{
    const side = m.who === '阿嵐' ? 'left' : 'right';
    return '<div class="msg '+side+'">'
      + '<div class="meta"><span class="who">'+esc(m.who)+'</span><span>#'+m.n+'</span></div>'
      + '<div class="bubble">'+hl(m.text,t)+'</div></div>';
  }).join('');
}

q.addEventListener('input', ()=>render(q.value));
cBtn.addEventListener('click', ()=>{
  compact = !compact;
  document.body.classList.toggle('compact', compact);
  cBtn.setAttribute('aria-pressed', String(compact));
});
window.addEventListener('scroll', ()=>{
  topBtn.classList.toggle('on', window.scrollY > 600);
});
topBtn.addEventListener('click', ()=>window.scrollTo({top:0,behavior:'smooth'}));

render('');
</script>
</body>
</html>
"""

OUT.write_text(TPL.replace("__DATA__", data_js), encoding="utf-8")
print("rows:", len(rows), "->", OUT, OUT.stat().st_size, "bytes")
