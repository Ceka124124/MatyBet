from flask import Flask, request, render_template_string, redirect
import requests
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Telegram bot bilgileri
TOKEN = "8189840347:AAE4-PmjNNoH89mke55VnAgJmsrK_4drYe4"
CHAT_ID = "7755042636"

HTML_FORM = '''
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <title>Şikayət Formu</title>
  <style>
    body {
      font-family: sans-serif;
      background: linear-gradient(#000428, #004e92);
      color: white;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    form {
      background: rgba(0, 0, 0, 0.6);
      padding: 30px;
      border-radius: 15px;
      width: 400px;
      box-shadow: 0 0 15px rgba(0,0,0,0.5);
    }
    h2 {
      text-align: center;
      margin-bottom: 15px;
    }
    input, textarea {
      width: 100%;
      margin-bottom: 15px;
      padding: 10px;
      border: none;
      border-radius: 10px;
      outline: none;
    }
    input[type="submit"] {
      background: white;
      color: black;
      font-weight: bold;
      cursor: pointer;
    }
    label {
      font-size: 14px;
    }
  </style>
</head>
<body>
  <form method="POST" enctype="multipart/form-data">
    <h2>Şikayət</h2>
    <input type="text" name="your_username" placeholder="Senin Username" required>
    <input type="text" name="target_username" placeholder="Username (şikayet edilen)" required>
    <textarea name="info" placeholder="Bilgiler" required></textarea>
    <textarea name="complaint" placeholder="Şikayetin" required></textarea>
    <label>Resim (isteğe bağlı):</label>
    <input type="file" name="image">
    <input type="submit" value="Gönder">
  </form>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        your_username = request.form.get("your_username")
        target_username = request.form.get("target_username")
        info = request.form.get("info")
        complaint = request.form.get("complaint")
        message = (
    "🔔 *Yeni Şikayət Bildirimi*\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "👤 *Şikayətçi:* " + f"`{your_username}`\n"
    "🎯 *Hedef Kullanıcı:* " + f"`{target_username}`\n"
    "📄 *Bilgiler:*\n" + f"{info}\n"
    "🚨 *Şikayət Nedeni:*\n" + f"{complaint}\n"
    "━━━━━━━━━━━━━━━━━━━━━━"
)

        image = request.files.get("image")
        if image and image.filename:
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            image.save(filepath)

            with open(filepath, "rb") as photo:
                requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
                    data={
                        "chat_id": CHAT_ID,
                        "caption": message,
                        "parse_mode": "Markdown"
                    },
                    files={"photo": photo}
                )
            os.remove(filepath)
        else:
            requests.get(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                params={
                    "chat_id": CHAT_ID,
                    "text": message,
                    "parse_mode": "Markdown"
                }
            )
        return "<h2 style='text-align:center;color:lime;'>Şikayet başarıyla gönderildi.</h2>"

    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
