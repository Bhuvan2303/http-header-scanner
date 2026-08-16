from flask import Flask, request, jsonify, render_template
import urllib.request
from urllib.parse import urlparse

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Please enter a website URL."
        }), 400

    url = data.get("url", "").strip()

    # Empty URL
    if not url:
        return jsonify({
            "error": "Please enter a website URL."
        }), 400

    # Require HTTP or HTTPS
    if not url.startswith(("http://", "https://")):
        return jsonify({
            "error": "Invalid URL. Use a URL starting with http:// or https://"
        }), 400

    # Check that the URL contains a real hostname
    parsed = urlparse(url)

    if not parsed.hostname:
        return jsonify({
            "error": "Invalid URL. Enter a complete website address, such as https://example.com"
        }), 400

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

    except urllib.error.HTTPError as e:
        return jsonify({
            "error": f"Website returned HTTP {e.code}."
        }), 400

    except urllib.error.URLError:
        return jsonify({
            "error": "Unable to reach this website. Check the URL or try another website."
        }), 400

    except TimeoutError:
        return jsonify({
            "error": "The website took too long to respond."
        }), 400

    except Exception:
        return jsonify({
            "error": "The website could not be scanned. Please check the URL and try again."
        }), 400


if __name__ == "__main__":
    app.run()
