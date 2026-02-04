import os
from flask import Flask, render_template_string, request, session, redirect, url_for
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "secret123"


AI_INTEGRATIONS_OPENAI_API_KEY = os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY")
AI_INTEGRATIONS_OPENAI_BASE_URL = os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL")

openai_client = OpenAI(
    api_key=AI_INTEGRATIONS_OPENAI_API_KEY,
    base_url=AI_INTEGRATIONS_OPENAI_BASE_URL
)

# ---------- OpenAI AI ---------- #
def ai_reply(prompt):
    try:
        result = openai_client.responses.create(
            model="gpt-5-mini",
            input=prompt,
            max_output_tokens=1024
        )
        reply = result.output_text
        if not reply:
            reply = "⚠️ حدث خلل مؤقت من الذكاء الصناعي، حاول مرة أخرى."
            
        return reply

    except Exception as e:
        return f"حدث خطأ: {str(e)}"
        
def evaluate_debate(chat, topic):
    full_chat = "\n".join([f"{m['role']}: {m['content']}" for m in chat])
    prompt = f"""
أنت مقيم مناظرات محترف.
قيّم هذه المناظرة حول الموضوع:
{topic}

النقاش:
{full_chat}

أعطِ تقييم من 10 مع سبب مختصر من دون رموز غريبه ويمكن استخدام الاعشار في التقيم مثلا7.5 وهكذا تكتب التقيم مثلا (لقد حصلت على تقيم 3.8من 10) .
تقيمك يكون بل اعتماد على:مدى التعمق بالنقاش و طول جواب المستخدم وفهمه للأسءلة واسوب تفكيره وما الى ذاك.
عليك انت تكون صارم في التقيم بدون مراعات.
"""
    return ai_reply(prompt)

# ---------- HTML ---------- #

NAME_PAGE = """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>AI Debate Arena</title>
<style>
body {
    font-family: Tahoma, Arial;
    background: linear-gradient(135deg, #1d2671, #c33764);
    height: 100vh;
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
}

.container {
    background: rgba(0,0,0,0.4);
    padding: 35px;
    border-radius: 15px;
    width: 420px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    text-align: center;
    animation: fadeIn 0.8s ease;
}

h2 {
    margin-bottom: 25px;
    font-size: 28px;
}

label {
    float: right;
    font-size: 16px;
    margin-bottom: 5px;
}

input {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    border-radius: 8px;
    border: none;
    margin-bottom: 18px;
}

button {
    width: 100%;
    padding: 12px;
    font-size: 18px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    background: #00c6ff;
    color: #000;
    transition: 0.3s;
}

button:hover {
    background: #00f2fe;
    transform: scale(1.03);
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
</head>
<body>

<div class="container">
    <h2>🧠 AI Debate Arena</h2>
    <form method="POST">
        <label>اسمك</label>
        <input name="username" required>

        <label>موضوع المناظرة</label>
        <input name="topic" required>

        <button type="submit">🚀 ابدأ المناظرة</button>
    </form>
</div>

</body>
</html>
"""


CHAT_PAGE = """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>AI Debate</title>
<style>
body {
    font-family: Tahoma, Arial;
    background: #0f2027;
    background: linear-gradient(135deg, #2c5364, #203a43, #0f2027);
    margin: 0;
    padding: 0;
    color: #fff;
}

.wrapper {
    max-width: 900px;
    margin: 40px auto;
    background: rgba(0,0,0,0.4);
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    animation: fadeIn 0.6s ease;
}

h2, h3 {
    text-align: center;
}

.chat-box {
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 10px;
    padding: 15px;
    height: 350px;
    overflow-y: auto;
    background: rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

.msg {
    margin-bottom: 12px;
    line-height: 1.7;
}

.msg b {
    color: #00f2fe;
}

.input-area {
    display: flex;
    gap: 10px;
}

input[type="text"] {
    flex: 1;
    padding: 14px;
    font-size: 16px;
    border-radius: 8px;
    border: none;
}

button {
    padding: 14px 20px;
    font-size: 16px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    background: #00c6ff;
    color: #000;
    transition: 0.3s;
}

button:hover {
    background: #00f2fe;
    transform: scale(1.05);
}

.result {
    background: rgba(0,0,0,0.3);
    padding: 20px;
    border-radius: 10px;
    font-size: 18px;
    line-height: 1.8;
}

a {
    color: #00f2fe;
    text-decoration: none;
    font-size: 18px;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(15px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
</head>
<body>

<div class="wrapper">
    <h2>👤 {{username}}</h2>
    <h3>📌 {{topic}}</h3>

    <div class="chat-box">
        {% for msg in chat %}
            <div class="msg">
                <b>{{msg.role}}:</b> {{msg.content}}
            </div>
        {% endfor %}
    </div>

    {% if not finished %}
    <form method="POST">
        <div class="input-area">
            <input type="text" name="user_input" placeholder="اكتب ردك هنا..." required>
            <button type="submit">إرسال</button>
        </div>
    </form>
    <br>
    <center>
        <form method="POST" action="/finish">
            <button type="submit" style="background: #ff4b2b; color: #fff; width: auto; padding: 10px 30px;">إنهاء المناظرة والحصول على التقييم 🏁</button>
        </form>
    </center>
    {% else %}
        <h2>📊 التقييم النهائي</h2>
        <div class="result">{{evaluation}}</div>
        <br>
        <center><a href="/reset">🔄 إعادة المناظرة</a></center>
    {% endif %}
</div>

</body>
</html>
"""


# ---------- Routes ---------- #

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session["username"] = request.form["username"]
        session["topic"] = request.form["topic"]
        session["chat"] = []
        session["turns"] = 0
        session["finished"] = False

        # --- AI يبدأ أولًا --- #
        opening_prompt = f"""
أنت ذكاء اصطناعي يقوم بدور محاور ومناظر ذكي ومحايد.

ابدأ مناظرة قصيرة مع المستخدم حول الموضوع التالي:
{session["topic"]}

قواعد المناظرة الصارمة التي يجب الالتزام بها في كل رد:

1) طول الرد:
- يجب أن يكون ردك من سطر إلى ثلاثة أسطر فقط، لا أكثر ولا أقل.

2) أسلوب النقاش:
- التزم بالموضوع بدقة.
- كن مرنًا في الحوار ولكن عميقًا في التحليل.
- اذا لم يكن لرد المستخدم صله في في الموضوع المحدد ترسل له رد تقول فيه ارجوا عدم الخروج عن الموضوع المحدد.
- اعتمد على التفكير المنطقي والنقدي وليس السطحي.

3) طريقة إنهاء كل رد (مهم جدًا):
في نهاية كل رد يجب أن تختار واحدة فقط من الطرق التالية، مع التناوب بينها في كل مرة:
- تطرح سؤالًا واحدًا مباشرًا.
- تطرح سؤالًا مع إعطاء خيارات للإجابة.
- تمنح المستخدم مساحة للتعبير عن رأيه بعبارة مثل: "أعطيك مساحة لتعبر عن رأيك وموقفك".

ولا تكرر نفس طريقة الإنهاء في ردّين متتاليين.

4) إذا طرح المستخدم سؤالًا:
- أجب عليه بإجابة منطقية وعميقة، ثم أكمل الحوار.

5) إذا كان رد المستخدم غير واضح، غير منطقي، متناقض، أو قصير جدًا:
- لا تكمل المناظرة مباشرة.
- اطلب منه توضيح فكرته أو إعادة صياغة رأيه بطريقة مفهومة ومنطقية قبل الاستمرار.

6) حافظ على أسلوب حوار محترم، عقلاني، ومحفّز للتفكير النقدي.

ابدأ المناظرة الآن.
"""

        first_reply = ai_reply(opening_prompt)

        session["chat"].append({"role": "AI", "content": first_reply})

        return redirect(url_for("chat"))

    return render_template_string(NAME_PAGE)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "username" not in session:
        return redirect(url_for("home"))

    if request.method == "POST" and not session["finished"]:
        user_input = request.form["user_input"]
        session["chat"].append({"role": "User", "content": user_input})
        session["turns"] += 1

        history = "\n".join([
            f"{m['role']}: {m['content']}"
            for m in session["chat"]
        ])

        prompt = f"""
أنت ذكاء اصطناعي يقوم بدور محاور ومناظر ذكي ومحايد.
الموضوع:
{session["topic"]}

سجل النقاش:
{history}

قواعد صارمة:

1) طول الرد:
- يجب أن يكون ردك من سطر إلى ثلاثة أسطر فقط، لا أكثر ولا أقل.

2) أسلوب النقاش:
- التزم بالموضوع بدقة.
- كن مرنًا في الحوار ولكن عميقًا في التحليل.
- اذا لم يكن لرد المستخدم صله في في الموضوع المحدد ترسل له رد تقول فيه ارجوا عدم الخروج عن الموضوع المحدد.
- اعتمد على التفكير المنطقي والنقدي وليس السطحي.

3) طريقة إنهاء كل رد (مهم جدًا):
في نهاية كل رد يجب أن تختار واحدة فقط من الطرق التالية، مع التناوب بينها في كل مرة:
- تطرح سؤالًا واحدًا مباشرًا.
- تطرح سؤالًا مع إعطاء خيارات للإجابة.
- تمنح المستخدم مساحة للتعبير عن رأيه بعبارة مثل: "أعطيك مساحة لتعبر عن رأيك وموقفك".

ولا تكرر نفس طريقة الإنهاء في ردّين متتاليين.

4) إذا طرح المستخدم سؤالًا:
- أجب عليه بإجابة منطقية وعميقة، ثم أكمل الحوار.

5) إذا كان رد المستخدم غير واضح، غير منطقي، متناقض، أو قصير جدًا:
- لا تكمل المناظرة مباشرة.
- اطلب منه توضيح فكرته أو إعادة صياغة رأيه بطريقة مفهومة ومنطقية قبل الاستمرار.

6) حافظ على أسلوب حوار محترم، عقلاني، ومحفّز للتفكير النقدي.

ردك:
"""
        reply = ai_reply(prompt)
        session["chat"].append({"role": "AI", "content": reply})

    return render_template_string(
        CHAT_PAGE,
        username=session["username"],
        topic=session["topic"],
        chat=session["chat"],
        finished=session["finished"],
        evaluation=session.get("evaluation", "")
    )

@app.route("/finish", methods=["POST"])
def finish():
    if "username" in session and not session["finished"]:
        session["chat"].append({
            "role": "AI",
            "content": "شكراً لمشاركتك، هذا تقييمي النهائي 👇"
        })
        session["evaluation"] = evaluate_debate(
            session["chat"],
            session["topic"]
        )
        session["finished"] = True
    return redirect(url_for("chat"))

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
