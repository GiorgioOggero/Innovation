(function(){
  const body=document.body;
  const langs=['en','it','ar','de','es','zh'];
  const stored=localStorage.getItem('site-lang')||'en';
  setLang(langs.includes(stored)?stored:'en');

  document.querySelectorAll('[data-lang]').forEach(btn=>btn.addEventListener('click',()=>setLang(btn.dataset.lang)));

  function setLang(lang){
    langs.forEach(l=>body.classList.toggle('lang-'+l,l===lang));
    body.classList.toggle('rtl',lang==='ar');
    document.documentElement.lang=lang;
    document.documentElement.dir=lang==='ar'?'rtl':'ltr';
    localStorage.setItem('site-lang',lang);
  }

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
