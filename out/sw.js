// 설치(앱으로 인정)에 필요한 서비스워커: 인터넷이 되면 항상 최신, 안 되면 저장해 둔 것을 보여 줌
const NAME = 'star-v1', FILES = ['./', 'index.html', 'skydata.js', 'astronomy.browser.min.js', 'info.js', 'manifest.json', 'icon-192.png', 'icon-512.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(NAME).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== NAME).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(fetch(e.request).then(r => { const cp = r.clone(); caches.open(NAME).then(c => c.put(e.request, cp)); return r; }).catch(() => caches.match(e.request)));
});
