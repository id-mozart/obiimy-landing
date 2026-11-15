#!/usr/bin/env python3
"""The sticky «Маркетинг» header of the manager pages on the editor service (15.11.2026, «хедер прилипающий с логотипом обийми и надпись
маркетинг, в меню — аудитория, знижки, клієнти, шопіфай»). `wrap(page, active)` puts the CSS before the page's first </style> and the
header right after <body>; the menu links carry ?key=… when the page was opened with the manager's key, so /discounts, /customers and
/sync stay reachable from /portrait and back. The logo is the repo file brand/logo-ink.svg, served by the editor as /brand/logo-ink.svg."""
NAV = [("portrait", "Аудиторія", "/portrait"), ("discounts", "Знижки", "/discounts"), ("customers", "Клієнти", "/customers"), ("sync", "Shopify", "/sync"),
       ("deck", "Презентація", "/"), ("creatives", "Креативи", "https://obiimy-landing-production.up.railway.app/creatives")]   # the corporate deck editor (this service’s root) and the creatives gallery on the landing service (15.11)
CSS = (".mk{position:sticky;top:0;z-index:50;background:linear-gradient(rgba(255,255,255,.55),rgba(255,255,255,.35));-webkit-backdrop-filter:blur(22px) saturate(1.7);backdrop-filter:blur(22px) saturate(1.7);border-bottom:1px solid rgba(20,17,16,.08);box-shadow:inset 0 1px 0 rgba(255,255,255,.75),0 10px 30px -14px rgba(20,17,16,.25)}@supports not (backdrop-filter:blur(1px)){.mk{background:rgba(247,243,236,.96)}}"
       ".mk .in{max-width:1200px;margin:0 auto;padding:0 20px;height:52px;display:flex;align-items:center;gap:16px}.mk img{height:19px;width:auto;display:block}"
       ".mk .t{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#6b645c;padding-left:14px;border-left:1px solid #e6e0d6;line-height:1}"
       ".mk nav{margin-left:auto;display:flex;gap:4px;overflow-x:auto;scrollbar-width:none}.mk nav::-webkit-scrollbar{display:none}.mk nav a{color:#141110;text-decoration:none;font-size:14px;padding:7px 12px;border-radius:999px;white-space:nowrap}.mk nav a:hover{background:rgba(255,255,255,.7)}.mk nav a.on{background:#141110;color:#fff}"
       "@media(max-width:700px){.mk .in{height:46px;gap:10px;padding:0 12px}.mk .t{display:none}.mk nav{gap:0}.mk nav a{padding:6px 8px;font-size:13px}.mk .in a[title]{flex:none}}")
JS = "(()=>{const k=new URLSearchParams(location.search).get('key');if(k)document.querySelectorAll('.mk nav a[href^=\"/\"]').forEach(a=>{a.href+=(a.href.includes('?')?'&':'?')+'key='+encodeURIComponent(k);});})();"

def header(active):
    links = "".join('<a href="%s"%s>%s</a>' % (href, ' class="on"' if key == active else "", title) for key, title, href in NAV)   # external links (https://…) get no key
    return (f'<header class="mk"><div class="in"><a href="/portrait" title="OBIIMY"><img src="/brand/logo-ink.svg" alt="OBIIMY"></a><span class="t">Маркетинг</span><nav>{links}</nav></div></header>'
            f"<script>{JS}</script>")

def wrap(page, active):
    """The page with the header: CSS before the first </style>, the header right after <body>."""
    page = page.replace("</style>", CSS + "\n</style>", 1)
    i = page.index("<body>") + len("<body>")
    return page[:i] + header(active) + page[i:]
