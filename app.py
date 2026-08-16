from flask import Flask, request, jsonify, render_template
import urllib.request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        response = urllib.request.urlopen(url, timeout=10)

        security_headers = {
            "Strict-Transport-Security": "Forces HTTPS",
            "Content-Security-Policy": "Controls browser resources",
            "X-Content-Type-Options": "Prevents MIME sniffing",
            "X-Frame-Options": "Helps prevent clickjacking"
        }

        results = {}

        for header, purpose in security_headers.items():
            results[header] = {
                "found": header in response.headers,
                "purpose": purpose
            }

        return jsonify({
            "url": url,
            "status": response.status,
            "headers": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run()