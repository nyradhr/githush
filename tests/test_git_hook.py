import os
import subprocess
import tempfile
from githush.scan import install_pre_commit_hook

def test_pre_commit_hook_blocks_secrets():
    with tempfile.TemporaryDirectory() as repo_dir:
        subprocess.run(["git", "init", repo_dir], check=True)

        install_pre_commit_hook(repo_dir)

        clean_file = os.path.join(repo_dir, "clean.txt")
        with open(clean_file, "w") as f:
            f.write("This is a safe file.")

        subprocess.run(["git", "-C", repo_dir, "add", "clean.txt"], check=True)
        commit_result = subprocess.run(
            ["git", "-C", repo_dir, "commit", "-m", "Safe commit"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert commit_result.returncode == 0

        secret_file = os.path.join(repo_dir, "secrets.txt")
        with open(secret_file, "w") as f:
            f.write("password: hunter2")

        subprocess.run(["git", "-C", repo_dir, "add", "secrets.txt"], check=True)
        secret_commit_result = subprocess.run(
            ["git", "-C", repo_dir, "commit", "-m", "Unsafe commit"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        assert secret_commit_result.returncode != 0
        assert b"Commit blocked due to detected secrets" in secret_commit_result.stderr