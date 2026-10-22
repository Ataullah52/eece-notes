addEventListener('DOMContentLoaded',()=>{
const d=document,r=d.body.dataset.root||'.',root=d.documentElement,K='eece-notes-theme';
const f=d.createElement('link');f.rel='stylesheet';f.href='https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&family=Outfit:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap';d.head.append(f);
const sv=localStorage.getItem(K);if(sv)root.dataset.theme=sv;
const isDark=()=>root.dataset.theme?root.dataset.theme==='dark':matchMedia('(prefers-color-scheme:dark)').matches;
const home=r+'/index.html',unit=d.querySelector('h1'),nav=d.createElement('nav');nav.className='topbar';
const depth=r==='.'?0:r.split('/').length,file=location.pathname.split('/').pop(),isIdx=file===''||file==='index.html';
const dirs=location.pathname.split('/').slice(0,-1).filter(Boolean).slice(-depth||undefined).slice(depth?0:99);
let cr='',up=r;const links=dirs.map((x,i)=>r+'/'+dirs.slice(0,i+1).join('/')+'/index.html');
dirs.forEach((x,i)=>{cr+=' › '+(i<dirs.length-1||!isIdx?'<a href="'+links[i]+'">'+x.toUpperCase()+'</a>':'<b>'+x.toUpperCase()+'</b>')});
if(!isIdx&&unit)cr+=' › <b>'+unit.textContent+'</b>';
nav.innerHTML='<a href="'+home+'">⌂ Home</a><span class="crumbs">'+cr+'</span><button id="tg" aria-label="Toggle dark mode"></button><button onclick="print()">⬇ Save as PDF</button>';
d.body.prepend(nav);
if(unit&&!isIdx){const hs=[...d.querySelectorAll('main h2')];
if(hs.length>2){hs.forEach((h,i)=>h.id=h.id||'s'+(i+1));const t=d.createElement('div');t.className='toc';
t.innerHTML='<b>Contents</b><ol>'+hs.map(h=>'<li><a href="#'+h.id+'">'+h.innerHTML.replace(/<[^>]+>/g,'')+'</a></li>').join('')+'</ol>';
const p=unit.nextElementSibling;(p&&p.tagName==='P'?p:unit).after(t);}}
const tg=d.getElementById('tg'),sync=()=>tg.textContent=isDark()?'☀ Light':'☾ Dark';sync();
tg.onclick=()=>{const n=isDark()?'light':'dark';root.dataset.theme=n;localStorage.setItem(K,n);sync()};
if(!/\\\(|\\\[/.test(d.body.innerHTML))return;
const k='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/',l=d.createElement('link');l.rel='stylesheet';l.href=k+'katex.min.css';d.head.append(l);
const s=u=>new Promise((o,e)=>{const x=d.createElement('script');x.src=u;x.onload=o;x.onerror=e;d.head.append(x)});
s(k+'katex.min.js').then(()=>s(k+'contrib/auto-render.min.js')).then(()=>renderMathInElement(d.body,{delimiters:[{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false}]})).catch(()=>{});
});
