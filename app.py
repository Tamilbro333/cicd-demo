from flask import Flask, jsonify
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "CI/CD Pipeline Demo",
        "status": "running",
        "version": "1.0.0",
        "deployed_by": "GitHub Actions"
    })

@app.route('/health')
def health():
    return jsonify({
        "healthy": True,
        "timestamp": str(datetime.datetime.now())
    })

@app.route('/info')
def info():
    return jsonify({
        "app": "Cloud Destinations Demo",
        "tech_stack": ["Python", "Flask", "Docker", "GitHub Actions", "AWS"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)