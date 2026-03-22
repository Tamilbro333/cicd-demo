from flask import Flask, jsonify, render_template
import datetime
import os
import psutil
import requests
import docker

app = Flask(__name__)

# Attempt to configure docker client
try:
    docker_client = docker.from_env()
except:
    docker_client = None

GITHUB_REPO = os.getenv('GITHUB_REPO', 'rdtamilselvan/cicd-demo')

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/api/metadata')
def metadata():
    return jsonify({
        "app": "My CI/CD Pipeline Project",
        "version": "Live 1.2",
        "deployed_by": "GitHub Actions",
        "repo": GITHUB_REPO
    })

@app.route('/api/stats')
def stats():
    # Hardware stats inside container/host
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent

    # Real AWS EC2 Fetch (via IMDSv2)
    aws_region = "Local Environment (Not AWS)"
    aws_instance = "N/A"
    try:
        token_headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
        token_req = requests.put("http://169.254.169.254/latest/api/token", headers=token_headers, timeout=0.5)
        if token_req.status_code == 200:
            token = token_req.text
            meta_headers = {"X-aws-ec2-metadata-token": token}
            doc_req = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document", headers=meta_headers, timeout=0.5)
            if doc_req.status_code == 200:
                aws_data = doc_req.json()
                aws_region = aws_data.get('region', aws_region)
                aws_instance = aws_data.get('instanceType', aws_instance)
    except Exception:
        pass

    return jsonify({
        "cpu_usage": cpu,
        "ram_usage": ram,
        "aws_region": aws_region,
        "aws_instance": aws_instance
    })

@app.route('/api/github')
def github_stats():
    # Fetch real live data from GitHub Actions API
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs?per_page=1"
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('workflow_runs'):
                run = data['workflow_runs'][0]
                return jsonify({
                    "success": True,
                    "status": run.get('status', 'unknown'),
                    "conclusion": run.get('conclusion', 'in-progress'),
                    "branch": run.get('head_branch', 'unknown'),
                    "commit_msg": run['head_commit']['message'].split('\n')[0],
                    "commit_sha": run.get('head_sha', '')[:7],
                    "html_url": run.get('html_url', '#')
                })
    except Exception as e:
        pass

    return jsonify({
        "success": False,
        "status": "API unreachable",
        "conclusion": "unknown",
        "branch": "main",
        "commit_msg": "N/A",
        "commit_sha": "N/A",
        "html_url": "#"
    })

@app.route('/api/docker')
def docker_logs():
    # Fetch real docker container logs using docker socket
    logs = "Docker socket not mounted. Cannot read container logs."
    status = "Unknown"
    
    if docker_client:
        try:
            container = docker_client.containers.get('cicd-app')
            raw_logs = container.logs(tail=20).decode('utf-8')
            logs = raw_logs if raw_logs.strip() else "Container running, no logs generated yet."
            status = container.status
        except docker.errors.NotFound:
            logs = "Container 'cicd-app' not found on this daemon."
        except Exception as e:
            logs = f"Error reading logs: {str(e)}"
    
    return jsonify({
        "status": status,
        "logs": logs
    })

@app.route('/health')
def health():
    return jsonify({
        "healthy": True,
        "timestamp": str(datetime.datetime.now())
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
