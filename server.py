from flask import Flask, request, jsonify
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

def run_llama(query):
    """Runs the Llama 3.1 LLM with the given query and returns the response."""
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.1"],
            input=query,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error while running Llama 3.1: {e}"

@app.route("/", methods=["POST"])
def analyze_code():
    """Handle POST requests for code analysis."""
    data = request.get_json()
    code_snippet = data.get("code", "")

    if not code_snippet:
        return jsonify({"error": "No code snippet provided"}), 400

    query = f"""
    You are an Automated Code Analysis System. Analyze the following code snippet:
    1. Readability test
    2. Complexity
    3. Naming conventions
    4. Error handling
    5. Duplication
    6. Formatting
    7. Private key detection
    Provide suggestions for improvement.

    Code snippet:
    {code_snippet}
    """
    response = run_llama(query)

    return jsonify({"report": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)  # Runs on all IPs
