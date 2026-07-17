#!/usr/bin/env python3
"""
Installs Docker (if missing) for the current OS, waits for the Docker
daemon to be ready, then runs the project via `docker compose up --build`.

Usage:
    python3 scripts/setup_and_run.py
"""
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run(cmd, **kwargs):
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, check=True, **kwargs)


def docker_installed():
    return shutil.which("docker") is not None


def docker_daemon_ready():
    try:
        subprocess.run(
            ["docker", "info"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_linux():
    print("Installing Docker Engine via the official convenience script (needs sudo)...")
    run(["curl", "-fsSL", "https://get.docker.com", "-o", "/tmp/get-docker.sh"])
    run(["sudo", "sh", "/tmp/get-docker.sh"])

    print("Adding current user to the 'docker' group so you can run docker without sudo...")
    try:
        run(["sudo", "usermod", "-aG", "docker", subprocess.getoutput("whoami")])
        print(
            "NOTE: group membership only takes effect in a new shell session. "
            "If 'docker info' fails below, log out/in (or run 'newgrp docker') and re-run this script."
        )
    except subprocess.CalledProcessError:
        pass

    print("Starting the Docker service...")
    try:
        run(["sudo", "systemctl", "enable", "--now", "docker"])
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Could not start docker via systemctl — start the Docker service manually if needed.")


def install_macos():
    if shutil.which("brew") is None:
        sys.exit(
            "Homebrew is required to auto-install Docker Desktop on macOS.\n"
            "Install Homebrew first: https://brew.sh\n"
            "Or install Docker Desktop manually: https://www.docker.com/products/docker-desktop/"
        )
    print("Installing Docker Desktop via Homebrew...")
    run(["brew", "install", "--cask", "docker"])

    print("Launching Docker Desktop (first launch may prompt for permissions)...")
    run(["open", "-a", "Docker"])
    print("Waiting for Docker Desktop to finish starting — this can take a minute...")


def install_windows():
    if shutil.which("winget"):
        print("Installing Docker Desktop via winget...")
        run(["winget", "install", "--id", "Docker.DockerDesktop", "-e", "--source", "winget"])
    elif shutil.which("choco"):
        print("Installing Docker Desktop via Chocolatey...")
        run(["choco", "install", "docker-desktop", "-y"])
    else:
        sys.exit(
            "Neither winget nor choco is available to auto-install Docker Desktop.\n"
            "Install it manually: https://www.docker.com/products/docker-desktop/"
        )

    print("Launching Docker Desktop...")
    try:
        run(["cmd", "/c", "start", "", "Docker Desktop"])
    except subprocess.CalledProcessError:
        print("Could not auto-launch Docker Desktop — start it manually from the Start menu.")
    print("Waiting for Docker Desktop to finish starting — this can take a minute...")


def install_docker():
    system = platform.system()
    if system == "Linux":
        install_linux()
    elif system == "Darwin":
        install_macos()
    elif system == "Windows":
        install_windows()
    else:
        sys.exit(f"Unsupported OS: {system}. Install Docker manually: https://docs.docker.com/get-docker/")


def wait_for_daemon(timeout_seconds=180):
    print("Waiting for the Docker daemon to be ready...")
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if docker_daemon_ready():
            print("Docker daemon is ready.")
            return
        time.sleep(3)
    sys.exit(
        "Timed out waiting for the Docker daemon.\n"
        "Make sure Docker Desktop is running (macOS/Windows) or the docker service is active (Linux), "
        "then re-run this script."
    )


def run_project():
    print("Starting the project with docker compose...")
    run(["docker", "compose", "up", "--build"], cwd=REPO_ROOT)


def main():
    if not docker_installed():
        print("Docker not found — installing...")
        install_docker()
    else:
        print("Docker is already installed.")

    if not docker_daemon_ready():
        wait_for_daemon()

    run_project()


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(f"Command failed with exit code {exc.returncode}: {exc}")
    except KeyboardInterrupt:
        sys.exit("\nInterrupted.")
