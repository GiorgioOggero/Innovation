(function(){
  const body=document.body;
  const stored=localStorage.getItem('site-lang')||'en';
  setLang(stored);
  document.querySelectorAll('[data-lang]').forEach(btn=>btn.addEventListener('click',()=>setLang(btn.dataset.lang)));
  function setLang(lang){body.classList.toggle('lang-it',lang==='it');body.classList.toggle('lang-en',lang==='en');localStorage.setItem('site-lang',lang);document.documentElement.lang=lang;}
  const hamburger=document.querySelector('.hamb'); const nav=document.querySelector('.nav-links');
  if(hamburger&&nav){hamburger.addEventListener('click',()=>nav.classList.toggle('open'));}
  const obs=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('in')}),{threshold:.12});
  document.querySelectorAll('.fade-up').forEach(el=>obs.observe(el));
  document.querySelectorAll('[data-tilt]').forEach(card=>{
    card.addEventListener('mousemove',e=>{const r=card.getBoundingClientRect();const x=(e.clientX-r.left)/r.width-.5;const y=(e.clientY-r.top)/r.height-.5;card.style.transform=`perspective(900px) rotateY(${x*5}deg) rotateX(${-y*5}deg) translateY(-4px)`});
    card.addEventListener('mouseleave',()=>card.style.transform='');
  });
  const counters=document.querySelectorAll('[data-counter]');
  const cobs=new IntersectionObserver(entries=>entries.forEach(e=>{if(!e.isIntersecting||e.target.dataset.done)return; e.target.dataset.done=1; const target=+e.target.dataset.counter; let n=0; const step=Math.max(1,Math.ceil(target/45)); const t=setInterval(()=>{n+=step;if(n>=target){n=target;clearInterval(t)}e.target.textContent=n+(e.target.dataset.suffix||'')},30)}),{threshold:.5});
  counters.forEach(c=>cobs.observe(c));
})();
(function(){const file=location.pathname.split('/').pop()||'index.html';document.querySelectorAll('.nav-links a').forEach(a=>{if(a.getAttribute('href')===file)a.classList.add('active')});})();
