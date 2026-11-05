/* Liberty Park option pages. Inlined into each page by build.py, after the
   VIEWS and IMG_BASE constants. One requestAnimationFrame loop drives every
   scroll-linked effect; nothing here runs when the visitor asks for reduced
   motion except the full-size viewer and the hero slideshow. */
(function () {
  'use strict';

  var root = document.documentElement;
  var motion = root.classList.contains('motion');
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.min(b === undefined ? 1 : b, Math.max(a === undefined ? 0 : a, v)); };
  var easeOut = function (t) { return 1 - Math.pow(1 - t, 3); };
  var easeInOut = function (t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };

  /* ---------- hero: split the title, open the iris, run the slideshow ---------- */
  var title = $('[data-chars]');
  if (title) {
    var label = title.textContent;
    title.setAttribute('aria-label', label);
    title.textContent = '';
    label.split('').forEach(function (c, i) {
      var s = document.createElement('span');
      s.className = 'ch';
      s.setAttribute('aria-hidden', 'true');
      s.style.setProperty('--i', i);
      s.textContent = c;
      title.appendChild(s);
    });
  }

  var slides = $$('.hero__slide');
  var ticks = $$('.hero__ticks i');
  var SLIDE_MS = 6500;
  var current = 0;
  function show(i) {
    var prev = current;
    current = i;
    slides.forEach(function (s, k) {
      s.classList.toggle('was', k === prev && k !== i);
      s.classList.toggle('on', k === i);
    });
    ticks.forEach(function (t, k) {
      t.classList.remove('on');
      if (k === i) { void t.offsetWidth; t.classList.add('on'); }
    });
  }
  function startSlides() {
    show(0);
    if (slides.length > 1) {
      setInterval(function () {
        if (!document.hidden) show((current + 1) % slides.length);
      }, SLIDE_MS);
    }
  }

  var opened = false;
  function open() {
    if (opened) return;
    opened = true;
    root.classList.add('ready');
    startSlides();
    setTimeout(function () { root.classList.add('opened'); }, 1900);
  }
  // open as soon as the first picture has arrived, or after 2.5 s regardless
  var first = slides[0] && $('img', slides[0]);
  if (!first || first.complete) open();
  else { first.addEventListener('load', open); first.addEventListener('error', open); }
  setTimeout(open, 2500);

  /* ---------- full-size viewer ---------- */
  var lb = $('#lb');
  var lbImg = $('#lb-img');
  var lbScroll = $('.lb__scroll', lb);
  var lbFit = $('.lb__fit', lb);
  var lbIndex = 0;
  var lbReturn = null;

  function lbSize() {
    if (innerWidth < 700) return 1920;   // sharp enough on a phone at a third less data
    var need = innerWidth * (window.devicePixelRatio || 1);
    return need > 2000 ? 2560 : need > 1400 ? 1920 : 1280;
  }
  function lbCenter() {
    if (lb.classList.contains('fill')) lbScroll.scrollLeft = (lbScroll.scrollWidth - lbScroll.clientWidth) / 2;
  }
  function lbShow(i) {
    lbIndex = (i + VIEWS.length) % VIEWS.length;
    var v = VIEWS[lbIndex];
    lbImg.style.animation = 'none';
    void lbImg.offsetWidth;
    lbImg.style.animation = '';
    lbImg.src = IMG_BASE + v.n + '-' + lbSize() + '.jpg';
    lbImg.alt = v.t + '. ' + v.d;
    $('#lb-n').textContent = v.t;
    $('#lb-t').textContent = v.d;
    lbCenter();
  }
  function lbMode(fill) {
    lb.classList.toggle('fill', fill);
    lbFit.textContent = fill ? 'Fit to screen' : 'Fill the screen';
    lbCenter();
  }
  function lbOpen(i, from) {
    lbReturn = from || null;
    lb.hidden = false;
    document.body.classList.add('lb-open');
    lbMode(innerHeight > innerWidth);
    lbShow(i);
    $('.lb__x', lb).focus();
  }
  function lbClose() {
    lb.hidden = true;
    document.body.classList.remove('lb-open');
    if (lbReturn) lbReturn.focus();
  }
  lbImg.addEventListener('load', lbCenter);
  $$('[data-open]').forEach(function (b) {
    b.addEventListener('click', function () { lbOpen(+b.getAttribute('data-open'), b); });
  });
  $('.lb__x', lb).addEventListener('click', lbClose);
  $('.lb__prev', lb).addEventListener('click', function () { lbShow(lbIndex - 1); });
  $('.lb__next', lb).addEventListener('click', function () { lbShow(lbIndex + 1); });
  lbFit.addEventListener('click', function () { lbMode(!lb.classList.contains('fill')); });
  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') lbClose();
    else if (e.key === 'ArrowLeft') lbShow(lbIndex - 1);
    else if (e.key === 'ArrowRight') lbShow(lbIndex + 1);
    else if (e.key === 'Tab') {
      // keep focus inside the viewer
      var f = $$('button', lb);
      var a = document.activeElement;
      if (e.shiftKey && a === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && a === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  });
  // swipe between views when the picture is fitted (when filled, dragging pans it)
  var sx = null;
  lbScroll.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
  lbScroll.addEventListener('touchend', function (e) {
    if (sx === null || lb.classList.contains('fill')) { sx = null; return; }
    var dx = e.changedTouches[0].clientX - sx;
    sx = null;
    if (Math.abs(dx) > 50) lbShow(lbIndex + (dx < 0 ? 1 : -1));
  });

  if (!motion) return;

  /* ---------- everything below is scroll-linked motion ---------- */

  // Reveal-on-enter for the grid and headings. These start fully clipped by
  // clip-path, and an IntersectionObserver never reports a fully clipped
  // element as visible, so the scroll loop checks their boxes instead.
  var pending = $$('.view').concat($$('[data-rise]'));
  $$('.view').forEach(function (v, i) { v.style.setProperty('--d', i % 3); });
  function reveal() {
    for (var i = pending.length - 1; i >= 0; i--) {
      var r = pending[i].getBoundingClientRect();
      // anything at or above the lower edge counts, so a jump to the bottom of
      // the page does not leave the pictures it skipped still hidden
      if (r.top < vh * 0.9) {
        pending[i].classList.add('in');
        pending.splice(i, 1);
      }
    }
  }

  // lede: words light up as the paragraph crosses the screen
  var lede = $('[data-words]');
  var words = [];
  if (lede) {
    var text = lede.textContent.trim().split(/\s+/);
    lede.setAttribute('aria-label', text.join(' '));
    lede.textContent = '';
    text.forEach(function (w, i) {
      var s = document.createElement('span');
      s.className = 'w';
      s.setAttribute('aria-hidden', 'true');
      s.textContent = w;
      lede.appendChild(s);
      if (i < text.length - 1) lede.appendChild(document.createTextNode(' '));
      words.push(s);
    });
  }

  var bar = $('.bar__progress');
  var heroText = $('.hero__text');
  var hero = $('.hero');

  var wheel = $('.wheel');
  var disc = $('.wheel__disc');
  var ring = $('.wheel__ring');
  var zones = $$('.wheel__zones li');
  var zoneTicks = $$('.wheel__ticks i');
  var wide = matchMedia('(min-width:900px) and (min-aspect-ratio:1/1)');
  // Rotation that brings each play area round to face the text: the text sits
  // below the wheel on a phone and to its right on a wide screen. The areas
  // are the left half, the lower-right quarter and the upper-right quarter of
  // the plan render, in that order.
  var TURN_BELOW = [-90, 45, 135];
  var TURN_RIGHT = [-180, -45, 45];
  var angle = -200;
  var zoneNow = -1;

  var walk = $('.walk');
  var walkPin = $('.walk__pin');
  var track = $('.walk__track');
  var scenes = $$('.scene').map(function (el) {
    return { el: el, frame: $('.scene__frame', el), img: $('img', el), left: 0, width: 0, pan: 0 };
  });
  var count = $('.walk__count b');
  var travel = 0;
  var countNow = 0;

  var aboves = $$('.above');
  var rows = $$('.band__row').map(function (el) {
    return { el: el, dir: +el.getAttribute('data-dir'), x: 0, half: 0 };
  });

  var vw = innerWidth;
  var vh = innerHeight;

  function measure() {
    vw = innerWidth;
    vh = innerHeight;
    track.style.transform = 'none';
    travel = Math.max(0, track.scrollWidth - walkPin.clientWidth);
    scenes.forEach(function (s) {
      // viewport position with the track at rest; the pin starts at the left edge
      s.left = s.frame.getBoundingClientRect().left;
      s.width = s.frame.clientWidth;
      s.pan = Math.max(0, s.img.offsetWidth - s.width);
    });
    rows.forEach(function (r) { r.half = r.el.scrollWidth / 2; });
  }

  function progress(el) {
    var r = el.getBoundingClientRect();
    return clamp(-r.top / Math.max(1, r.height - vh));
  }

  var lastY = window.pageYOffset;
  var vel = 0;
  var t0 = performance.now();

  var lastT = t0;

  function frame(now) {
    // Everything eased here is eased by elapsed time, not by frame count, so
    // it looks the same on a 120 Hz phone and on a throttled background tab.
    var dt = clamp(now - lastT, 1, 100);
    lastT = now;
    var y = window.pageYOffset;
    vel += ((y - lastY) / dt * 1000 - vel) * (1 - Math.exp(-dt / 110));   // px per second
    lastY = y;

    if (pending.length) reveal();

    // top progress line
    var max= Math.max(1, document.documentElement.scrollHeight - vh);
    bar.style.transform = 'scaleX(' + clamp(y / max) + ')';

    // hero: the text drifts up and fades as the page starts to move
    if (y < vh * 1.2) {
      var h = clamp(y / (vh * 0.8));
      heroText.style.transform = 'translate3d(0,' + (-y * 0.28) + 'px,0)';
      heroText.style.opacity = 1 - h;
      hero.style.setProperty('--hero-p', h);
    }

    // lede words
    if (words.length) {
      var lr = lede.getBoundingClientRect();
      if (lr.bottom > -vh && lr.top < vh * 2) {
        var lp = clamp((vh * 0.86 - lr.top) / (lr.height + vh * 0.42));
        var lit = lp * (words.length + 2);
        for (var i = 0; i < words.length; i++) {
          words[i].style.opacity = 0.16 + 0.84 * clamp(lit - i);
        }
      }
    }

    // plan wheel
    var wr = wheel.getBoundingClientRect();
    if (wr.bottom > -vh * 0.5 && wr.top < vh * 1.5) {
      var wp = clamp(-wr.top / Math.max(1, wr.height - vh));
      var enter = clamp((vh - wr.top) / vh);            // 0..1 while the section slides in
      var zf = wp * zones.length;
      var z = Math.min(zones.length - 1, Math.floor(zf));
      var turns = wide.matches ? TURN_RIGHT : TURN_BELOW;
      var target = turns[z] + (zf - z - 0.5) * 16 - (1 - enter) * 110;
      angle += (target - angle) * (1 - Math.exp(-dt / 190));
      disc.style.transform = 'rotate(' + angle.toFixed(2) + 'deg)';
      ring.style.transform = 'rotate(' + (-angle * 0.45 + (now - t0) * 0.004).toFixed(2) + 'deg)';
      if (z !== zoneNow) {
        zoneNow = z;
        zones.forEach(function (li, k) { li.classList.toggle('on', k === z); });
        zoneTicks.forEach(function (ti, k) { ti.classList.toggle('on', k === z); });
      }
    }

    // walk: the track slides sideways, and each picture pans inside its frame
    var kr = walk.getBoundingClientRect();
    if (kr.bottom > -vh * 0.5 && kr.top < vh * 1.5) {
      // hold the first and last pictures still for a moment at each end
      var kp = clamp((clamp(-kr.top / Math.max(1, kr.height - vh)) - 0.05) / 0.9);
      var x = -kp * travel;
      track.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,0)';
      var best = 0;
      var bestD = Infinity;
      for (var s = 0; s < scenes.length; s++) {
        var sc = scenes[s];
        var center = sc.left + x + sc.width / 2;
        var t = clamp((vw + sc.width / 2 - center) / (vw + sc.width));
        sc.img.style.transform = 'translate3d(' + (-t * sc.pan).toFixed(1) + 'px,0,0)';
        var d = Math.abs(center - vw / 2);
        if (d < bestD) { bestD = d; best = s; }
      }
      if (best !== countNow) { countNow = best; count.textContent = best + 1; }
    }

    // aerials: the frame opens out to the full screen, then the caption arrives
    for (var a = 0; a < aboves.length; a++) {
      var ar = aboves[a].getBoundingClientRect();
      if (ar.bottom < -vh * 0.5 || ar.top > vh * 1.5) continue;
      var lead = clamp((vh - ar.top) / vh);              // sliding into view
      var ap = clamp(-ar.top / Math.max(1, ar.height - vh));
      var e = easeInOut(clamp(lead * 0.35 + ap / 0.5 * 0.65));
      aboves[a].style.setProperty('--e', e.toFixed(4));
      aboves[a].style.setProperty('--c', easeOut(clamp((ap - 0.45) / 0.25)).toFixed(4));
      aboves[a].style.setProperty('--p', (a % 2 ? 1 - (lead + ap) / 2 : (lead + ap) / 2).toFixed(4));
    }

    // word bands: drift on their own, speed up with the scroll
    for (var b = 0; b < rows.length; b++) {
      var r = rows[b];
      if (!r.half) continue;
      r.x += r.dir * (42 + Math.min(2600, Math.abs(vel)) * 0.5) * dt / 1000;
      if (r.x <= -r.half) r.x += r.half;
      if (r.x > 0) r.x -= r.half;
      r.el.style.transform = 'translate3d(' + r.x.toFixed(1) + 'px,0,0)';
    }

    requestAnimationFrame(frame);
  }

  measure();
  addEventListener('resize', measure);
  addEventListener('load', measure);
  scenes.forEach(function (s) { s.img.addEventListener('load', measure); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
  requestAnimationFrame(frame);
})();
