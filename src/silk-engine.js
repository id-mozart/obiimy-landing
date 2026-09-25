/* Obiimy silk engine: Verlet cloth + anisotropic silk shader + procedural weave. Requires THREE (r128 UMD). */
window.SilkEngine = (function () {
  'use strict';

  function makeWeaveNormalMap(size) {
    size = size || 512;
    var c = document.createElement('canvas'); c.width = c.height = size;
    var ctx = c.getContext('2d');
    var img = ctx.createImageData(size, size), d = img.data;
    // height field: twill diagonal + fine thread ridges + noise
    var h = new Float32Array(size * size);
    for (var y = 0; y < size; y++) for (var x = 0; x < size; x++) {
      var tw = Math.sin((x + y) * 0.55) * 0.5 + 0.5;          // diagonal twill
      var th = Math.sin(x * 1.9) * 0.5 + 0.5;                  // warp threads
      var tv = Math.sin(y * 1.9) * 0.5 + 0.5;                  // weft threads
      var n = Math.random() * 0.25;
      h[y * size + x] = tw * 0.35 + th * 0.35 + tv * 0.2 + n * 0.1;
    }
    for (var y2 = 0; y2 < size; y2++) for (var x2 = 0; x2 < size; x2++) {
      var xl = h[y2 * size + ((x2 - 1 + size) % size)], xr = h[y2 * size + ((x2 + 1) % size)];
      var yu = h[((y2 - 1 + size) % size) * size + x2], yd = h[((y2 + 1) % size) * size + x2];
      var nx = (xl - xr) * 2.2, ny = (yu - yd) * 2.2, nz = 1.0;
      var l = Math.sqrt(nx * nx + ny * ny + nz * nz);
      var i = (y2 * size + x2) * 4;
      d[i] = (nx / l * 0.5 + 0.5) * 255; d[i + 1] = (ny / l * 0.5 + 0.5) * 255; d[i + 2] = (nz / l * 0.5 + 0.5) * 255; d[i + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
    var t = new THREE.CanvasTexture(c);
    t.wrapS = t.wrapT = THREE.RepeatWrapping;
    return t;
  }

  function makeShadowTexture() {
    var c = document.createElement('canvas'); c.width = c.height = 256;
    var ctx = c.getContext('2d');
    var g = ctx.createRadialGradient(128, 128, 10, 128, 128, 128);
    g.addColorStop(0, 'rgba(0,0,0,0.55)'); g.addColorStop(0.5, 'rgba(0,0,0,0.18)'); g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, 256, 256);
    return new THREE.CanvasTexture(c);
  }

  var VERT = [
    'attribute vec3 tangent;',
    'varying vec2 vUv; varying vec3 vN; varying vec3 vT; varying vec3 vP;',
    'void main(){',
    '  vUv = uv;',
    '  vN = normalize(normalMatrix * normal);',
    '  vT = normalize(normalMatrix * tangent);',
    '  vec4 mv = modelViewMatrix * vec4(position, 1.0); vP = mv.xyz;',
    '  gl_Position = projectionMatrix * mv;',
    '}'
  ].join('\n');

  var FRAG = [
    'precision highp float;',
    'uniform sampler2D uFront, uBack, uNextFront, uNextBack, uWeave;',
    'uniform float uMix, uWeaveRepeat, uWeaveScale, uGloss, uAniso, uEnvStrength, uTime, uTone, uDiffBase, uAnisoMix;',
    'uniform vec3 uLight, uEnvTop, uEnvBottom, uEnvTint, uSheen;',
    'varying vec2 vUv; varying vec3 vN; varying vec3 vT; varying vec3 vP;',
    'float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }',
    'void main(){',
    '  bool front = gl_FrontFacing;',
    '  vec3 N = normalize(vN); if(!front) N = -N;',
    '  vec3 T = normalize(vT - N * dot(vT, N)); vec3 B = cross(N, T);',
    '  vec3 wn = texture2D(uWeave, vUv * uWeaveRepeat).xyz * 2.0 - 1.0;',
    '  vec3 n = normalize(T * wn.x * uWeaveScale + B * wn.y * uWeaveScale + N * wn.z);',
    '  vec2 uv = front ? vUv : vec2(1.0 - vUv.x, vUv.y);',
    '  vec3 a = front ? texture2D(uFront, uv).rgb : texture2D(uBack, uv).rgb;',
    '  vec3 b = front ? texture2D(uNextFront, uv).rgb : texture2D(uNextBack, uv).rgb;',
    '  vec3 base = mix(a, b, uMix);',
    '  vec3 V = normalize(-vP); vec3 L = normalize(uLight); vec3 H = normalize(L + V);',
    '  float NdotL = dot(n, L);',
    '  float diff = uDiffBase + (1.0 - uDiffBase) * max(NdotL, 0.0) + 0.08 * max(-NdotL, 0.0);',
    '  float TdotH = dot(T, H);',
    '  float aniso = pow(sqrt(max(1.0 - TdotH * TdotH, 0.0)), 24.0) * uAniso;',
    '  float spec = pow(max(dot(n, H), 0.0), 90.0) * uGloss;',
    '  vec3 R = reflect(-V, n);',
    '  float up = clamp(R.y * 0.5 + 0.5, 0.0, 1.0);',
    '  vec3 env = mix(uEnvBottom, uEnvTop, smoothstep(0.15, 0.95, up));',
    '  float box1 = smoothstep(0.86, 0.985, dot(R, normalize(vec3(-0.35, 0.55, 0.75))));',
    '  float box2 = smoothstep(0.93, 0.995, dot(R, normalize(vec3(0.7, 0.2, 0.68))));',
    '  float fres = pow(1.0 - max(dot(n, V), 0.0), 3.5);',
    '  float grain = (hash(floor(gl_FragCoord.xy * 0.5)) - 0.5) * 0.035;',
    '  vec3 col = base * diff;',
    '  col += base * aniso * uAnisoMix + uSheen * aniso * 0.25;',
    '  col += env * uEnvStrength * (0.15 + 0.85 * fres);',
    '  col += uEnvTint * (box1 * 0.35 + box2 * 0.22) * (0.5 + 0.5 * fres);',
    '  col += vec3(spec);',
    '  col += grain;',
    '  if (uTone > 0.5) { col *= 1.12; col = (col * (2.51 * col + 0.03)) / (col * (2.43 * col + 0.59) + 0.14); }',
    '  gl_FragColor = vec4(col, 1.0);',
    '}'
  ].join('\n');

  function Cloth(nx, ny, w, h) {
    this.nx = nx; this.ny = ny; this.w = w; this.h = h;
    var n = nx * ny;
    this.pos = new Float32Array(n * 3); this.prev = new Float32Array(n * 3); this.acc = new Float32Array(n * 3);
    this.pinned = new Uint8Array(n); this.pinPos = new Float32Array(n * 3);
    this.cons = [];
    var dx = w / (nx - 1), dy = h / (ny - 1);
    for (var j = 0; j < ny; j++) for (var i = 0; i < nx; i++) {
      var k = j * nx + i;
      this.pos[k * 3] = -w / 2 + i * dx; this.pos[k * 3 + 1] = h / 2 - j * dy; this.pos[k * 3 + 2] = 0;
    }
    this.prev.set(this.pos);
    var self = this;
    function add(a, b, type) { var d = self.dist(a, b); self.cons.push(a, b, d, type); }
    for (var j2 = 0; j2 < ny; j2++) for (var i2 = 0; i2 < nx; i2++) {
      var k2 = j2 * nx + i2;
      if (i2 < nx - 1) add(k2, k2 + 1, 0);
      if (j2 < ny - 1) add(k2, k2 + nx, 0);
      if (i2 < nx - 1 && j2 < ny - 1) { add(k2, k2 + nx + 1, 1); add(k2 + 1, k2 + nx, 1); }
      if (i2 < nx - 2) add(k2, k2 + 2, 2);
      if (j2 < ny - 2) add(k2, k2 + 2 * nx, 2);
    }
    this.uvs = new Float32Array(n * 2);
    for (var j3 = 0; j3 < ny; j3++) for (var i3 = 0; i3 < nx; i3++) { var k3 = j3 * nx + i3; this.uvs[k3 * 2] = i3 / (nx - 1); this.uvs[k3 * 2 + 1] = 1 - j3 / (ny - 1); }
    var idx = [];
    for (var j4 = 0; j4 < ny - 1; j4++) for (var i4 = 0; i4 < nx - 1; i4++) {
      var a = j4 * nx + i4, b = a + 1, c = a + nx, d = c + 1;
      idx.push(a, c, b, b, c, d);
    }
    this.index = new Uint32Array(idx);
    this.tangents = new Float32Array(n * 3);
    this.rest = null; this.bendStiff = 0.35;
  }
  Cloth.prototype.dist = function (a, b) {
    var p = this.pos, dx = p[a * 3] - p[b * 3], dy = p[a * 3 + 1] - p[b * 3 + 1], dz = p[a * 3 + 2] - p[b * 3 + 2];
    return Math.sqrt(dx * dx + dy * dy + dz * dz);
  };
  Cloth.prototype.transform = function (fn) {
    var n = this.nx * this.ny, v = new THREE.Vector3();
    for (var k = 0; k < n; k++) { v.set(this.pos[k * 3], this.pos[k * 3 + 1], this.pos[k * 3 + 2]); fn(v, k); this.pos[k * 3] = v.x; this.pos[k * 3 + 1] = v.y; this.pos[k * 3 + 2] = v.z; }
    this.prev.set(this.pos);
  };
  Cloth.prototype.pin = function (k, x, y, z) { this.pinned[k] = 1; this.pinPos[k * 3] = x; this.pinPos[k * 3 + 1] = y; this.pinPos[k * 3 + 2] = z; };
  Cloth.prototype.unpin = function (k) { this.pinned[k] = 0; };
  Cloth.prototype.step = function (dt, damping, iterations, collide) {
    var n = this.nx * this.ny, p = this.pos, q = this.prev, a = this.acc, dt2 = dt * dt;
    for (var k = 0; k < n; k++) {
      var i = k * 3;
      if (this.pinned[k]) { p[i] = this.pinPos[i]; p[i + 1] = this.pinPos[i + 1]; p[i + 2] = this.pinPos[i + 2]; q[i] = p[i]; q[i + 1] = p[i + 1]; q[i + 2] = p[i + 2]; continue; }
      var x = p[i], y = p[i + 1], z = p[i + 2];
      p[i] = x + (x - q[i]) * damping + a[i] * dt2;
      p[i + 1] = y + (y - q[i + 1]) * damping + a[i + 1] * dt2;
      p[i + 2] = z + (z - q[i + 2]) * damping + a[i + 2] * dt2;
      q[i] = x; q[i + 1] = y; q[i + 2] = z;
    }
    a.fill(0);
    var c = this.cons, m = c.length;
    for (var it = 0; it < iterations; it++) {
      for (var j = 0; j < m; j += 4) {
        var A = c[j], B = c[j + 1], rest = c[j + 2], type = c[j + 3];
        var ai = A * 3, bi = B * 3;
        var dx = p[bi] - p[ai], dy = p[bi + 1] - p[ai + 1], dz = p[bi + 2] - p[ai + 2];
        var d = Math.sqrt(dx * dx + dy * dy + dz * dz); if (d < 1e-6) continue;
        var stiff = type === 2 ? this.bendStiff : type === 1 ? 0.75 : 1.0;
        var diff = (d - rest) / d * 0.5 * stiff;
        var pa = this.pinned[A], pb = this.pinned[B];
        if (!pa && !pb) { p[ai] += dx * diff; p[ai + 1] += dy * diff; p[ai + 2] += dz * diff; p[bi] -= dx * diff; p[bi + 1] -= dy * diff; p[bi + 2] -= dz * diff; }
        else if (!pa) { p[ai] += dx * diff * 2; p[ai + 1] += dy * diff * 2; p[ai + 2] += dz * diff * 2; }
        else if (!pb) { p[bi] -= dx * diff * 2; p[bi + 1] -= dy * diff * 2; p[bi + 2] -= dz * diff * 2; }
      }
      if (collide) collide(p, n);
    }
  };
  Cloth.prototype.computeTangents = function () {
    var nx = this.nx, ny = this.ny, p = this.pos, t = this.tangents;
    for (var j = 0; j < ny; j++) for (var i = 0; i < nx; i++) {
      var k = j * nx + i, l = j * nx + Math.max(0, i - 1), r = j * nx + Math.min(nx - 1, i + 1);
      var dx = p[r * 3] - p[l * 3], dy = p[r * 3 + 1] - p[l * 3 + 1], dz = p[r * 3 + 2] - p[l * 3 + 2];
      var len = Math.sqrt(dx * dx + dy * dy + dz * dz) || 1;
      t[k * 3] = dx / len; t[k * 3 + 1] = dy / len; t[k * 3 + 2] = dz / len;
    }
  };

  function create(opts) {
    if (!window.THREE) return null;
    var canvas = opts.canvas, mode = opts.mode || 'hang';
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var renderer;
    try { renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true, powerPreference: 'high-performance' }); }
    catch (e) { return null; }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
    renderer.setClearColor(0x000000, 0);
    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(opts.fov || 30, 1, 0.1, 50);
    var camDist = opts.camDist || 4.2;
    camera.position.set(0, opts.camY || 0, camDist);

    var loader = new THREE.TextureLoader(), cache = {};
    function tex(id) {
      if (!cache[id]) { cache[id] = loader.load(opts.texPath + id + '.jpg'); cache[id].anisotropy = renderer.capabilities.getMaxAnisotropy(); }
      return cache[id];
    }
    var weave = makeWeaveNormalMap(512);
    var uniforms = {
      uFront: { value: tex(opts.front) }, uBack: { value: tex(opts.back) },
      uNextFront: { value: tex(opts.front) }, uNextBack: { value: tex(opts.back) }, uMix: { value: 0 },
      uWeave: { value: weave }, uWeaveRepeat: { value: opts.weaveRepeat || 18 }, uWeaveScale: { value: opts.weaveScale == null ? 0.35 : opts.weaveScale },
      uGloss: { value: opts.gloss == null ? 0.35 : opts.gloss }, uAniso: { value: opts.aniso == null ? 1.0 : opts.aniso },
      uTone: { value: opts.toneMap ? 1 : 0 }, uDiffBase: { value: opts.diffBase == null ? 0.58 : opts.diffBase }, uAnisoMix: { value: opts.anisoMix == null ? 0.55 : opts.anisoMix },
      uEnvStrength: { value: opts.envStrength == null ? 0.5 : opts.envStrength }, uTime: { value: 0 },
      uLight: { value: new THREE.Vector3().fromArray(opts.light || [0.5, 0.8, 1.0]).normalize() },
      uEnvTop: { value: new THREE.Color(opts.envTop || '#ffffff') }, uEnvBottom: { value: new THREE.Color(opts.envBottom || '#4a4655') },
      uEnvTint: { value: new THREE.Color(opts.envTint || '#ffffff') }, uSheen: { value: new THREE.Color(opts.sheen || '#F2B705') }
    };
    var material = new THREE.ShaderMaterial({ uniforms: uniforms, vertexShader: VERT, fragmentShader: FRAG, side: THREE.DoubleSide });

    var size = opts.size || 1.6, aspect = opts.aspect || 1;
    var res = opts.resolution || 34;
    var cloth = null, geo = null, mesh = null;
    var group = new THREE.Group(); scene.add(group);
    var extras = new THREE.Group(); scene.add(extras);
    var time = 0, flipT = 0, flipTarget = 0;

    // collision sphere for 'drape'
    var sphereR = opts.sphereRadius || 0.7, sphereC = new THREE.Vector3(0, opts.sphereY == null ? -0.25 : opts.sphereY, 0);
    if (mode === 'drape') {
      var sm = new THREE.MeshStandardMaterial({ color: new THREE.Color(opts.formColor || '#d9d5d0'), roughness: 0.95, metalness: 0 });
      var sph = new THREE.Mesh(new THREE.SphereGeometry(sphereR * 0.985, 64, 48), sm); sph.position.copy(sphereC); extras.add(sph);
      var stand = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.07, 1.6, 24), sm); stand.position.set(0, sphereC.y - sphereR - 0.8, 0); extras.add(stand);
      var base = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.45, 0.06, 48), sm); base.position.set(0, sphereC.y - sphereR - 1.6, 0); extras.add(base);
      var amb = new THREE.AmbientLight(0xffffff, 0.75); scene.add(amb);
      var dir = new THREE.DirectionalLight(0xffffff, 0.55); dir.position.set(2, 3, 3); scene.add(dir);
    }
    if (opts.groundShadow) {
      var shadow = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: makeShadowTexture(), transparent: true, depthWrite: false }));
      shadow.rotation.x = -Math.PI / 2; shadow.position.y = opts.groundY == null ? -1.35 : opts.groundY; shadow.scale.set(2.6, 1.4, 1); extras.add(shadow);
    }

    function buildCloth() {
      if (mesh) { group.remove(mesh); geo.dispose(); }
      var w = size, h = size * aspect;
      var nx = res, ny = Math.max(8, Math.round(res * aspect));
      cloth = new Cloth(nx, ny, w, h); cloth.bendStiff = mode === 'float' ? 0.7 : 0.35;
      geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.BufferAttribute(cloth.pos, 3));
      geo.setAttribute('uv', new THREE.BufferAttribute(cloth.uvs, 2));
      geo.setAttribute('tangent', new THREE.BufferAttribute(cloth.tangents, 3));
      geo.setIndex(new THREE.BufferAttribute(cloth.index, 1));
      geo.computeVertexNormals();
      mesh = new THREE.Mesh(geo, material); mesh.frustumCulled = false; group.add(mesh);
      poseCloth();
    }
    function poseCloth() {
      var w = size, h = size * aspect, nx = cloth.nx, ny = cloth.ny;
      if (mode === 'hang') {
        // two pins at top corners, slight sag, gentle curl in z
        cloth.transform(function (v) { v.z = Math.sin((v.x / w + 0.5) * Math.PI) * 0.12; v.y += 0.25; });
        cloth.pin(0, -w / 2 + 0.04, h / 2 + 0.25, 0); cloth.pin(nx - 1, w / 2 - 0.04, h / 2 + 0.25, 0);
        var mid = Math.floor(nx / 2); cloth.pin(mid, 0, h / 2 + 0.36, 0.05);
      } else if (mode === 'float') {
        cloth.transform(function (v) { var x = v.x, y = v.y; v.x = x * 0.92; v.y = y * 0.92 - 0.05; v.z = Math.sin(x * 3.0) * 0.12 + Math.cos(y * 2.2) * 0.1; });
        cloth.rest = new Float32Array(cloth.pos);
      } else if (mode === 'drape') {
        cloth.transform(function (v) { var x = v.x, y = v.y; var c = Math.cos(0.6), s = Math.sin(0.6); var rx = x * c - y * s, rz = x * s + y * c; v.x = rx; v.z = rz; v.y = sphereC.y + sphereR + 0.45 + Math.sin(rx * 2.0) * 0.03 + Math.cos(rz * 1.7) * 0.03; });
      }
    }
    buildCloth();

    // pointer interaction
    var raycaster = new THREE.Raycaster(), ndc = new THREE.Vector2(), grabbed = -1, grabDepth = 0, lastPointer = new THREE.Vector2(), pointerVel = new THREE.Vector2(), hovering = false;
    var dragRotate = false, rotY = opts.rotY || 0, rotTarget = rotY, lastX = 0;
    function setNdc(e) { var r = canvas.getBoundingClientRect(); ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -(((e.clientY - r.top) / r.height) * 2 - 1)); }
    function nearestVertex(hit) {
      var f = hit.face, p = cloth.pos, best = f.a, bd = Infinity; [f.a, f.b, f.c].forEach(function (k) {
        var d = hit.point.distanceTo(new THREE.Vector3(p[k * 3], p[k * 3 + 1], p[k * 3 + 2]).applyMatrix4(group.matrixWorld)); if (d < bd) { bd = d; best = k; }
      }); return best;
    }
    canvas.addEventListener('pointerdown', function (e) {
      setNdc(e); raycaster.setFromCamera(ndc, camera);
      var hit = raycaster.intersectObject(mesh)[0];
      if (hit) {
        grabbed = nearestVertex(hit); grabDepth = hit.distance;
        var lp = hit.point.clone(); group.worldToLocal(lp); cloth.pin(grabbed, lp.x, lp.y, lp.z);
        canvas.classList.add('grabbing');
      } else if (opts.rotate) { dragRotate = true; lastX = e.clientX; }
      canvas.setPointerCapture(e.pointerId);
    });
    canvas.addEventListener('pointermove', function (e) {
      setNdc(e); raycaster.setFromCamera(ndc, camera);
      pointerVel.set(ndc.x - lastPointer.x, ndc.y - lastPointer.y); lastPointer.copy(ndc); hovering = true;
      if (grabbed >= 0) {
        var pt = raycaster.ray.at(grabDepth, new THREE.Vector3()); group.worldToLocal(pt); cloth.pin(grabbed, pt.x, pt.y, pt.z);
      } else if (dragRotate) { rotTarget += (e.clientX - lastX) * 0.006; lastX = e.clientX; }
      else if (mode === 'float' || mode === 'hang') {
        // wind push near the ray
        var p = cloth.pos, n = cloth.nx * cloth.ny, a = cloth.acc, tmp = new THREE.Vector3();
        var strength = (mode === 'float' ? 60 : 30) * Math.min(1, pointerVel.length() * 12);
        if (strength > 0.01) for (var k = 0; k < n; k++) {
          tmp.set(p[k * 3], p[k * 3 + 1], p[k * 3 + 2]); group.localToWorld(tmp);
          var d = raycaster.ray.distanceToPoint(tmp);
          if (d < 0.45) { var f = (1 - d / 0.45) * strength; a[k * 3] += pointerVel.x * f * 40; a[k * 3 + 1] += pointerVel.y * f * 40; a[k * 3 + 2] += -f * 0.6; }
        }
      }
    });
    function release() { if (grabbed >= 0 && !isPermanentPin(grabbed)) cloth.unpin(grabbed); grabbed = -1; dragRotate = false; canvas.classList.remove('grabbing'); }
    window.addEventListener('pointerup', release); window.addEventListener('pointercancel', release);
    canvas.addEventListener('pointerleave', function () { hovering = false; });
    function isPermanentPin(k) { if (mode !== 'hang') return false; return k === 0 || k === cloth.nx - 1 || k === Math.floor(cloth.nx / 2); }

    function resize() {
      var w = canvas.clientWidth, h = canvas.clientHeight; if (!w || !h) return;
      renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
      var narrow = w < 820;
      camera.position.z = camDist * (narrow ? 1.35 : 1);
      group.position.x = narrow ? 0 : (opts.offsetX || 0);
      extras.position.x = group.position.x;
    }
    window.addEventListener('resize', resize); resize();

    var visible = true, paused = false;
    document.addEventListener('visibilitychange', function () { if (document.hidden) paused = true; else paused = !!pausedByApp; });
    var pausedByApp = false;
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }, { threshold: 0 }).observe(canvas);

    var scrollAmp = 0, mixTarget = 0, pending = null, last = performance.now();
    var gravity = mode === 'float' ? 0 : (opts.gravity == null ? -6.5 : opts.gravity);
    var windBase = new THREE.Vector3().fromArray(opts.wind || (mode === 'hang' ? [1.2, 0.1, 0.9] : [0, 0, 0]));
    var normals = null;

    function collideSphere(p, n) {
      var cx = sphereC.x, cy = sphereC.y, cz = sphereC.z, R = sphereR + 0.012, q = cloth.prev;
      for (var k = 0; k < n; k++) {
        var i = k * 3, dx = p[i] - cx, dy = p[i + 1] - cy, dz = p[i + 2] - cz, d = Math.sqrt(dx * dx + dy * dy + dz * dz);
        if (d < R) {
          var f = R / d; p[i] = cx + dx * f; p[i + 1] = cy + dy * f; p[i + 2] = cz + dz * f;
          // friction: bleed off tangential velocity
          q[i] = p[i] + (q[i] - p[i]) * 0.25; q[i + 1] = p[i + 1] + (q[i + 1] - p[i + 1]) * 0.25; q[i + 2] = p[i + 2] + (q[i + 2] - p[i + 2]) * 0.25;
        }
      }
    }

    function simulate(dt) {
      time += dt;
      var n = cloth.nx * cloth.ny, a = cloth.acc, p = cloth.pos;
      normals = geo.attributes.normal.array;
      var gust = 0.65 + 0.35 * Math.sin(time * 0.6) + 0.25 * Math.sin(time * 1.7 + 1.3);
      if (reduced) gust *= 0.3;
      for (var k = 0; k < n; k++) {
        var i = k * 3;
        a[i + 1] += gravity;
        if (mode === 'hang') {
          var wx = windBase.x * gust * (0.6 + 0.4 * Math.sin(p[i + 1] * 2.5 + time * 2.0)), wz = windBase.z * gust * (0.5 + 0.5 * Math.sin(p[i] * 3.0 - time * 1.4));
          var facing = Math.abs(normals[i] * wx + normals[i + 2] * wz) / (Math.hypot(wx, wz) || 1);
          a[i] += wx * (0.4 + 0.6 * facing) * 2.2; a[i + 2] += wz * (0.4 + 0.6 * facing) * 2.2;
        } else if (mode === 'float') {
          var x = p[i], y = p[i + 1], z = p[i + 2];
          var t = time * 0.5;
          var fx = Math.sin(y * 2.1 + t) * Math.cos(z * 1.7 - t * 0.7), fy = Math.sin(z * 2.3 - t * 1.1) * Math.cos(x * 1.9 + t * 0.6), fz = Math.sin(x * 2.0 + t * 0.8) * Math.cos(y * 2.4 - t);
          var amp = (reduced ? 0.3 : 0.9) * (1 + scrollAmp * 2.5);
          var r = cloth.rest, ks = 3.2;
          a[i] += fx * amp + (r[i] - x) * ks; a[i + 1] += fy * amp + (r[i + 1] - y) * ks; a[i + 2] += fz * amp + (r[i + 2] - z) * ks;
        }
      }
      var damping = mode === 'float' ? 0.965 : 0.985;
      cloth.step(dt, damping, mode === 'drape' ? 7 : 5, mode === 'drape' ? collideSphere : null);
      geo.computeVertexNormals();
    }
    function frame(now) {
      requestAnimationFrame(frame);
      var real = Math.min(0.1, (now - last) / 1000); last = now;
      if (!visible || paused) return;
      var dt = real;
      var steps = Math.max(1, Math.min(4, Math.round(real / 0.0167)));
      for (var st = 0; st < steps; st++) simulate(Math.min(0.02, real / steps));
      uniforms.uTime.value = time;
      geo.attributes.position.needsUpdate = true; geo.attributes.normal.needsUpdate = true; cloth.computeTangents(); geo.attributes.tangent.needsUpdate = true;

      rotY += (rotTarget - rotY) * 0.08;
      flipT += (flipTarget - flipT) * 0.06;
      var idle = reduced ? 0 : Math.sin(time * 0.3) * (opts.idleSway == null ? 0.12 : opts.idleSway);
      group.rotation.y = rotY + idle + flipT;
      extras.rotation.y = rotY + idle;
      group.rotation.x = (opts.tiltX || 0) + scrollAmp * (opts.scrollTilt == null ? 0.3 : opts.scrollTilt);
      extras.rotation.x = group.rotation.x;
      group.position.y = (opts.offsetY || 0) + scrollAmp * (opts.scrollLift == null ? 0.6 : opts.scrollLift);
      extras.position.y = group.position.y;

      if (uniforms.uMix.value < mixTarget) {
        uniforms.uMix.value = Math.min(1, uniforms.uMix.value + dt * 1.6);
        if (uniforms.uMix.value >= 1 && pending) { uniforms.uFront.value = pending.f; uniforms.uBack.value = pending.b; uniforms.uMix.value = 0; mixTarget = 0; pending = null; }
      }
      renderer.render(scene, camera);
    }
    requestAnimationFrame(frame);

    return {
      setTextures: function (front, back) {
        var f = tex(front), b = tex(back);
        if (pending) { uniforms.uFront.value = pending.f; uniforms.uBack.value = pending.b; }
        uniforms.uNextFront.value = f; uniforms.uNextBack.value = b; uniforms.uMix.value = 0; mixTarget = 1; pending = { f: f, b: b };
      },
      setScale: function (s) { size = (opts.size || 1.6) * s; buildCloth(); },
      setPaused: function (v) { pausedByApp = !!v; paused = !!v || document.hidden; },
      reset: function () { buildCloth(); },
      flip: function () { flipTarget += Math.PI; },
      setScroll: function (v) { scrollAmp = Math.max(0, Math.min(1, v)); },
      setWind: function (x, y, z) { windBase.set(x, y, z); },
      setLook: function (o) { if (o.gloss != null) uniforms.uGloss.value = o.gloss; if (o.aniso != null) uniforms.uAniso.value = o.aniso; if (o.weaveScale != null) uniforms.uWeaveScale.value = o.weaveScale; if (o.env != null) uniforms.uEnvStrength.value = o.env; },
      uniforms: uniforms
    };
  }

  // Ribbon (twilly) along an animated curve
  function createRibbon(opts) {
    if (!window.THREE) return null;
    var canvas = opts.canvas, renderer;
    try { renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true }); } catch (e) { return null; }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    var scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(30, 1, 0.1, 50); camera.position.set(0, 0, 6);
    var loader = new THREE.TextureLoader();
    var t = loader.load(opts.texPath + opts.texture + '.jpg'); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = renderer.capabilities.getMaxAnisotropy();
    var weave = makeWeaveNormalMap(256);
    var uniforms = {
      uFront: { value: t }, uBack: { value: t }, uNextFront: { value: t }, uNextBack: { value: t }, uMix: { value: 0 },
      uWeave: { value: weave }, uWeaveRepeat: { value: 8 }, uWeaveScale: { value: 0.3 }, uGloss: { value: 0.22 }, uAniso: { value: 0.9 }, uEnvStrength: { value: 0.22 }, uTime: { value: 0 }, uTone: { value: opts.toneMap ? 1 : 0 }, uDiffBase: { value: opts.diffBase == null ? 0.58 : opts.diffBase }, uAnisoMix: { value: opts.anisoMix == null ? 0.55 : opts.anisoMix },
      uLight: { value: new THREE.Vector3(0.4, 0.8, 1).normalize() }, uEnvTop: { value: new THREE.Color(opts.envTop || '#ffffff') }, uEnvBottom: { value: new THREE.Color(opts.envBottom || '#3a3646') },
      uEnvTint: { value: new THREE.Color('#ffffff') }, uSheen: { value: new THREE.Color(opts.sheen || '#F2B705') }
    };
    var material = new THREE.ShaderMaterial({ uniforms: uniforms, vertexShader: VERT, fragmentShader: FRAG, side: THREE.DoubleSide });
    var SEG = 260, W = opts.width || 0.34;
    var pos = new Float32Array((SEG + 1) * 2 * 3), uv = new Float32Array((SEG + 1) * 2 * 2), tan = new Float32Array((SEG + 1) * 2 * 3), idx = [];
    for (var i = 0; i < SEG; i++) { var a = i * 2; idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); }
    for (var i2 = 0; i2 <= SEG; i2++) { var u = i2 / SEG; uv[(i2 * 2) * 2] = u * (opts.repeat || 5); uv[(i2 * 2) * 2 + 1] = 0; uv[(i2 * 2 + 1) * 2] = u * (opts.repeat || 5); uv[(i2 * 2 + 1) * 2 + 1] = 1; }
    var geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3)); geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2)); geo.setAttribute('tangent', new THREE.BufferAttribute(tan, 3)); geo.setIndex(idx);
    var mesh = new THREE.Mesh(geo, material); mesh.frustumCulled = false; scene.add(mesh);
    var pts = [], N = 7; for (var k = 0; k < N; k++) pts.push(new THREE.Vector3());
    var curve = new THREE.CatmullRomCurve3(pts, false, 'centripetal', 0.5);
    var rPaused = false, time = 0, last = performance.now(), visible = true, mouse = new THREE.Vector2(0, 0), mouseT = new THREE.Vector2(0, 0);
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }, { threshold: 0 }).observe(canvas);
    canvas.addEventListener('pointermove', function (e) { var r = canvas.getBoundingClientRect(); mouseT.set(((e.clientX - r.left) / r.width) * 2 - 1, -(((e.clientY - r.top) / r.height) * 2 - 1)); });
    canvas.addEventListener('pointerleave', function () { mouseT.set(0, 0); });
    function resize() { var w = canvas.clientWidth, h = canvas.clientHeight; if (!w || !h) return; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); camera.position.z = (opts.camZ ? window.innerWidth : w) < 820 ? (opts.camZMobile || 8.5) : (opts.camZ || 6); }
    window.addEventListener('resize', resize); resize();
    var P = new THREE.Vector3(), T = new THREE.Vector3(), Nn = new THREE.Vector3(), B = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0);
    function frame(now) {
      requestAnimationFrame(frame); var dt = Math.min(0.033, (now - last) / 1000); last = now; if (!visible || rPaused || document.hidden) return;
      time += dt; mouse.lerp(mouseT, 0.05);
      for (var k = 0; k < N; k++) {
        var s = k / (N - 1), x = (s - 0.5) * (opts.length || 7.2);
        pts[k].set(x + Math.sin(time * 0.5 + k) * 0.15, Math.sin(s * 5.2 + time * 0.9) * 0.55 + Math.sin(s * 2.0 - time * 0.5) * 0.35 + mouse.y * 0.6 * Math.sin(s * Math.PI), Math.cos(s * 4.0 + time * 0.7) * 0.5 + mouse.x * 0.5 * Math.sin(s * Math.PI));
      }
      for (var i = 0; i <= SEG; i++) {
        var u = i / SEG; curve.getPoint(u, P); curve.getTangent(u, T).normalize();
        // twist along the ribbon
        var twist = u * Math.PI * 2.2 + time * 0.6;
        Nn.copy(up).cross(T).normalize(); if (Nn.lengthSq() < 1e-4) Nn.set(1, 0, 0); B.copy(T).cross(Nn).normalize();
        var cx = Math.cos(twist), sx = Math.sin(twist);
        var side = new THREE.Vector3().copy(Nn).multiplyScalar(cx).addScaledVector(B, sx).multiplyScalar(W / 2);
        var o = i * 2 * 3;
        pos[o] = P.x - side.x; pos[o + 1] = P.y - side.y; pos[o + 2] = P.z - side.z;
        pos[o + 3] = P.x + side.x; pos[o + 4] = P.y + side.y; pos[o + 5] = P.z + side.z;
        tan[o] = T.x; tan[o + 1] = T.y; tan[o + 2] = T.z; tan[o + 3] = T.x; tan[o + 4] = T.y; tan[o + 5] = T.z;
      }
      geo.attributes.position.needsUpdate = true; geo.attributes.tangent.needsUpdate = true; geo.computeVertexNormals();
      mesh.rotation.z = -0.12; uniforms.uTime.value = time;
      renderer.render(scene, camera);
    }
    requestAnimationFrame(frame);
    return { setPaused: function (v) { rPaused = !!v; }, setTexture: function (id) { var nt = loader.load(opts.texPath + id + '.jpg'); nt.wrapS = nt.wrapT = THREE.RepeatWrapping; uniforms.uFront.value = nt; uniforms.uBack.value = nt; uniforms.uNextFront.value = nt; uniforms.uNextBack.value = nt; } };
  }

  return { create: create, createRibbon: createRibbon };
})();
