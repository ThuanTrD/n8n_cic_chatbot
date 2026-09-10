#!/usr/bin/env python3
import subprocess, re, os, sys, time

ENV_FILE = "/opt/n8n/.env"
COMPOSE_FILE = "/opt/n8n/compose.yaml"

def get_current_tunnel():
    try:
        res = subprocess.run(
            ["journalctl", "-u", "cloudflared-n8n", "--no-pager", "-n", "100"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False
        )
        matches = re.findall(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", res.stdout)
        if matches:
            return matches[-1].rstrip("/") + "/"
    except Exception as e:
        sys.stderr.write(f"Error reading journal: {e}\n")
    return None

def get_env_url():
    if not os.path.exists(ENV_FILE):
        return None
    try:
        with open(ENV_FILE, "r") as f:
            for line in f:
                if line.startswith("N8N_WEBHOOK_URL="):
                    return line.strip().split("=", 1)[1].strip()
    except Exception as e:
        sys.stderr.write(f"Error reading env: {e}\n")
    return None

def update_env_and_n8n(new_url):
    print(f"Updating n8n webhook URL to: {new_url}")
    lines = []
    with open(ENV_FILE, "r") as f:
        for line in f:
            if line.startswith("N8N_WEBHOOK_URL="):
                lines.append(f"N8N_WEBHOOK_URL={new_url}\n")
            elif line.startswith("N8N_EDITOR_BASE_URL="):
                lines.append(f"N8N_EDITOR_BASE_URL={new_url}\n")
            elif line.startswith("WEBHOOK_URL="):
                lines.append(f"WEBHOOK_URL={new_url}\n")
            else:
                lines.append(line)
    
    with open(ENV_FILE, "w") as f:
        f.writelines(lines)
    
    print("Recreating n8n container with new webhook URL...")
    subprocess.run(["docker", "compose", "-f", COMPOSE_FILE, "up", "-d"], check=False)
    print("n8n synchronized successfully.")

def check_sync():
    tunnel_url = get_current_tunnel()
    if not tunnel_url:
        return
    current_env = get_env_url()
    if not current_env or current_env.rstrip("/") != tunnel_url.rstrip("/"):
        update_env_and_n8n(tunnel_url)
    else:
        print(f"Webhook URL is up-to-date: {current_env}")

if __name__ == "__main__":
    check_sync()
