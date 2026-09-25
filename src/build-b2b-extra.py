#!/usr/bin/env python3
"""Extra B2B pages: certificates, agencies, speakers, English, plus two 3D/art versions (b2b-garden, b2b-atelier)."""
import importlib.util, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent
_spec = importlib.util.spec_from_file_location("b2b", ROOT / "build-b2b.py")
b2b = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(b2b)
img, typo, hero, facts_html, proof_html, form_html, shell = b2b.img, b2b.typo, b2b.hero, b2b.facts_html, b2b.proof_html, b2b.form_html, b2b.shell
PHONE, PHONE_HREF, MAIL, SAMPLE_URL, EN = b2b.PHONE, b2b.PHONE_HREF, b2b.MAIL, b2b.SAMPLE_URL, b2b.EN
DOCS_FAQ, BATCH_FAQ = b2b.DOCS_FAQ, b2b.BATCH_FAQ
PROOF = proof_html("Де вже є Obiimy", "Obiimy продається у роздрібних партнерів в Україні та за кордоном, а історію бренду розповідали LIGA.net та INSIDER UA.", first=True)

def contact(title, text):
    return f'<div class="contact"><p class="eyebrow">Напишіть нам</p><h2>{title}</h2><p>{text}</p><p class="big"><a href="{PHONE_HREF}">{PHONE}</a></p><p><a href="mailto:{MAIL}">{MAIL}</a></p></div>'

BASE_FIELDS = [
    ("company", "Компанія", "input", True, {"ph": "Назва компанії", "ac": "organization"}),
    ("name", "Ваше ім’я", "input", True, {"ph": "Як до вас звертатись", "ac": "name"}),
    ("phone", "Телефон", "tel", True, {"ph": "+380", "ac": "tel", "err": "Вкажіть номер телефону"}),
    ("email", "Email", "email", True, {"ph": "для розрахунку", "ac": "email", "err": "Вкажіть коректний email"}),
]
PAY = ("payment", "Оплата", "select:Безготівково, ТОВ|Безготівково, ФОП|Карткою", False, {})


# ---------------------------------------------------------------- certificates (Studio)
def certificates():
    body = hero("Сертифікати · для команд і віддалених людей", "Подарунок, який людина обирає сама",
        "Подарунковий сертифікат Obiimy: ви тримаєте бюджет, а людина обирає хустку, твіллі чи маску для сну під себе. Без збору розмірів і адрес.<span class=\"m-hide\"> Для команд у різних містах і країнах — найпростіший корпоративний подарунок.</span>",
        "Отримати умови для команди", "Сертифікати на obiimy.world", "https://obiimy.world/sertyfikaty/",
        "Номінали під ціни речей: від 700 до 4 400 грн.", "photo/kolo-1.webp", "Жінка в шовковій хустці біля вікна", "Сертифікат — коли важливо, щоб обрали самі", pos="50% 12%") + facts_html([
        ("Без адрес", "Не потрібно збирати розміри, кольори й відділення пошти"),
        ("700 – 4 400 грн", "Номінали під роздрібні ціни речей"),
        ("Будь-де", "Для команд у різних містах і за кордоном"),
        ("Один запит", "Список імен і номінал — решту робимо ми"),
    ]) + f'''
  <section class="block" id="how"><div class="wrap">
    <div class="head"><p class="eyebrow">Як це працює</p><h2>Три кроки замість таблиці розмірів</h2></div>
    <div class="steps" style="grid-template-columns:repeat(3,minmax(0,1fr))">
      <div><h3>Номінал і список</h3><p>Оберіть суму на людину й надішліть список імен. Для ключових людей — інший номінал.</p></div>
      <div><h3>Сертифікати</h3><p>Електронний на email кожному або друкований у фірмовій коробці — формат узгоджуємо в запиті.</p></div>
      <div><h3>Вибір і доставка</h3><p>Людина обирає річ на obiimy.world; замовлення до 16:00 відправляємо того ж дня.</p></div>
    </div>
  </div></section>

  <section class="block alt" id="nominals"><div class="wrap">
    <div class="head"><p class="eyebrow">Номінали</p><h2>Що можна обрати на кожну суму</h2><p class="sub">Номінали прив’язані до роздрібних цін, щоб сертифікат покривав річ повністю.</p></div>
    <div class="grid4">
      <div class="card photo">{img("photo/scrunchie.jpg", "Резинка у фірмовій коробочці", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">700 грн</p><h3>Резинка</h3><p>Шовкова резинка у фірмовій коробочці.</p></div></div>
      <div class="card photo">{img("photo/paris-bun.jpg", "Твіллі у волоссі", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">1 600 грн</p><h3>Твіллі або паше</h3><p>Твіллі 84 × 5 чи хустка 44 × 44 — будь-який принт.</p></div></div>
      <div class="card photo">{img("photo/box-green.jpg", "Набір у жовтій коробці", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">3 200 грн</p><h3>Хустка 65 або набір</h3><p>Хустка 65 × 65 або набір «Натхнення».</p></div></div>
      <div class="card photo">{img("photo/kolo-3.webp", "Хустка на пальті", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">4 400 грн</p><h3>Шаль 88 × 88</h3><p>Велика хустка — на плечі, як топ, тюрбан.</p></div></div>
    </div>
    <p class="note">Номінал може бути будь-яким — це орієнтири, з якими зручно працювати.</p>
  </div></section>

  <section class="block" id="cases"><div class="wrap grid2">
    <figure>{img("photo/mizh-2.webp", "Шовкова хустка на голові, біле пальто", sizes="(max-width: 960px) 100vw, 50vw")}</figure>
    <div><p class="eyebrow">Коли сертифікат кращий за коробку</p><h2 style="margin-top:10px">Чотири ситуації</h2>
      <div class="faq" style="margin-top:22px">
        <details open><summary>Віддалена команда</summary><p>Люди в різних містах і країнах — сертифікат приходить на email, а річ людина замовляє сама, куди зручно.</p></details>
        <details><summary>Різні смаки</summary><p>Один принт на всіх не завжди працює. Із сертифікатом кожен обирає свій — і ніхто не передаровує.</p></details>
        <details><summary>Терміни горять</summary><p>Електронний сертифікат не залежить від пакування й пошти — зручно, коли до події лишилося кілька днів.</p></details>
        <details><summary>Подяка клієнту</summary><p>Сертифікат на шаль 88 × 88 — стриманий жест, який не виглядає як реклама.</p></details>
      </div>
    </div>
  </div></section>

  <section class="block alt" id="faq"><div class="wrap">
    <div class="head"><p class="eyebrow">Питання</p><h2>Що зазвичай питають</h2></div>
    <div class="faq">
      <details><summary>Якщо річ дорожча за номінал?</summary><p>Людина доплачує різницю при замовленні на obiimy.world.</p></details>
      <details><summary>Скільки діє сертифікат?</summary><p>Термін дії узгоджуємо в запиті — залежить від формату.</p></details>
      {DOCS_FAQ}
      <details><summary>Чи працює за кордоном?</summary><p>Так. Людина обирає річ на obiimy.world, доставка за кордон — за тарифами перевізника.</p></details>
    </div>
  </div></section>
  {PROOF}

  <section class="form-block alt" id="request"><div class="wrap">
    {contact("Отримати умови для команди", "Кількість людей і номінал — повернемось із розрахунком і форматом сертифікатів.")}
    <div>{form_html("f-cert", "Сертифікати для команди", BASE_FIELDS + [
        ("qty", "Кількість сертифікатів", "number", False, {"ph": "наприклад, 25"}),
        ("nominal", "Номінал", "select:700 грн|1 600 грн|3 200 грн|4 400 грн|інший", False, {}),
        ("format", "Формат", "select:Електронний на email|Друкований у коробці|Ще не знаю", False, {}),
        PAY,
        ("note", "Коментар", "textarea", False, {"ph": "Привід, терміни, різні номінали для різних людей…"}),
    ], "")}</div>
  </div></section>'''
    return dict(slug="b2b-certificates", skin="studio", title="Подарункові сертифікати Obiimy для команд",
        desc="Корпоративні сертифікати на шовкові хустки: номінали від 700 до 4 400 грн, електронні або друковані, без збору розмірів і адрес. Для віддалених команд і клієнтів.",
        og="photo/kolo-1.webp", nav=[("Як це працює", "how"), ("Номінали", "nominals"), ("Коли доречно", "cases"), ("Питання", "faq"), ("Контакт", "request")],
        cta="Запит", sticky="Сертифікати для команд · від 700 грн", body=body)


# ---------------------------------------------------------------- agencies (Form)
def agencies():
    body = hero("Для event-, HR- і подарункових агенцій", "Шовк, який легко продати вашому клієнту",
        "Ви ведете клієнта — ми даємо продукт, матеріали й логістику: лукбук для презентації, зразки, фірмова коробка з листівкою клієнта, відправка кожному адресату.<span class=\"m-hide\"> Один менеджер на всі проєкти агенції.</span>",
        "Стати партнером", "Лукбук і роздрібні ціни (PDF, 3 МБ)", "lookbook-obiimy-2026.pdf",
        "Агентські умови обговорюємо після першого запиту.", "photo/dotyk-2.webp", "Шовкова хустка на тренчі", "Продукт, який легко презентувати клієнту", pos="50% 14%") + facts_html([
        ("PDF-лукбук", "Пакшоти, дві зйомки й історія бренду — для ваших презентацій"),
        ("Зразки", "Речі з каталогу в роздріб — для показу клієнту"),
        ("Брендинг", "Листівка з текстом і логотипом клієнта в кожній коробці"),
        ("Один менеджер", "На всі проєкти агенції — від брифу до накладних"),
    ]) + f'''
  <section class="block" id="give"><div class="wrap">
    <div class="head"><p class="eyebrow">Що отримує агенція</p><h2>Ви продаєте ідею — ми закриваємо решту</h2></div>
    <div class="grid4">
      <div class="card"><span class="k">01</span><h3>Матеріали для пітчу</h3><p>Лукбук, пакшоти на білому, лайфстайл-зйомки й історія бренду — для презентації клієнту.</p></div>
      <div class="card"><span class="k">02</span><h3>Швидкий розрахунок</h3><p>Кількість і бюджет — повертаємось із добіркою принтів і цінами на тираж.</p></div>
      <div class="card"><span class="k">03</span><h3>Брендинг клієнта</h3><p>Листівка з привітанням і логотипом клієнта; підпис від руки за бажанням.</p></div>
      <div class="card"><span class="k">04</span><h3>Доставка і звіт</h3><p>В офіс або кожному адресату Новою поштою; після відправки — номери накладних.</p></div>
    </div>
  </div></section>

  <section class="block alt" id="range"><div class="wrap">
    <div class="head"><p class="eyebrow">Продукт</p><h2>Що пропонувати клієнтам</h2><p class="sub">Роздрібні ціни з obiimy.world — орієнтир для кошторису.</p></div>
    <div class="grid4">
      <div class="card photo">{img("photo/scrunchie.jpg", "Резинка у фірмовій коробочці", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><h3>Резинка</h3><p>Масові подарунки, welcome-pack.</p><div class="price-row"><span>Роздріб</span><span class="num">700 грн</span></div></div></div>
      <div class="card photo">{img("photo/paris-belt.jpg", "Твіллі як пояс на тренчі", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><h3>Твіллі · паше</h3><p>Команда, спікери, гості.</p><div class="price-row"><span>Роздріб</span><span class="num">1 600 грн</span></div></div></div>
      <div class="card photo">{img("photo/box-gold.jpg", "Набір у фірмовій коробці", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><h3>Набори</h3><p>Ключові люди, партнери.</p><div class="price-row"><span>Роздріб</span><span class="num">2 200 – 4 800 грн</span></div></div></div>
      <div class="card photo">{img("photo/riviera-boat.jpg", "Хустка на плечах", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><h3>Хустки 65 · 88</h3><p>VIP-клієнти, керівники.</p><div class="price-row"><span>Роздріб</span><span class="num">3 200 – 4 400 грн</span></div></div></div>
    </div>
  </div></section>

  <section class="block" id="how"><div class="wrap grid2">
    <div><p class="eyebrow">Як працюємо</p><h2 style="margin-top:10px">Від брифу до накладних</h2>
      <div class="steps" style="grid-template-columns:1fr;gap:18px;margin-top:22px">
        <div><h3>Бриф</h3><p>Клієнт, привід, кількість, бюджет, дата. Досить одного листа.</p></div>
        <div><h3>Добірка і зразок</h3><p>Принти й речі під бюджет із розрахунком на тираж; зразок — у роздріб.</p></div>
        <div><h3>Погодження</h3><p>Принти, текст листівки, список адрес. Рахунок на агенцію або на клієнта.</p></div>
        <div><h3>Відправка</h3><p>Пакування, відправка за списком, номери накладних.</p></div>
      </div>
    </div>
    <figure>{img("photo/hratsiia-belt.webp", "Хустка як пояс на синьому жакеті", sizes="(max-width: 960px) 100vw, 50vw")}</figure>
  </div></section>

  <section class="block alt" id="faq"><div class="wrap">
    <div class="head"><p class="eyebrow">Питання</p><h2>Що зазвичай питають</h2></div>
    <div class="faq">
      <details><summary>Які агентські умови?</summary><p>Обговорюємо після першого запиту — залежать від обсягу й регулярності проєктів.</p></details>
      <details><summary>Рахунок на агенцію чи на клієнта?</summary><p>Як зручно — узгоджуємо в запиті.</p></details>
      <details><summary>Чи можна використовувати фото Obiimy в презентаціях?</summary><p>Для презентації подарунків клієнту — так, лукбук і пакшоти для цього й надаємо.</p></details>
      {DOCS_FAQ}
      {BATCH_FAQ}
    </div>
  </div></section>
  {PROOF}

  <section class="form-block alt" id="request"><div class="wrap">
    {contact("Стати партнером", "Розкажіть про агенцію та найближчий проєкт — повернемось із матеріалами й умовами.")}
    <div>{form_html("f-ag", "Партнерство з агенцією", [
        ("company", "Агенція", "input", True, {"ph": "Назва агенції", "ac": "organization"}),
        BASE_FIELDS[1], BASE_FIELDS[2],
        ("email", "Email", "email", True, {"ph": "для матеріалів і умов", "ac": "email", "err": "Вкажіть коректний email"}),
        ("type", "Профіль агенції", "select:Event|HR / корпоративна культура|Подарунки та мерч|PR / комунікації|Інше", False, {}),
        ("qty", "Найближчий проєкт, шт.", "number", False, {"ph": "наприклад, 80"}),
        ("project", "Клієнт, привід, дата", "input", False, {"ph": "наприклад, IT-компанія, Новий рік, до 10 грудня", "full": True}),
        ("invoice", "Рахунок", "select:На агенцію|На клієнта|Ще не знаю", False, {}),
        ("note", "Коментар", "textarea", False, {"ph": "Бюджет на подарунок, брендинг клієнта, побажання до принтів…"}),
    ], "")}</div>
  </div></section>'''
    return dict(slug="b2b-agencies", skin="form", title="Obiimy для event-, HR- і подарункових агенцій",
        desc="Партнерська програма для агенцій: лукбук і пакшоти для пітчу, зразки, фірмова коробка з листівкою клієнта, відправка кожному адресату, рахунок на агенцію або клієнта.",
        og="photo/dotyk-2.webp", nav=[("Що отримує агенція", "give"), ("Продукт", "range"), ("Як працюємо", "how"), ("Питання", "faq"), ("Контакт", "request")],
        cta="Партнерство", sticky="Для агенцій · один постачальник", body=body)


# ---------------------------------------------------------------- speakers & event guests (Classic)
def speakers():
    body = hero("Конференції · форуми · корпоративні події", "Спікеру — не блокнот, а шовк",
        "Твіллі у фірмовій коробці замість чергового блокнота з логотипом: подарунок, який спікер надягне того ж вечора, а гості сфотографують.<span class=\"m-hide\"> Від десяти до кількох сотень коробок — один принт події або добірка.</span>",
        "Порахувати для події", "Замовити зразок", SAMPLE_URL,
        "Зразок — від 1 600 грн у роздріб, у тій самій коробці.", "photo/probudzhennia-3.webp", "Жінка в білому жакеті та шовковій хустці", "Один принт події — і сцена виглядає зібрано", pos="50% 16%") + facts_html([
        ("1 600 грн", "Твіллі або паше в коробці — головний формат для спікерів"),
        ("700 грн", "Резинка в коробочці — для гостей і welcome-pack"),
        ("Один принт", "Принт події під кольори айдентики — з колекцій Obiimy"),
        ("3 тижні", "Рекомендований запас до дати для тиражу з листівками"),
    ]) + f'''
  <section class="block" id="formats"><div class="wrap">
    <div class="head"><p class="eyebrow">Формати</p><h2>Кому і що дарувати на події</h2></div>
    <div class="grid4">
      <div class="card photo">{img("photo/paris-bag.jpg", "Твіллі на ручці сумки", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><h3>Спікерам</h3><p>Твіллі 84 × 5 у коробці з листівкою від організаторів.</p><div class="price-row"><span>Роздріб</span><span class="num">1 600 грн</span></div></div></div>
      <div class="card photo">{img("photo/scrunchie.jpg", "Резинка у коробочці", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><h3>Гостям</h3><p>Резинка у фірмовій коробочці — маленька, помітна, не викидається.</p><div class="price-row"><span>Роздріб</span><span class="num">700 грн</span></div></div></div>
      <div class="card photo">{img("photo/box-dots.jpg", "Набір у жовтій коробці", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><h3>Партнерам події</h3><p>Набір «Натхнення» або хустка 65 × 65 — для спонсорів.</p><div class="price-row"><span>Роздріб</span><span class="num">3 200 грн</span></div></div></div>
      <div class="card photo">{img("photo/paris-dots.jpg", "Велика хустка на плечах", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><h3>Хедлайнеру</h3><p>Шаль 88 × 88 — подарунок, який запам’ятають.</p><div class="price-row"><span>Роздріб</span><span class="num">4 400 грн</span></div></div></div>
    </div>
  </div></section>

  <section class="block alt" id="why"><div class="wrap grid2">
    <div><p class="eyebrow">Чому це працює</p><h2 style="margin-top:10px">Подарунок, який потрапляє в кадр</h2>
      <div class="faq" style="margin-top:22px">
        <details open><summary>Його надягають одразу</summary><p>Твіллі на шию чи на сумку — і спікер уже в кадрі фотографа події з вашим подарунком.</p></details>
        <details><summary>Принт події</summary><p>Один принт на всіх спікерів читається як дрес-код сцени; підбираємо з колекцій під кольори айдентики.</p></details>
        <details><summary>Є що розповісти зі сцени</summary><p>Авторські принти художниці Світлани Сніжко, італійський шовк, ручна обробка, українське виробництво.</p></details>
        <details><summary>Один розмір на всіх</summary><p>Твіллі, паше й резинка — не треба збирати мірки.</p></details>
      </div>
    </div>
    <figure>{img("photo/kolo-2.webp", "Хустка на бежевому пальті", sizes="(max-width: 960px) 100vw, 50vw")}</figure>
  </div></section>

  <section class="block" id="timeline"><div class="wrap">
    <div class="head"><p class="eyebrow">Терміни</p><h2>Щоб коробки були на майданчику вчасно</h2><p class="sub">Рекомендований графік для тиражу з листівками. Речі з наявності відправляємо того ж дня при замовленні до 16:00.</p></div>
    <div class="timeline">
      <div><p class="eyebrow">За 3 тижні</p><b>Запит і зразок</b><p>Кількість, формат, кольори події. Добірка принтів, розрахунок, зразок у роздріб.</p></div>
      <div><p class="eyebrow">За 2 тижні</p><b>Погодження</b><p>Принт події, текст листівки, рахунок.</p></div>
      <div><p class="eyebrow">За 3–5 днів</p><b>Відправка</b><p>Одна посилка на майданчик або в офіс організатора.</p></div>
    </div>
  </div></section>

  <section class="block alt" id="faq"><div class="wrap">
    <div class="head"><p class="eyebrow">Питання</p><h2>Що зазвичай питають</h2></div>
    <div class="faq">
      <details><summary>Мінімальна кількість?</summary><p>Фіксованого мінімуму немає — і десять коробок для спікерів, і кілька сотень для гостей.</p></details>
      <details><summary>Логотип події на коробці?</summary><p>Стандартно — листівка з вашим текстом і логотипом усередині фірмової коробки Obiimy. Інший брендинг обговорюємо окремо.</p></details>
      {DOCS_FAQ}
      {BATCH_FAQ}
    </div>
  </div></section>
  {PROOF}

  <section class="form-block alt" id="request"><div class="wrap">
    {contact("Порахувати для події", "Дата, кількість спікерів і гостей — повернемось із добіркою принтів і розрахунком.")}
    <div>{form_html("f-sp", "Подарунки для події", [
        ("company", "Організатор", "input", True, {"ph": "Компанія або назва події", "ac": "organization"}),
        BASE_FIELDS[1], BASE_FIELDS[2], BASE_FIELDS[3],
        ("date", "Дата події", "input", False, {"ph": "наприклад, 14 травня"}),
        ("speakers", "Спікерів", "number", False, {"ph": "наприклад, 20"}),
        ("guests", "Гостей із подарунком", "number", False, {"ph": "наприклад, 150"}),
        PAY,
        ("note", "Коментар", "textarea", False, {"ph": "Кольори події, місто майданчика, побажання до принтів…"}),
    ], "")}</div>
  </div></section>'''
    return dict(slug="b2b-speakers", skin="classic", title="Подарунки спікерам і гостям подій — Obiimy",
        desc="Твіллі та хустки Obiimy у фірмовій коробці для спікерів, гостей і партнерів конференцій: один принт події, від 700 грн, зразок сьогодні, тираж за три тижні.",
        og="photo/probudzhennia-3.webp", nav=[("Формати", "formats"), ("Чому це працює", "why"), ("Терміни", "timeline"), ("Питання", "faq"), ("Контакт", "request")],
        cta="Запит", sticky="Подарунки для події · від 700 грн", body=body)


# ---------------------------------------------------------------- English (Campaign)
def english():
    body = hero("Corporate gifts from Ukraine", "A gift that carries a story",
        "Silk scarves with original prints by Ukrainian artist Svitlana Snizhko, on 100% Italian silk, hand-finished in Ukraine.<span class=\"m-hide\"> For teams abroad, partners and clients — in a signature yellow box with your card.</span>",
        "Get a selection and quote", "Shop obiimy-world.com", "https://obiimy-world.com/",
        "Worldwide shipping at carrier rates.", "photo/vyr-3.webp", "Woman in a silk headscarf and white coat", "Every gift in a signature box with your card", pos="50% 14%", L=EN) + facts_html([
        ("100% silk", "Italian silk, original prints, hand-finished edges"),
        ("Made in Ukraine", "A brand born during the war, supporting charity projects"),
        ("₴700 – ₴4 800", "Retail prices in hryvnia; volume terms on request"),
        ("Worldwide", "Shipping at carrier rates to one or many addresses"),
    ]).replace('aria-label="Коротко про бренд"', 'aria-label="The brand in brief"') + f'''
  <section class="block" id="why"><div class="wrap">
    <div class="head"><p class="eyebrow">Why silk from Ukraine</p><h2>Instead of another branded notebook</h2><p class="sub">A corporate gift has three enemies: it gets eaten, forgotten or re-gifted. A silk scarf stays in a wardrobe for years and tells a story every time it is worn.</p></div>
    <div class="grid4">
      <div class="card"><span class="k">01</span><h3>A story to tell</h3><p>Each print is a painting. The Singing Soul collection, made with artist Anna Klovak and the Ukrainian Society for the Protection of Birds, funds nesting boxes for the endangered European roller.</p></div>
      <div class="card"><span class="k">02</span><h3>One budget, many pieces</h3><p>Scrunchie, twilly, sleep mask, scarves in three sizes, gift sets — a choice within one budget.</p></div>
      <div class="card"><span class="k">03</span><h3>Your card inside</h3><p>A greeting card with your message in every box; handwritten on request.</p></div>
      <div class="card"><span class="k">04</span><h3>Ships worldwide</h3><p>One parcel to your office or to each recipient, at carrier rates.</p></div>
    </div>
  </div></section>

  <section class="block alt" id="budgets"><div class="wrap">
    <div class="head"><p class="eyebrow">Budgets</p><h2>Four budgets, one level of quality</h2><p class="sub">Retail prices from obiimy.world in Ukrainian hryvnia. Volume terms depend on quantity and timing — we quote on request.</p></div>
    <div class="grid4">
      <div class="card photo">{img("photo/scrunchie.jpg", "Silk scrunchie in a yellow box", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">Up to ₴1 000</p><h3>A small token</h3><div class="price-row"><span>Scrunchie in a box</span><span class="num">₴700</span></div></div></div>
      <div class="card photo">{img("photo/paris-bag.jpg", "Twilly on a handbag", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">Up to ₴2 000</p><h3>For the whole team</h3><div class="price-row"><span>Twilly 84 × 5</span><span class="num">₴1 600</span></div><div class="price-row"><span>Scarf 44 × 44</span><span class="num">₴1 600</span></div></div></div>
      <div class="card photo">{img("photo/box-red.jpg", "Gift set in a yellow box", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">Up to ₴3 500</p><h3>For key people</h3><div class="price-row"><span>Sleep mask</span><span class="num">₴2 700</span></div><div class="price-row"><span>Scarf 65 × 65</span><span class="num">₴3 200</span></div><div class="price-row"><span>Twilly + scarf set</span><span class="num">₴3 200</span></div></div></div>
      <div class="card photo">{img("photo/paris-dots.jpg", "Large scarf on the shoulders", sizes="(max-width: 640px) 50vw, 25vw")}<div class="in"><p class="eyebrow">Up to ₴5 000</p><h3>For partners and VIPs</h3><div class="price-row"><span>Scarf 88 × 88</span><span class="num">₴4 400</span></div><div class="price-row"><span>Three twillies</span><span class="num">₴4 800</span></div></div></div>
    </div>
  </div></section>

  <section class="block" id="how"><div class="wrap grid2">
    <div><p class="eyebrow">How it works</p><h2 style="margin-top:10px">From request to delivery</h2>
      <div class="steps" style="grid-template-columns:1fr;gap:18px;margin-top:22px">
        <div><h3>Request</h3><p>Quantity, budget per gift, destination countries. One email is enough.</p></div>
        <div><h3>Selection and quote</h3><p>Prints and pieces for your budget with a quote; a sample can be ordered at retail.</p></div>
        <div><h3>Approval</h3><p>Prints, the text of your card, the list of recipients. Invoice for company payment.</p></div>
        <div><h3>Shipping</h3><p>To one address or to each recipient, with tracking numbers after dispatch.</p></div>
      </div>
    </div>
    <figure>{img("photo/riviera-car.jpg", "Silk headscarf in a convertible", sizes="(max-width: 960px) 100vw, 50vw")}</figure>
  </div></section>

  <section class="block alt" id="faq"><div class="wrap">
    <div class="head"><p class="eyebrow">Questions</p><h2>What we are usually asked</h2></div>
    <div class="faq">
      <details><summary>Is there a minimum order?</summary><p>No fixed minimum — we discuss every request individually. Quantity affects timing and terms.</p></details>
      <details><summary>How do we pay from abroad?</summary><p>By invoice for companies; samples and small orders by card at obiimy-world.com.</p></details>
      <details><summary>How long does shipping take?</summary><p>It depends on the destination and carrier; we quote the option and cost together with the gifts.</p></details>
      <details><summary>Are all pieces identical?</summary><p>Print and colour are identical within a batch. Size may vary by 0–2.5 cm because edges are finished by hand.</p></details>
    </div>
  </div></section>

  <section class="block" id="proof"><div class="wrap grid2" style="align-items:start">
    <div><p class="eyebrow">Trust</p><h2 style="margin-top:10px">Where Obiimy already is</h2><p style="margin-top:14px;color:var(--ink2);max-width:36em">Obiimy is sold by retail partners in Ukraine and abroad, and its story has been covered by LIGA.net and INSIDER UA.</p></div>
    <div><div class="proof">
      <div><b>INTERTOP · Hram</b><span>Retail partners in Ukraine</span></div>
      <div><b>Be Brave</b><span>Partner in Canada</span></div>
      <div><b>UFD London</b><span>Partner in the United Kingdom</span></div>
      <div><b class="num">5.0</b><span>Rating on obiimy.world</span></div>
    </div></div>
  </div></section>

  <section class="form-block alt" id="request"><div class="wrap">
    <div class="contact"><p class="eyebrow">Write to us</p><h2>Get a selection and quote</h2><p>Tell us about the team and the budget — we come back with prints, a quote and shipping options.</p><p class="big"><a href="{PHONE_HREF}">{PHONE}</a></p><p><a href="mailto:{MAIL}">{MAIL}</a></p></div>
    <div>{form_html("f-en", "Corporate gifts request", [
        ("company", "Company", "input", True, {"ph": "Company name", "ac": "organization", "err": "Please fill in this field"}),
        ("name", "Your name", "input", True, {"ph": "How should we address you", "ac": "name", "err": "Please fill in this field"}),
        ("phone", "Phone", "tel", True, {"ph": "+1 …", "ac": "tel", "err": "Please enter a phone number"}),
        ("email", "Email", "email", True, {"ph": "for the selection and quote", "ac": "email", "err": "Please enter a valid email"}),
        ("qty", "Number of gifts", "number", False, {"ph": "e.g. 30"}),
        ("budget", "Budget per gift", "select:up to ₴1 000|up to ₴2 000|up to ₴3 500|up to ₴5 000|other", False, {}),
        ("countries", "Destination countries", "input", False, {"ph": "e.g. Germany, USA, Canada", "full": True}),
        ("delivery", "Delivery", "select:One parcel to our office|A parcel to each recipient|Not sure yet", False, {}),
        ("note", "Comments", "textarea", False, {"ph": "Occasion, deadline, card text, print preferences…"}),
    ], "", L=EN)}</div>
  </div></section>'''
    return dict(slug="b2b-en", skin="campaign", lang="en", title="Corporate gifts from Ukraine — Obiimy silk",
        desc="Silk scarves with original prints, hand-finished in Ukraine, for teams abroad, partners and clients. From ₴700 to ₴4 800 per gift, signature box with your card, worldwide shipping.",
        og="photo/vyr-3.webp", nav=[("Why", "why"), ("Budgets", "budgets"), ("How it works", "how"), ("Questions", "faq"), ("Contact", "request")],
        cta="Request", sticky="Corporate gifts · from ₴700", body=body)


# ---------------------------------------------------------------- 3D versions
def _states():
    src = (ROOT / "build.py").read_text(); ns = {}
    exec(src[src.index("STATES = ["):src.index("GARDEN = ")], {}, ns)
    return ns["STATES"]

def inline(tpl, engine_file, form):
    html = typo(tpl.replace("<!--FORM-->", form))
    html = html.replace("<script>/*ENGINE*/</script>", "<script>\n" + (ROOT / engine_file).read_text() + "\n</script>")
    return html.replace("/*STATES*/[]", json.dumps(_states(), ensure_ascii=False))

def garden_b2b():
    form = form_html("f-3d", "Корпоративні подарунки", BASE_FIELDS + [
        ("qty", "Кількість подарунків", "number", False, {"ph": "наприклад, 30"}),
        ("budget", "Бюджет на один подарунок", "select:до 1 000 грн|до 2 000 грн|до 3 500 грн|до 5 000 грн|інший", False, {}),
        ("deadline", "Коли потрібно", "select:До 10 грудня|До 20 грудня|Після свят|Інша дата", False, {}),
        PAY,
        ("note", "Коментар", "textarea", False, {"ph": "Привід, побажання до принтів, текст листівки…"}),
    ], "")
    return inline((ROOT / "b2b-garden.html").read_text(), "garden.js", form)

def atelier():
    form = form_html("f-at", "Конфігурація з ательє подарунка", BASE_FIELDS + [
        ("qty", "Кількість подарунків", "number", False, {"ph": "з конфігуратора"}),
        ("deadline", "Коли потрібно", "select:До 10 грудня|До 20 грудня|Після свят|Інша дата", False, {}),
        ("delivery", "Доставка", "select:В офіс однією посилкою|Кожному на відділення Нової пошти|Ще не знаю", False, {}),
        PAY,
        ("note", "Конфігурація і коментар", "textarea", False, {"ph": "Заповнюється з конфігуратора"}),
    ], "")
    return inline((ROOT / "b2b-atelier.html").read_text(), "silk-engine.js", form)


if __name__ == "__main__":
    b2b.build_all([certificates, agencies, speakers, english])
    for slug, fn in (("b2b-garden", garden_b2b), ("b2b-atelier", atelier)):
        html = fn(); (OUT / f"{slug}.html").write_text(html); print(slug, len(html) // 1024, "KB")
