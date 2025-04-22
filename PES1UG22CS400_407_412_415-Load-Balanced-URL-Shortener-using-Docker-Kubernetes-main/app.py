from flask import Flask, request, redirect, render_template_string
import random, string

app = Flask(__name__)
url_mapping = {}

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    if request.method == 'POST':
        long_url = request.form.get("long_url")
        short_code = generate_short_code()
        url_mapping[short_code] = long_url
        short_url = f"http://localhost:5000/{short_code}"

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>URL Shortener</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background-color: #F1EFEC;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .box {
                background-color: #D4C9BE;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.1);
                text-align: center;
                width: 100%;
                max-width: 500px;
                border: 2px solid #123458;
            }
            h2 {
                margin-bottom: 20px;
                color: #123458;
            }
            input[type=text] {
                width: 80%;
                padding: 12px;
                margin-bottom: 15px;
                border: 1px solid #030303;
                border-radius: 6px;
                font-size: 16px;
                background-color: #F1EFEC;
                color: #030303;
            }
            button {
                padding: 10px 20px;
                background-color: #123458;
                color: #F1EFEC;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #0e2c4d;
            }
            .short-url {
                margin-top: 20px;
                font-size: 18px;
                color: #030303;
            }
            .short-url a {
                color: #123458;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>🔗 URL Shortener</h2>
            <form method="POST">
                <input type="text" name="long_url" placeholder="Paste your long URL here..." required>
                <br>
                <button type="submit">Shorten URL</button>
            </form>

            {% if short_url %}
            <div class="short-url">
                <p>Here is your short URL:</p>
                <a href="{{ short_url }}" target="_blank">{{ short_url }}</a>
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    ''', short_url=short_url)

@app.route('/<short_code>')
def redirect_url(short_code):
    long_url = url_mapping.get(short_code)
    if long_url:
        return redirect(long_url)
    return "<h3 style='color:#123458; text-align:center;'>URL not found 😢</h3>", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
