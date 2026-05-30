# ترجم

إسأل أي ذكاء اصطناعي يترجم حاجة للعربية المصرية وعادة هتحصل على نتيجتين:
- فصحى رسمية (أو MSA) اللي محدش بيتكلمها
- أو لهجة شعبية مفرطة في التصحيح بإملاء مش متماسك زي الكاريكاتير

الأرض الوسط — العربية المحكية الطبيعية اللي بيتكلمها المصريين المتعلمين — نادرًا ما بتنجو في الترجمة.

Targem بيحل ده عن طريق توجيه النموذج بأمثلة، يعني Few-shot learning (FSL).

قبل كل ترجمة، بيسترجع الجمل الزوجية الأكثر صلة من مجموعة بيانات ثنائية اللغة مخصصة وبيقدمها للنموذج كأمثلة قليلة. النموذج بيتعلم أسلوبك من الأمثلة، مش بس من التعليمات، وده بيحافظ على الناتج متماسك ومنطقي.

ملف README ده مترجم للعربية المصرية باستخدام Targem: [README_ARZ.md](README_ARZ.md)

## ليه ترجم بيساعد

طلب بسيط زي `Translate this to Egyptian Arabic` غالبًا هيطلعلك عربي مفهوم لكن مشدود لـ `MSA`.

مثال للمدخلات:

```text
The Dutch department store that sells everything — and somehow feels like home
```

الناتج النموذجي من LLM:

```text
المتجر الهولندي الذي يبيع كل شيء ويمنحك بطريقة ما شعور المنزل
```

ناتج بأسلوب Targem:

```text
المحل الهولندي اللي بيبيع كل حاجة وبيحسسك إنك في بيتك
```

ليه التاني أحسن:
- `اللي` بدل `الذي`
- `كل حاجة` بدل `كل شيء`
- `بيحسسك` بدل الـ `يمنحك شعور` الجامدة
- الإيقاع العام بيبان زي العربية المصرية المنطوقة والمتعلمة، مش العربي الرسمي المرتب

الفرق ده هو الميزة في `targem`: مش بس ترجمة المعنى، لكن كمان سحب الأسلوب نحو العربية المصرية اللي فعلا عايزها.

## التثبيت

مُستحسن: تنزل بـ `uv` في وضع التعديل من جذر المستودع. ده بيخلي أمر `targem` متاح في أي مكان على جهازك وفي نفس الوقت يعكس التغييرات في الكود المحلي. التثبيت الافتراضي بيشمل دعم لكلود وOpenAI.

```bash
# after cloning the repo
cd /path/to/targem
uv tool install --editable .
```

لو دليل `bin` الخاص بـ `uv` مش موجود بالفعل في الـ `PATH`، ضيفه مرة واحدة:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

أوامر صيانة مفيدة:

```bash
# reinstall / refresh after dependency or metadata changes
uv tool install --editable --reinstall .

# remove the global command
uv tool uninstall targem
```

ممكن كمان تشغله من غير تثبيت عالمي من جذر المستودع:

```bash
uv run targem "Life is a terminal disease."
```

سلوك تحميل البيئة:
- `targem` أولًا بيحترم متغيرات البيئة الحالية
- بعدين بيحمل `~/.targem`
- المزود بيكون افتراضيًا `auto`
- `auto` بيفضل Claude لو الاتنين مزودين مهيئين؛ وإلا بيستخدم أي مفتاح مزود متاح
- المفاتيح المدعومة:
  - `ANTHROPIC_API_KEY`
  - `OPENAI_API_KEY`

## الاستخدام

```bash
# translate a string
targem "Life is a terminal disease."

# translate a file
targem --in essay.txt

# pipe input
cat article.txt | targem

# write translation directly to a file
targem "Some text." --out translation.txt

# file-to-file translation
targem --in article.txt --out translation.txt

# show which corpus examples were used
targem "Some text." --show-examples

# print retrieved exemplars and full prompt
targem "Some text." --debug-prompt

# control how many examples to retrieve (default 5)
targem "Some text." --k 3

# let targem infer provider from your keys
targem "Some text."

# use OpenAI instead of Claude
targem "Some text." --provider openai

# override the model
targem "Some text." --provider openai --model gpt-4-turbo

# run provider/network/model diagnostics
targem --doctor --provider openai
```

الإعداد الموصى بيه: عبّي ملف القالب `.targem` في المستودع، بعدين انسخه لدليل البيت الخاص بيك كـ `~/.targem`.

```bash
cp .targem ~/.targem
```

مثال `~/.targem`:

```env
ANTHROPIC_API_KEY=...   # for --provider claude or auto
OPENAI_API_KEY=...      # for --provider openai or auto
```

ترتيب القرار:
1. متغيرات البيئة الحالية
2. `~/.targem`

ده بيخلّي البيانات السرية برّه المستودع ويخلي `targem` شغال من أي مجلد على الجهاز.

المفاتيح المدعومة:

```env
ANTHROPIC_API_KEY=...   # for --provider claude or auto
OPENAI_API_KEY=...      # for --provider openai or auto
```

## التخطيط

- `corpus/` — الأصول ثنائية اللغة للكوربوس
- `src/targem/` — كود الحزمة
- `tests/` — اختبارات مؤتمتة
- `pyproject.toml` — بيانات تعريف الحزمة

## ملاحظات التطوير

- التثبيت القابل للتحرير بيتوجه للشجرة العاملة دي، عشان كده التغييرات تحت `src/targem/` بتظهر المرة الجاية اللى تشغل فيها `targem`.
- لو غيرت التبعيات، نقاط الدخول، أو بيانات تعريف الحزمة في `pyproject.toml`، شغل `uv tool install --editable --reinstall .` تاني.

## Doctor

استخدم `--doctor` لما تحتاج تشخيصات من غير ما تخلطها في سير عمل الترجمة.

الفحوصات تشمل:
- المورد المختار
- المفتاح موجود
- الحزمة مثبتة
- يعمل نظام أسماء النطاقات
- اتصال HTTPS شغال
- نداء النموذج شغال

مثال:

```bash
targem --doctor --provider openai
```
