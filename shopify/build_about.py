"""The «About us» page of shop.obiimy.world (Shopify, Dawn): one self-contained HTML block for the page body — a hero
photograph to the full page width, the story in short paragraphs, four facts, how a scarf is made, the SOLO prints,
the showroom and contacts. Pictures are real brand photographs uploaded to the store's Files (see upload_about.py);
until then the preview uses local paths. Facts: review/SITE-FACTS.md and the client's own About text (English, as on the
store today). Output: shopify/about-us.html (page body) and shopify/about-preview.html (a standalone preview in Dawn's look).
Usage: python3 shopify/build_about.py [--cdn urls.json]"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = pathlib.Path(__file__).resolve().parent

# pictures: key -> (local file, alt); the CDN map replaces the src after upload
PICS = {
    "hero": ("ads/solo/ref/new/F44A3254_reblum.jpg", "Silk scarf «Avantiura» from the SOLO collection"),
    "founder": ("photo/solo/tysha-88-2.webp", "Silk scarf «Tysha» worn on the shoulders"),
    "print": ("ads/solo/src/avantiura-88-1-hi.webp", "The «Avantiura» print on silk"),
    "edge": ("photo/site/khustka-vidnovlennia-88x88-02.jpg", "Hand-finished edge of a silk scarf"),
    "box": ("photo/site/set-tvilli-845-ta-khustky-4444-dvost-13-01.jpg", "Obiimy gift box with a scarf and a twilly"),
    "look1": ("photo/solo/iskra-65-4.webp", "«Iskra» scarf, autumn street"),
    "look2": ("photo/solo/flirt-tw-1.webp", "«Flirt» twilly in the hair"),
    "look3": ("photo/solo/zolote-44-2.webp", "«Zolote svitlo» scarf"),
    "look4": ("photo/solo/krok-tw-2.webp", "«Smilyvyi krok» twilly"),
    "mask": ("photo/site/mask-vpevnenist-04.jpg", "Silk sleep mask «Vpevnenist»"),
    "svit": ("shopify/svitlana/p4-5.jpeg", "Svitlana Snizhko, founder and artist of Obiimy"),
    "svit2": ("shopify/svitlana/p1-1.jpeg", "Svitlana Snizhko"),
    "song": ("shopify/svitlana/p3-4.jpeg", "Silk scarf from the «Singing Soul» collection"),
    "knot": ("ads/solo/ref/new/F44A3254_reblum.jpg", "The knot of a silk scarf"),
    "yacht": ("photo/solo/avantiura-88-3.webp", "«Avantiura» scarf"),
}
cdn = {}
if "--cdn" in sys.argv:
    cdn = json.loads(pathlib.Path(sys.argv[sys.argv.index("--cdn") + 1]).read_text())

def src(key):
    return cdn.get(key) or ("../" + PICS[key][0])

def img(key, style="", cls=""):
    f, alt = PICS[key]
    return f'<img src="{src(key)}" alt="{alt}" loading="lazy" class="{cls}" style="{style}">'

# Dawn's own variables are used where they exist; everything else is scoped under .ob-about so the theme stays untouched
CSS = """
<style>
.ob-about { --ink:#1b1613; --ink2:#5a5048; --line:rgba(27,22,19,.14); --yellow:#F2B705; --paper:#F6F1E8; color:var(--ink); font-family: var(--font-body-family, Assistant, sans-serif); line-height:1.6; }
.ob-about * { box-sizing:border-box; }
.ob-about h2, .ob-about h3 { font-family: var(--font-heading-family, Assistant, sans-serif); font-weight:400; margin:0; line-height:1.15; letter-spacing:-.01em; }
.ob-about h2 { font-size: clamp(2.6rem, 3.2vw, 3.6rem); }
.ob-about h3 { font-size: 2rem; }
.ob-about p { margin:0; font-size:1.6rem; }
.ob-about .k { font-size:1.2rem; letter-spacing:.2em; text-transform:uppercase; color:var(--ink2); margin-bottom:1.6rem; }
.ob-hero { position:relative; height: clamp(360px, 52vw, 640px); overflow:hidden; background:#141110; }
.ob-hero img { width:100%; height:100%; object-fit:cover; object-position:50% 38%; display:block; }
.ob-hero .t { position:absolute; left:0; right:0; bottom:0; padding: 4rem max(5vw, calc((100% - 120rem) / 2)) 4.4rem; color:#fff; background:linear-gradient(180deg, rgba(0,0,0,0), rgba(0,0,0,.62)); }
.ob-hero h1 { font-family: var(--font-heading-family, Assistant, sans-serif); font-weight:400; font-size: clamp(3.4rem, 5.4vw, 6.4rem); line-height:1; margin:0 0 1rem; letter-spacing:-.01em; }
.ob-hero p { max-width:62rem; font-size:1.8rem; color:rgba(255,255,255,.92); }
.ob-sec { padding: 6.4rem 5vw; } .ob-sec > * { max-width: 120rem; margin-left:auto; margin-right:auto; }
.ob-sec.paper { background:var(--paper); }
.ob-two { display:grid; grid-template-columns: 1fr 1fr; gap: 5rem; align-items:center; }
.ob-two .ph { aspect-ratio: 4/5; overflow:hidden; } .ob-two .ph img { width:100%; height:100%; object-fit:cover; display:block; }
.ob-lead { font-size: clamp(2rem, 2.4vw, 2.6rem); line-height:1.35; max-width:70rem; }
.ob-txt p + p { margin-top:1.4rem; }
.ob-facts { display:grid; grid-template-columns: repeat(4, 1fr); gap:3rem; margin-top:4rem; }
.ob-facts div { border-top:1px solid var(--ink); padding-top:1.6rem; }
.ob-facts b { display:block; font-family: var(--font-heading-family, Assistant, sans-serif); font-weight:400; font-size:2.4rem; margin-bottom:.6rem; }
.ob-facts p { font-size:1.45rem; color:var(--ink2); }
.ob-steps { display:grid; grid-template-columns: repeat(3, 1fr); gap:3rem; margin-top:3.6rem; }
.ob-steps .ph { aspect-ratio: 1; overflow:hidden; margin-bottom:1.8rem; } .ob-steps .ph img { width:100%; height:100%; object-fit:cover; display:block; }
.ob-steps h3 { margin-bottom:.8rem; } .ob-steps p { color:var(--ink2); font-size:1.5rem; }
.ob-looks { display:grid; grid-template-columns: repeat(4, 1fr); gap:1.2rem; margin-top:3.6rem; }
.ob-looks .ph { aspect-ratio: 3/4; overflow:hidden; } .ob-looks .ph img { width:100%; height:100%; object-fit:cover; display:block; }
.ob-quote { font-family: var(--font-heading-family, Assistant, sans-serif); font-size: clamp(2.2rem, 3vw, 3.4rem); line-height:1.25; max-width:80rem; margin: 0 auto; text-align:center; }
.ob-quote small { display:block; margin-top:2rem; font-size:1.3rem; letter-spacing:.18em; text-transform:uppercase; color:var(--ink2); font-family: var(--font-body-family, Assistant, sans-serif); }
.ob-contact { display:grid; grid-template-columns: 1.2fr 1fr; gap:5rem; align-items:center; }
.ob-contact .ph { aspect-ratio: 5/4; overflow:hidden; } .ob-contact .ph img { width:100%; height:100%; object-fit:cover; display:block; }
.ob-kv { display:grid; grid-template-columns: 14rem 1fr; gap:1.2rem 2rem; font-size:1.6rem; margin-top:2.4rem; }
.ob-kv span:first-child { color:var(--ink2); }
.ob-about a { color:inherit; text-decoration:underline; text-underline-offset:.2em; }
.ob-btn { display:inline-block; margin-top:2.8rem; padding:1.4rem 2.8rem; background:var(--ink); color:#fff !important; text-decoration:none !important; font-size:1.5rem; letter-spacing:.04em; border-radius:999px; }
.ob-btn.y { background:var(--yellow); color:var(--ink) !important; }
.ob-founder { display:grid; grid-template-columns: 1fr 1.25fr; gap:5rem; align-items:center; }
.ob-founder .ph { aspect-ratio: 3/4; overflow:hidden; } .ob-founder .ph img { width:100%; height:100%; object-fit:cover; object-position:50% 20%; display:block; }
.ob-founder h2 { margin-bottom:.6rem; } .ob-founder .role { font-size:1.4rem; letter-spacing:.16em; text-transform:uppercase; color:var(--ink2); margin-bottom:2.4rem; }
.ob-founder ul { margin:2.4rem 0 0; padding:0; list-style:none; display:grid; gap:1rem; } .ob-founder li { position:relative; padding-left:2.2rem; font-size:1.5rem; color:var(--ink2); } .ob-founder li::before { content:""; position:absolute; left:0; top:1rem; width:1.2rem; height:2px; background:var(--yellow); }
.ob-nums { display:grid; grid-template-columns: repeat(3, 1fr); gap:3rem; margin-top:3.2rem; } .ob-nums b { display:block; font-family: var(--font-heading-family, Assistant, sans-serif); font-weight:400; font-size:3.6rem; line-height:1; } .ob-nums p { font-size:1.4rem; color:var(--ink2); margin-top:.6rem; }
.ob-hero.tall { height: clamp(420px, 60vw, 760px); } .ob-hero.tall img { object-position:50% 30%; }
.ob-hero .t.center { text-align:center; padding-bottom:6rem; } .ob-hero .t.center p { margin:0 auto; }
.ob-letter { max-width:76rem; margin:0 auto; font-size:1.8rem; line-height:1.7; } .ob-letter p + p { margin-top:1.8rem; } .ob-letter .sig { margin-top:3rem; font-family: var(--font-heading-family, Assistant, sans-serif); font-size:2.4rem; }
.ob-marq { display:flex; gap:4rem; overflow:hidden; white-space:nowrap; font-family: var(--font-heading-family, Assistant, sans-serif); font-size: clamp(3rem, 5vw, 6rem); color:var(--ink2); opacity:.35; padding:2rem 0; }
.ob-band { display:grid; grid-template-columns: repeat(3, 1fr); gap:1.2rem; } .ob-band .ph { aspect-ratio: 4/5; overflow:hidden; } .ob-band .ph img { width:100%; height:100%; object-fit:cover; display:block; }
@media (max-width: 749px) { .ob-founder { grid-template-columns:1fr; gap:2.4rem; } .ob-nums { grid-template-columns:1fr 1fr 1fr; gap:1.4rem; } .ob-nums b { font-size:2.8rem; } .ob-band { grid-template-columns:1fr; } }
@media (max-width: 749px) { .ob-two, .ob-contact { grid-template-columns:1fr; gap:2.6rem; } .ob-facts { grid-template-columns:1fr 1fr; gap:2rem; } .ob-steps { grid-template-columns:1fr; } .ob-looks { grid-template-columns:1fr 1fr; } .ob-sec { padding:4rem 5vw; } .ob-kv { grid-template-columns:1fr; gap:.4rem 0; } }
</style>
"""

FOUNDER = f"""
  <section class="ob-sec paper">
    <div class="ob-founder">
      <div class="ph">{img("svit")}</div>
      <div>
        <p class="k">The founder</p>
        <h2>Svitlana Snizhko</h2>
        <p class="role">Entrepreneur, philanthropist, artist</p>
        <p>Every Obiimy print begins as one of Svitlana's paintings — her artworks became the basis of the brand's first collections. With over 15 years in business, she built Obiimy from scratch into a brand with a Ukrainian identity that is sold internationally, and she develops it as a cultural product that carries that identity into the world.</p>
        <ul>
          <li>Patron of the Olos Foundation since 2019; named «Philanthropist of the Year 2024»</li>
          <li>Supports the restoration of the Trypillia culture museum in Lehedzyne and of the mosaics of Saint Sophia Cathedral in Kyiv</li>
          <li>Supports Superhumans Center and Repower NGO, and pays for music education of talented Ukrainian children</li>
          <li>Started the «Singing Soul» project: part of the profit from the collection goes to saving the European roller, a Red Book bird, in Rivne region</li>
        </ul>
      </div>
    </div>
  </section>
"""

BODY = f"""{CSS}
<div class="ob-about">
  <div class="ob-hero">{img("hero")}
    <div class="t"><h1>Silk hugs, made in Ukraine</h1><p>Obiimy means «hugs» in Ukrainian. We make silk scarves, twillies and accessories with original prints by our founder, artist Svitlana Snizhko — and ship them from Kyiv to the world.</p></div>
  </div>

  <section class="ob-sec">
    <div class="ob-two">
      <div class="ph">{img("founder")}</div>
      <div class="ob-txt">
        <p class="k">Who we are</p>
        <p class="ob-lead">Obiimy is an independent Ukrainian brand of natural silk products with original prints by artist and founder Svitlana Snizhko.</p>
        <p style="margin-top:2rem">We create things that combine beauty, art and care — and give emotions from the first touch. Obiimy is about love for yourself, nature and people. Each box is a hug that reminds you that you are worthy of beauty.</p>
        <p>Our brand is not only about beauty, but also about health. Silk is soft and gentle to the skin and does not cause irritation or allergic reactions — that is why it makes the best sleep masks, among other things.</p>
      </div>
    </div>
    <div class="ob-facts">
      <div><b>100% silk</b><p>Premium natural silk with a delicate shine and soft texture. Scarves are printed on both sides.</p></div>
      <div><b>Original prints</b><p>Every print starts as a painting by Svitlana Snizhko. No stock patterns, no licensed designs.</p></div>
      <div><b>Finished by hand</b><p>Seamstresses finish the corners of every scarf by hand, so the edge is even all the way round. Made in Ukraine.</p></div>
      <div><b>Founded in wartime</b><p>Obiimy was born during the war and takes part in charitable initiatives for the military and those affected.</p></div>
    </div>
  </section>

  <section class="ob-sec paper">
    <p class="k">How a scarf is made</p>
    <h2>From a painting to your silk</h2>
    <div class="ob-steps">
      <div><div class="ph">{img("print")}</div><h3>1 · The print</h3><p>Svitlana paints the artwork; it becomes a print with its own name and story — like «Avantiura», «Tysha» or «Iskra».</p></div>
      <div><div class="ph">{img("edge")}</div><h3>2 · Silk and hand finishing</h3><p>The print goes onto 100% Italian silk. Seamstresses work on the corners of every scarf by hand, so the density along the edge is the same everywhere.</p></div>
      <div><div class="ph">{img("box")}</div><h3>3 · The yellow box</h3><p>Each piece comes in Obiimy's gift packaging — ready to give, or to keep for yourself.</p></div>
    </div>
  </section>

  <section class="ob-sec">
    <p class="k">What we make</p>
    <h2>Silk scarves, twillies and more</h2>
    <p style="margin-top:1.6rem;max-width:70rem">Scarves in three sizes (44, 65 and 88 cm), narrow twillies for the hair, neck or bag, silk scrunchies and sleep masks, home and care accessories, and jewellery for scarves. Collections like <a href="/collections/all">SOLO — the path to yourself</a> bring seven prints, seven states of a woman on her way to herself.</p>
    <div class="ob-looks"><div class="ph">{img("look1")}</div><div class="ph">{img("look2")}</div><div class="ph">{img("look3")}</div><div class="ph">{img("look4")}</div></div>
    <a class="ob-btn y" href="/collections/all">Shop the collection</a>
  </section>

{FOUNDER}
  <section class="ob-sec paper">
    <p class="ob-quote">«Obiimy is a combination of fragility, style, originality and extreme tenderness. We create not just accessories, but a way to express your own individuality and feelings. You deserve the best.»<small>Svitlana Snizhko, founder and artist</small></p>
  </section>

  <section class="ob-sec">
    <div class="ob-contact">
      <div class="ph">{img("mask")}</div>
      <div>
        <p class="k">Where to find us</p>
        <h2>Kyiv showroom and worldwide shipping</h2>
        <p style="margin-top:1.6rem">We sell directly: worldwide through this store, in Ukraine through <a href="https://obiimy.world">obiimy.world</a> and our showroom in Kyiv, and through partner stores. We also make corporate gift sets for companies.</p>
        <div class="ob-kv">
          <span>Showroom</span><span>12 Petra Sahaidachnoho St., Kyiv · Mon–Fri 10:00–18:00, Sat 11:00–18:00</span>
          <span>Shipping</span><span>From Kyiv by FedEx — see <a href="/policies/shipping-policy">Shipping policy</a> and <a href="/policies/refund-policy">Refund policy</a></span>
          <span>Email</span><span><a href="mailto:sale@obiimy.world">sale@obiimy.world</a></span>
          <span>Phone</span><span><a href="tel:+380670108525">+38 067 010 85 25</a></span>
          <span>Responsible person</span><span>Svitlana Snizhko — founder and artist of Obiimy</span>
        </div>
        <a class="ob-btn" href="/pages/contact">Contact us</a>
      </div>
    </div>
  </section>
</div>
"""

(HERE / "about-us.html").write_text(BODY)

# B · editorial: tall hero with the founder's words, numbers, the founder with a big portrait, a photo band, the craft, contacts
BODY_B = f"""{CSS}
<div class="ob-about">
  <div class="ob-hero tall">{img("hero")}
    <div class="t center"><h1>Silk hugs from Ukraine</h1><p>Scarves, twillies and accessories in 100% natural silk, with prints painted by our founder. Shipped from Kyiv to the world.</p></div>
  </div>
  <section class="ob-sec">
    <div class="ob-two">
      <div class="ob-txt">
        <p class="k">Who we are</p>
        <p class="ob-lead">Obiimy means «hugs». We are an independent Ukrainian brand of natural silk products with original prints by artist and founder Svitlana Snizhko.</p>
        <p style="margin-top:2rem">We create things that combine beauty, art and care — and give emotions from the first touch. Each box is a hug that reminds you that you are worthy of beauty. Obiimy was founded during the war and takes part in charitable initiatives for the military and those affected.</p>
        <div class="ob-nums"><div><b>100%</b><p>natural premium silk, printed on both sides</p></div><div><b>7</b><p>prints in the SOLO collection — seven states of a woman</p></div><div><b>Kyiv</b><p>showroom and studio; worldwide shipping by FedEx</p></div></div>
      </div>
      <div class="ph">{img("song")}</div>
    </div>
  </section>
  <section class="ob-sec paper">
    <div class="ob-founder" style="grid-template-columns: 1.1fr 1fr">
      <div>
        <p class="k">The founder</p>
        <h2>Svitlana Snizhko</h2>
        <p class="role">Entrepreneur, philanthropist, artist</p>
        <p class="ob-lead" style="font-size:2rem">«My paintings became the first Obiimy collections. I wanted silk to carry Ukrainian identity into the world — and to give back.»</p>
        <p style="margin-top:1.6rem">Over 15 years in business; co-founder of one of the largest retail projects in its niche; built Obiimy from scratch into an international brand. Patron of the Olos Foundation since 2019 and «Philanthropist of the Year 2024»: the Trypillia museum in Lehedzyne, the mosaics of Saint Sophia in Kyiv, scholarships for researchers of Trypillia heritage, music education for talented children, Superhumans Center and Repower NGO. Her «Singing Soul» project saves the European roller, a Red Book bird, with part of the profit from the collection of the same name.</p>
      </div>
      <div class="ph" style="aspect-ratio:4/5">{img("svit")}</div>
    </div>
  </section>
  <section class="ob-sec" style="padding-top:0;padding-bottom:0"><div class="ob-band"><div class="ph">{img("look1")}</div><div class="ph">{img("knot")}</div><div class="ph">{img("look3")}</div></div></section>
  <section class="ob-sec">
    <p class="k">How a scarf is made</p>
    <h2>From a painting to your silk</h2>
    <div class="ob-steps">
      <div><div class="ph">{img("print")}</div><h3>1 · The print</h3><p>Svitlana paints the artwork; it becomes a print with its own name and story — «Avantiura», «Tysha», «Iskra».</p></div>
      <div><div class="ph">{img("edge")}</div><h3>2 · Silk and hand finishing</h3><p>The print goes onto 100% Italian silk. Seamstresses work on the corners of every scarf by hand, so the density along the edge is the same everywhere.</p></div>
      <div><div class="ph">{img("box")}</div><h3>3 · The yellow box</h3><p>Each piece comes in Obiimy's gift packaging — ready to give, or to keep for yourself.</p></div>
    </div>
    <a class="ob-btn y" href="/collections/all">Shop the collection</a>
  </section>
  <section class="ob-sec paper">
    <div class="ob-contact">
      <div class="ph">{img("mask")}</div>
      <div>
        <p class="k">Where to find us</p>
        <h2>Kyiv showroom and worldwide shipping</h2>
        <p style="margin-top:1.6rem">We sell directly: worldwide through this store, in Ukraine through <a href="https://obiimy.world">obiimy.world</a> and our showroom in Kyiv, and through partner stores. We also make corporate gift sets for companies.</p>
        <div class="ob-kv">
          <span>Showroom</span><span>12 Petra Sahaidachnoho St., Kyiv · Mon–Fri 10:00–18:00, Sat 11:00–18:00</span>
          <span>Shipping</span><span>From Kyiv by FedEx — see <a href="/policies/shipping-policy">Shipping policy</a> and <a href="/policies/refund-policy">Refund policy</a></span>
          <span>Email</span><span><a href="mailto:sale@obiimy.world">sale@obiimy.world</a></span>
          <span>Phone</span><span><a href="tel:+380670108525">+38 067 010 85 25</a></span>
          <span>Responsible person</span><span>Svitlana Snizhko — founder and artist of Obiimy</span>
        </div>
        <a class="ob-btn" href="/pages/contact">Contact us</a>
      </div>
    </div>
  </section>
</div>
"""
(HERE / "about-us-b.html").write_text(BODY_B)

# C · a letter from the founder: her portrait wide, the story in the first person, then the facts and contacts
BODY_C = f"""{CSS}
<div class="ob-about">
  <section class="ob-sec" style="padding-top:2rem">
    <div class="ob-two" style="align-items:start">
      <div class="ph" style="aspect-ratio:3/4">{img("svit", "object-position:50% 15%")}</div>
      <div class="ob-letter" style="margin:0;max-width:none">
        <p class="k">A letter from the founder</p>
        <h2 style="margin-bottom:2.4rem">Dear friend,</h2>
      <p>Obiimy means «hugs» in Ukrainian. I started the brand with my own paintings: the first collections were printed from them, and every print since has its own name and its own state — «Iskra», «Tysha», «Avantiura». I wanted a scarf to be more than an accessory: a small act of freedom, a reminder that you are worthy of beauty.</p>
      <p>We work only with 100% natural premium silk. The print goes onto Italian silk and every scarf is finished in Ukraine — our seamstresses work on the corners by hand so the edge is even all the way round. Each piece comes in a yellow box, ready to give to someone — or to yourself.</p>
      <p>Obiimy was founded during the war. From the first day the brand has taken part in charitable initiatives for the military and for those affected, and part of the profit from our «Singing Soul» collection goes to saving the European roller, a rare bird in Rivne region. Buying Obiimy, you become part of this — and I am grateful to you for that.</p>
      <p class="sig">Svitlana Snizhko</p><p class="role" style="font-size:1.3rem;letter-spacing:.16em;text-transform:uppercase;color:var(--ink2);margin-top:.6rem">Founder and artist of Obiimy</p>
      </div>
    </div>
  </section>
  <section class="ob-sec paper">
    <div class="ob-founder">
      <div class="ph">{img("song", "object-position:50% 30%")}</div>
      <div>
        <p class="k">Beyond the brand</p>
        <h2>Entrepreneur and philanthropist</h2>
        <p style="margin-top:1.2rem">Over 15 years in business and co-founder of one of the largest retail projects in its niche, Svitlana built Obiimy from scratch into an international brand and develops it as a cultural product that carries Ukrainian identity into the world.</p>
        <ul>
          <li>Patron of the Olos Foundation since 2019; «Philanthropist of the Year 2024»</li>
          <li>Restoration of the Trypillia culture museum in Lehedzyne and of the mosaics of Saint Sophia Cathedral; scholarships for researchers of Trypillia heritage</li>
          <li>Books on the Ukrainian language, history and notable figures; the monument to Ivan Mazepa</li>
          <li>Superhumans Center, Repower NGO, music education for talented Ukrainian children</li>
        </ul>
      </div>
    </div>
  </section>
  <section class="ob-sec">
    <p class="k">What we make</p>
    <h2>Silk scarves, twillies and more</h2>
    <p style="margin-top:1.6rem;max-width:70rem">Scarves in three sizes (44, 65 and 88 cm), narrow twillies for the hair, neck or bag, silk scrunchies and sleep masks, home and care accessories, and jewellery for scarves.</p>
    <div class="ob-looks"><div class="ph">{img("yacht")}</div><div class="ph">{img("look2")}</div><div class="ph">{img("song")}</div><div class="ph">{img("look4")}</div></div>
    <a class="ob-btn y" href="/collections/all">Shop the collection</a>
  </section>
  <section class="ob-sec paper">
    <div class="ob-contact">
      <div class="ph">{img("box")}</div>
      <div>
        <p class="k">Where to find us</p>
        <h2>Kyiv showroom and worldwide shipping</h2>
        <div class="ob-kv">
          <span>Showroom</span><span>12 Petra Sahaidachnoho St., Kyiv · Mon–Fri 10:00–18:00, Sat 11:00–18:00</span>
          <span>Shipping</span><span>From Kyiv by FedEx — see <a href="/policies/shipping-policy">Shipping policy</a> and <a href="/policies/refund-policy">Refund policy</a></span>
          <span>Email</span><span><a href="mailto:sale@obiimy.world">sale@obiimy.world</a></span>
          <span>Phone</span><span><a href="tel:+380670108525">+38 067 010 85 25</a></span>
          <span>In Ukraine</span><span><a href="https://obiimy.world">obiimy.world</a> and partner stores; corporate gift sets for companies</span>
        </div>
        <a class="ob-btn" href="/pages/contact">Contact us</a>
      </div>
    </div>
  </section>
</div>
"""
(HERE / "about-us-c.html").write_text(BODY_C)
PREVIEW = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>About Us — Obiimy (preview)</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600&display=swap">
<style>html {{ font-size: 62.5%; }} body {{ margin:0; font-family: Assistant, sans-serif; color:#121212; background:#fff; }}
.hd {{ display:flex; justify-content:center; align-items:center; gap:4rem; padding:2.4rem 5vw; border-bottom:1px solid rgba(0,0,0,.08); font-size:1.5rem; }} .hd img {{ height:3.6rem; }} .hd span {{ color:#555; }}
.sw {{ position:sticky; top:0; z-index:9; background:#fff; border-bottom:1px solid rgba(0,0,0,.1); display:flex; gap:.8rem; justify-content:center; padding:1.2rem; font-size:1.4rem; }} .sw button {{ font:inherit; border:1px solid #ccc; background:#fff; border-radius:999px; padding:.8rem 1.6rem; cursor:pointer; }} .sw button[aria-pressed=true] {{ background:#121212; color:#fff; border-color:#121212; }}
.v {{ display:none; }} .v.on {{ display:block; }}
.ttl {{ text-align:center; font-size:4rem; font-weight:400; margin:4rem 0 2rem; }}
.ft {{ padding:4rem 5vw; border-top:1px solid rgba(0,0,0,.08); font-size:1.3rem; color:#777; text-align:center; margin-top:4rem; }}</style></head><body>
<div class="hd"><img src="../brand/logo-original.png" alt="Obiimy"><span>Home</span><span>Catalog</span><span>About Us</span><span>Contact</span></div>
<div class="sw"><b style="align-self:center;margin-right:1rem">Variant:</b><button type="button" data-v="a" aria-pressed="true">A · Story + founder</button><button type="button" data-v="b" aria-pressed="false">B · Editorial</button><button type="button" data-v="c" aria-pressed="false">C · A letter from Svitlana</button></div>
<h1 class="ttl">About Us</h1>
<div class="v on" id="v-a">{BODY}</div><div class="v" id="v-b">{BODY_B}</div><div class="v" id="v-c">{BODY_C}</div>
<div class="ft">© Obiimy · preview of the new About page for shop.obiimy.world</div>
<script>document.querySelectorAll('.sw button').forEach(function (b) {{ b.addEventListener('click', function () {{ document.querySelectorAll('.sw button').forEach(function (x) {{ x.setAttribute('aria-pressed', x === b); }}); document.querySelectorAll('.v').forEach(function (v) {{ v.classList.toggle('on', v.id === 'v-' + b.dataset.v); }}); history.replaceState(null, '', '?v=' + b.dataset.v); window.scrollTo(0, 0); }}); }}); var q = new URLSearchParams(location.search).get('v'); if (q) document.querySelector('.sw [data-v=' + q + ']').click();</script>
</body></html>"""
(HERE / "about-preview.html").write_text(PREVIEW)
print("about-us.html", len(BODY) // 1024, "KB; B", len(BODY_B) // 1024, "KB; C", len(BODY_C) // 1024, "KB; preview written")
