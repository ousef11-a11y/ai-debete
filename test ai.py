import requests
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- Ollama AI ---------- #
def ai_reply(prompt):
    response = requests.post(
        "https://ollama.com/api/generate",
        json={
            "model": "gpt-oss:120b-cloud",
            "prompt": prompt,
            "stream": Falseimport requests
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- Ollama AI ---------- #
def ai_reply(prompt):
    response = requests.post(
        "https://ollama.com/api/generate",
        json={
            "model": "gpt-oss:120b-cloud",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json().get("response", "").strip()

def evaluate_debate(chat, topic):
    full_chat = "\n".join([f"{m['role']}: {m['content']}" for m in chat])
    prompt = f"""
أنت مقيم مناظرات محترف.
قيّم هذه المناظرة حول الموضوع:
{topic}

النقاش:
{full_chat}

أعطِ تقييم من 10 مع سبب مختصر من دون رموز غريبه ويمكن استخدام الاعشار في التقيم مثلا7.5 وهكذا .
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
أنت ذكاء اصطناعي ذكي.
ابدأ مناظرة قصيرة حول الموضوع التالي:
{session["topic"]}

قواعد صارمة:
- ان يكون كل رد من سطران الى اربع اسطر .
- التزم بالموضوع وكن مرن.
- لا تكرر الأفكار.
-في نهاية كل ردانت مخير بين ان تختم بسؤال واحد فقط أو تعطي سؤال مع تخيره بل اجابه بين خيارات تضعهاأو  تعطي مساحه للشخص بأن يعبر عن رأيه حيث تقول له اعطيك مساحه لتعبر عن رأيك وموقفك .
- على التفكير  ان يكون عميق وليس سطحي.

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
أنت ذكاء اصطناعي تناقش مستخدمًا.

الموضوع:
{session["topic"]}

سجل النقاش:
{history}

قواعد صارمة:
- ان يكون كل رد من سطران الى اربع اسطر .
- التزم بالموضوع وكن مرن.
- لا تكرر الأفكار.
-في نهاية كل ردانت مخير بين ان تختم بسؤال واحد فقط أو تعطي سؤال مع تخيره بل اجابه بين خيارات تضعهاأو  تعطي مساحه للشخص بأن يعبر عن رأيه حيث تقول له اعطيك مساحه لتعبر عن رأيك وموقفك .
- على التفكير  ان يكون عميق وليس سطحي.
ردك:
"""
        reply = ai_reply(prompt)
        session["chat"].append({"role": "AI", "content": reply})

        if session["turns"] > 4:
            session["chat"].append({
                "role": "AI",
                "content": "شكراً لمشاركتك، هذا تقييمي النهائي 👇"
            })
            session["evaluation"] = evaluate_debate(
                session["chat"],
                session["topic"]
            )
            session["finished"] = True

    return render_template_string(
        CHAT_PAGE,
        username=session["username"],
        topic=session["topic"],
        chat=session["chat"],
        finished=session["finished"],
        evaluation=session.get("evaluation", "")
    )

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

        }
    )
    return response.json().get("response", "").strip()

def evaluate_debate(chat, topic):
    full_chat = "\n".join([f"{m['role']}: {m['content']}" for m in chat])
    prompt = f"""
أنت مقيم مناظرات محترف.
قيّم هذه المناظرة حول الموضوع:
{topic}

النقاش:
{full_chat}

أعطِ تقييم من 10 مع سبب مختصر من دون رموز غريبه ويمكن استخدام الاعشار في التقيم مثلا7.5 وهكذا .
تقيمك يكون بل اعتماد على:مدى التعمق بالنقاش و طول جواب المستخدم وفهمه للأسءلة واسوب تفكيره وما الى ذاك.
عليك انت تكون صارم في التقيم بدون مراعات.
"""
    return ai_reply(prompt)

# ---------- HTML ---------- #

NAME_PAGE = """
<h2>🧠 AI Debate Arena</h2>
<form method="POST">
    <label>اسمك:</label><br>
    <input name="username" required><br><br>

    <label>موضوع المناظرة:</label><br>
    <input name="topic" required style="width:300px;"><br><br>

    <button type="submit">ابدأ المناظرة</button>
</form>
"""

CHAT_PAGE = """
<h2>👤 {{username}}</h2>
<h3>📌 الموضوع: {{topic}}</h3>

<div style="border:1px solid black;padding:10px;height:300px;overflow:auto;">
{% for msg in chat %}
<p><b>{{msg.role}}:</b> {{msg.content}}</p>
{% endfor %}
</div>

{% if not finished %}
<form method="POST">
    <input name="user_input" style="width:80%;" required>
    <button type="submit">إرسال</button>
</form>
{% else %}
<h2>📊 التقييم النهائي</h2>
<p>{{evaluation}}</p>
<a href="/reset">إعادة</a>
{% endif %}
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
أنت ذكاء اصطناعي ذكي.
ابدأ مناظرة قصيرة حول الموضوع التالي:
{session["topic"]}

قواعد صارمة:
- ان يكون كل رد من سطران الى اربع اسطر .
- التزم بالموضوع وكن مرن.
- لا تكرر الأفكار.
-في نهاية كل ردانت مخير بين ان تختم بسؤال واحد فقط أو تعطي سؤال مع تخيره بل اجابه بين خيارات تضعهاأو  تعطي مساحه للشخص بأن يعبر عن رأيه حيث تقول له اعطيك مساحه لتعبر عن رأيك وموقفك .
- على التفكير  ان يكون عميق وليس سطحي.

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
أنت ذكاء اصطناعي تناقش مستخدمًا.

الموضوع:
{session["topic"]}

سجل النقاش:
{history}

قواعد صارمة:
- ان يكون كل رد من سطران الى اربع اسطر .
- التزم بالموضوع وكن مرن.
- لا تكرر الأفكار.
-في نهاية كل ردانت مخير بين ان تختم بسؤال واحد فقط أو تعطي سؤال مع تخيره بل اجابه بين خيارات تضعهاأو  تعطي مساحه للشخص بأن يعبر عن رأيه حيث تقول له اعطيك مساحه لتعبر عن رأيك وموقفك .
- على التفكير  ان يكون عميق وليس سطحي.
ردك:
"""
        reply = ai_reply(prompt)
        session["chat"].append({"role": "AI", "content": reply})

        if session["turns"] > 4:
            session["chat"].append({
                "role": "AI",
                "content": "شكراً لمشاركتك، هذا تقييمي النهائي 👇"
            })
            session["evaluation"] = evaluate_debate(
                session["chat"],
                session["topic"]
            )
            session["finished"] = True

    return render_template_string(
        CHAT_PAGE,
        username=session["username"],
        topic=session["topic"],
        chat=session["chat"],
        finished=session["finished"],
        evaluation=session.get("evaluation", "")
    )

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

