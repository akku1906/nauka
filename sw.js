/* Service worker aplikacji Nauka.
   Powłoka (index, manifest, ikony): zapisana z góry, podawana z pamięci. Nowa powłoka = nowa WERSJA,
   która czeka, aż uczennica stuknie „Odśwież” (albo zamknie aplikację), więc nic nie przeładowuje się w trakcie zadania.
   Tematy (tematy/index.json i tematy/*.md): najpierw sieć, potem pamięć. Przy każdym pobraniu katalogu
   pobieramy do pamięci wszystkie tematy z katalogu, także te jeszcze nieotwierane.
   WERSJĘ ustawia narzedzia/wersja.py na podstawie skrótu plików powłoki. */
const WERSJA='2026-11-04.b2b4e753';
const POWLOKA='nauka-powloka-'+WERSJA;
const TEMATY='nauka-tematy';
const PLIKI_POWLOKI=['index.html','manifest.webmanifest','ikony/ikona-192.png','ikony/ikona-512.png','ikony/ikona-maskable-192.png','ikony/ikona-maskable-512.png'];
const CZAS_SIECI=4000; // po tylu ms bez odpowiedzi sieci podajemy temat z pamięci (sieć dalej aktualizuje pamięć w tle)

const adres=p=>new URL(p,self.registration.scope).href;

self.addEventListener('install',e=>{
  e.waitUntil((async()=>{
    const c=await caches.open(POWLOKA);
    // cache:'reload' omija pamięć HTTP przeglądarki, żeby nie zapisać starej powłoki po wdrożeniu
    await c.addAll(PLIKI_POWLOKI.map(p=>new Request(adres(p),{cache:'reload'})));
    try{await pobierzTematy();}catch(err){}
  })());
});

self.addEventListener('activate',e=>{
  e.waitUntil((async()=>{
    for(const k of await caches.keys())if(k.startsWith('nauka-powloka-')&&k!==POWLOKA)await caches.delete(k);
    await self.clients.claim();
  })());
});

self.addEventListener('message',e=>{
  if(e.data&&e.data.typ==='aktywuj')self.skipWaiting();
});

async function pobierzTematy(odpKatalogu){
  const c=await caches.open(TEMATY);
  let res=odpKatalogu;
  if(!res){
    res=await fetch(adres('tematy/index.json'),{cache:'no-cache'});
    if(!res.ok)return;
    await c.put(adres('tematy/index.json'),res.clone());
  }
  const kat=await res.json();
  const pliki=(Array.isArray(kat.tematy)?kat.tematy:[]).filter(t=>t&&t.plik).map(t=>adres('tematy/'+t.plik));
  await Promise.all(pliki.map(async u=>{
    try{const r=await fetch(u,{cache:'no-cache'});if(r.ok)await c.put(u,r);}catch(err){}
  }));
}

const czekaj=ms=>new Promise(r=>setTimeout(r,ms));

async function najpierwSiec(e,klucz,katalog){
  const c=await caches.open(TEMATY);
  const zSieci=fetch(klucz,{cache:'no-cache'}).then(res=>{
    if(res.ok){
      // kopie robimy od razu, zanim strona zacznie czytać odpowiedź
      const doPamieci=res.clone(),doKatalogu=katalog?res.clone():null;
      const praca=(async()=>{await c.put(klucz,doPamieci);if(doKatalogu)await pobierzTematy(doKatalogu);})().catch(()=>{});
      try{e.waitUntil(praca);}catch(err){}
    }
    return res;
  });
  const zPamieci=await c.match(klucz);
  if(!zPamieci)return zSieci;
  try{e.waitUntil(zSieci.catch(()=>{}));}catch(err){}
  return Promise.race([
    zSieci.then(res=>res.ok?res:zPamieci,()=>zPamieci),
    czekaj(CZAS_SIECI).then(()=>zPamieci),
  ]);
}

self.addEventListener('fetch',e=>{
  const req=e.request;
  if(req.method!=='GET')return;
  const u=new URL(req.url);
  const scope=new URL(self.registration.scope);
  if(u.origin!==scope.origin||!u.pathname.startsWith(scope.pathname))return;
  const rel=u.pathname.slice(scope.pathname.length);
  if(req.mode==='navigate'){
    if(rel===''||rel==='index.html'){
      e.respondWith(caches.open(POWLOKA).then(c=>c.match(adres('index.html'))).then(r=>r||fetch(req)));
    }
    return;
  }
  if(rel.startsWith('tematy/')){
    e.respondWith(najpierwSiec(e,adres(rel),rel==='tematy/index.json'));
    return;
  }
  if(PLIKI_POWLOKI.includes(rel)){
    e.respondWith(caches.open(POWLOKA).then(c=>c.match(adres(rel))).then(r=>r||fetch(req)));
  }
});
