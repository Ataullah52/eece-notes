addEventListener('DOMContentLoaded',()=>{
const r=document.body.dataset.root||'.',b=document.createElement('nav');b.className='topbar';
b.innerHTML='<a href="'+r+'/index.html">⌂ Home</a><button onclick="print()">⬇ Save as PDF</button>';
document.body.prepend(b);
if(!document.querySelector('main :is(.definition,.theory,.memorize,.example,.pyq,.warn,p,td)')||!/\\\(|\\\[/.test(document.body.innerHTML))return;
const k='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/',l=document.createElement('link');l.rel='stylesheet';l.href=k+'katex.min.css';document.head.append(l);
const s=u=>new Promise((o,e)=>{const x=document.createElement('script');x.src=u;x.onload=o;x.onerror=e;document.head.append(x)});
s(k+'katex.min.js').then(()=>s(k+'contrib/auto-render.min.js')).then(()=>renderMathInElement(document.body,{delimiters:[{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false}]})).catch(()=>{});
});
