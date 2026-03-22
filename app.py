from flask import Flask, jsonify, render_template
import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('dashboard.html')


@app.route('/api/metadata')
def metadata():
    commit_sha = os.getenv('GITHUB_SHA', 'local-dev')

    return jsonify({
        "app": "Cloud Destinations Demo",
        "version": "1.0.1",
        "branch": os.getenv('GITHUB_REF_NAME', 'main'),
        "commit_sha": commit_sha,
        "commit_sha_short": commit_sha[:7],
        "deployed_by": "GitHub Actions"
    })


@app.route('/api/workflow-status')
def workflow_status():
    # Without GitHub API auth in this demo, pipeline stages reflect known runtime state.
    return jsonify({
        "tests": "Passed",
        "tests_ok": True,
        "docker_build": "Image Running",
        "docker_build_ok": True,
        "aws_deploy": "Live on EC2",
        "aws_deploy_ok": True,
        "last_checked": str(datetime.datetime.now())
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