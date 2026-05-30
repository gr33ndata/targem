# ترجم

لما تطلب من الذكاء الاصطناعي يترجم حاجة للمصري، غالبًا هتاخد واحد من نتيجتين:
- فصحى رسمية محدش بيتكلم بيها فعلًا
- أو لهجة شوارع متكلفة زيادة وتهجيها مش ثابت وبتطلع كاريكاتير

المنطقة الوسط ديه — المصري الطبيعي المثقف اللي ناس متعلمة بتكتبه وبتتكلمه — نادرًا ما بتنجو في الترجمة.

**ترجم بيحل المشكلة ديه عن طريق توجيه النموذج بأمثلة، يعني Few-shot learning (FSL).**

قبل كل ترجمة، بيسترجع أكتر أزواج جمل شبه النص المطلوب من corpus ثنائي اللغة متظبط بعناية، وبيبعتها للنموذج كأمثلة. النموذج بيتعلم الـ register من الأمثلة، مش من التعليمات وبس، وده بيخلي الناتج أهدى، أثبت، وأقرب للمصري اللي إنت عايزه.

النسخة العربية من الـ README ده مترجمة بترجم: [README_ARZ.md](README_ARZ.md)

## ليه ترجم مفيد

لو كتبت prompt عادي زي `Translate this to Egyptian Arabic`، غالبًا هتاخد عربي مفهوم، بس لسه بيزحف ناحية `الفصحى`.

مثال input:

```text
The Dutch department store that sells everything — and somehow feels like home
```

ناتج vanilla LLM المعتاد:

```text
المتجر الهولندي الذي يبيع كل شيء ويمنحك بطريقة ما شعور المنزل
```

ناتج أقرب لأسلوب ترجم:

```text
المحل الهولندي اللي بيبيع كل حاجة وبيحسسك إنك في بيتك
```

ليه التاني أحسن:

- `اللي` بدل `الذي`
- `كل حاجة` بدل `كل شيء`
- `بيحسسك` بدل التركيب الأنشف `يمنحك شعور`
- الإيقاع كله مصري طبيعي ومثقف، مش عربي متشطب على طريقة الفصحى

وده أصلًا هدف `targem`: مش بس ينقل المعنى، لكن كمان يشد الـ register ناحية المصري اللي إنت فعلًا عايزه.

## التثبيت

الأفضل: ثبّت الأداة بـ `uv` في وضع editable من جذر الـ repo. كده أمر `targem` هيبقى شغال من أي مكان على الجهاز، وأي تعديل محلي هيبان مباشرة. التثبيت الافتراضي بيشمل دعم Claude و OpenAI.

```bash
# بعد ما تعمل clone للـ repo
cd /path/to/targem
uv tool install --editable .
```

لو مجلد bin بتاع `uv` مش موجود في `PATH`، ضيفه مرة واحدة:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

أوامر صيانة مفيدة:

```bash
# إعادة تثبيت / تحديث بعد أي تغيير في dependencies أو metadata
uv tool install --editable --reinstall .

# إزالة الأمر من على الجهاز
uv tool uninstall targem
```

وتقدر تشغله من غير تثبيت عام من جذر الـ repo:

```bash
uv run targem "Life is a terminal disease."
```

سلوك تحميل environment:

- `targem` الأول بيحترم أي environment variables موجودة بالفعل
- بعد كده بيحمّل `~/.targem`
- الـ provider الافتراضي هو `auto`
- `auto` بيفضل Claude لو الاتنين موجودين، وإلا بيستخدم أي key متاحة
- الـ keys المدعومة:
  - `ANTHROPIC_API_KEY`
  - `OPENAI_API_KEY`

## الاستخدام

```bash
# ترجمة string
targem "Life is a terminal disease."

# ترجمة ملف
targem --in essay.txt

# ترجمة من stdin
cat article.txt | targem

# كتابة الترجمة مباشرة في ملف
targem "Some text." --out translation.txt

# ترجمة من ملف لملف
targem --in article.txt --out translation.txt

# عرض الأمثلة اللي اتسحبت من الـ corpus
targem "Some text." --show-examples

# طباعة الأمثلة والـ prompt الكامل
targem "Some text." --debug-prompt

# التحكم في عدد الأمثلة المسترجعة (الافتراضي 5)
targem "Some text." --k 3

# خليه يحدد الـ provider من الـ keys الموجودة
targem "Some text."

# استخدم OpenAI بدل Claude
targem "Some text." --provider openai

# override للموديل
targem "Some text." --provider openai --model gpt-4-turbo

# تشخيص provider / network / model call
targem --doctor --provider openai
```

الإعداد المقترح: املا ملف القالب `.targem` اللي في الـ repo، وبعد كده انسخه للـ home directory باسم `~/.targem`.

```bash
cp .targem ~/.targem
```

مثال `~/.targem`:

```env
ANTHROPIC_API_KEY=...   # لـ --provider claude أو auto
OPENAI_API_KEY=...      # لـ --provider openai أو auto
```

ترتيب التحميل:

1. environment variables الموجودة بالفعل
2. `~/.targem`

وده بيخلي الـ credentials برا الـ repo وبيخلي `targem` يشتغل من أي فولدر على الجهاز.

الـ keys المدعومة:

```env
ANTHROPIC_API_KEY=...   # لـ --provider claude أو auto
OPENAI_API_KEY=...      # لـ --provider openai أو auto
```

## المجلدات

- `corpus/` — ملفات الـ corpus الثنائية المتسجلة مع المشروع
- `src/targem/` — كود الحزمة
- `tests/` — اختبارات تلقائية
- `pyproject.toml` — بيانات تعريف الحزمة

## ملاحظات للتطوير

- التثبيت editable بيربط الأداة مباشرة بالشجرة الحالية، فالتغييرات تحت `src/targem/` بتبان أول ما تشغل `targem`.
- لو غيرت dependencies أو entry points أو metadata في `pyproject.toml`، شغل `uv tool install --editable --reinstall .` تاني.

## Doctor

استخدم `--doctor` لما تحتاج تشخيص من غير ما تلخبطه مع مخرجات الترجمة.

الـ checks تشمل:

- الـ provider المختار
- هل الـ key موجودة
- هل الباكدج متثبتة
- هل DNS شغال
- هل HTTPS شغال
- هل model call شغالة

مثال:

```bash
targem --doctor --provider openai
```
