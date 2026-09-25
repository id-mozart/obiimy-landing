#!/usr/bin/env python3
"""Inline the silk engine and the shared STATES data into each version page."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent
ENGINE = (ROOT / "silk-engine.js").read_text()

STATES = [
    {"id": "probudzhennia", "name": "Пробудження", "line": "Іриси, написані навесні. Про емоції, що ростуть зсередини у перші хвилини чогось нового.", "size": "65 × 65 см · двосторонній друк", "price": "4 320 грн", "old": "4 800 грн", "url": "https://obiimy.world/shovkova-khustka-probudzhennia-65x65/", "back": "litnie-pole"},
    {"id": "yednannia", "name": "Єднання", "line": "Жовті пташки на кульбабах. Про те, що тримає разом, коли розлітається все інше.", "size": "44 × 44 см · двосторонній друк", "price": "2 400 грн", "old": "", "url": "https://obiimy.world/spivocha-dusha/", "back": "pidnesennia"},
    {"id": "tysha-sertsia", "name": "Тиша серця", "line": "Горобці у високій траві. Про спокій, який не треба заслуговувати.", "size": "65 × 65 см", "price": "3 200 грн", "old": "", "url": "https://obiimy.world/spivocha-dusha/", "back": "melodiia"},
    {"id": "prystrast", "name": "Пристрасть", "line": "Сині кульбаби на кремовому шовку. Про те, що розлітається від одного подиху.", "size": "65 × 65 см · двосторонній друк", "price": "4 320 грн", "old": "4 800 грн", "url": "https://obiimy.world/dvostoronnii-druk/", "back": "mizh-namy"},
    {"id": "kolo-sontsia", "name": "Коло сонця", "line": "Вінок із сонячних квітів на рожевому. Про тепло, яке щоразу повертається.", "size": "88 × 88 см · шаль", "price": "4 400 грн", "old": "", "url": "https://obiimy.world/spivocha-dusha/", "back": "litnie-pole"},
    {"id": "melodiia", "name": "Мелодія двох", "line": "Дві пташки серед верболозу. Про розмову, для якої не потрібні слова.", "size": "44 × 44 см · паше", "price": "1 600 грн", "old": "", "url": "https://obiimy.world/spivocha-dusha/", "back": "yednannia"},
    {"id": "pidnesennia", "name": "Піднесення", "line": "Сиворакші та золотий дощ. Про політ, який починається на землі.", "size": "65 × 65 см · двосторонній друк", "price": "4 320 грн", "old": "4 800 грн", "url": "https://obiimy.world/spivocha-dusha/", "back": "kolo-sontsia"},
    {"id": "mizh-namy", "name": "Між нами", "line": "Гортензії по краю сірого шовку. Про те, що лишається тільки між двома.", "size": "65 × 65 см · двосторонній друк", "price": "4 320 грн", "old": "4 800 грн", "url": "https://obiimy.world/dvostoronnii-druk/", "back": "prystrast"},
    {"id": "litnie-pole", "name": "Літнє поле", "line": "Букет, написаний за один день. Про літо, яке не хоче закінчуватись.", "size": "65 × 65 см · двосторонній друк", "price": "4 320 грн", "old": "4 800 грн", "url": "https://obiimy.world/dvostoronnii-druk/", "back": "probudzhennia"},
]

GARDEN = (ROOT / "garden.js").read_text()
for name in ["v-studio", "v-noir", "v-form", "garden"]:
    src = (ROOT / f"{name}.html").read_text()
    engine = GARDEN if name == "garden" else ENGINE
    out = src.replace("<script>/*ENGINE*/</script>", "<script>\n" + engine + "\n</script>")
    out = out.replace("/*STATES*/[]", json.dumps(STATES, ensure_ascii=False))
    (OUT / f"{name}.html").write_text(out)
    print(name, len(out) // 1024, "KB")
