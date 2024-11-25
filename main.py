from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://openai-devsdocode.up.railway.app"

@app.route('/v1/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(endpoint):
    # Forward request headers and data
    headers = {key: value for key, value in request.headers if key != 'Host'}
    data = request.get_json(silent=True) or request.form or request.data

    # Construct the target URL
    target_url = f"{BASE_URL}/{endpoint}"

    # Forward the request
    try:
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            params=request.args,
            data=data
        )
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
