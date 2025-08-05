import os
import subprocess
import click

SONARR_TF_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'terraform', 'sonarr'))
IAC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def git_commit(message):
    """Helper function to commit changes."""
    try:
        subprocess.run(["git", "add", "."], cwd=IAC_ROOT, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=IAC_ROOT, check=True)
        click.echo(f"📝 Committed: {message}")
    except subprocess.CalledProcessError:
        click.echo("⚠️  Git commit failed (maybe no changes)")


@click.group()
def sonarr():
    """Manage Sonarr via Terraform"""
    pass

@sonarr.command()
def deploy():
    """Deploy the Sonarr container"""
    click.echo("🚀 Deploying Sonarr with Terraform...")

    try:
        subprocess.run(["terraform", "init"], cwd=SONARR_TF_DIR, check=True)
        subprocess.run(["terraform", "apply", "-auto-approve"], cwd=SONARR_TF_DIR, check=True)

        git_commit("Deployed Sonarr successfully")
        click.echo("✅ Sonarr deployed successfully")

    except subprocess.CalledProcessError as e:
        git_commit(f"Failed to deploy Sonarr - error code {e.returncode}")
        click.echo("❌ Deployment failed", fg="red")

@sonarr.command()
def destroy():
    """Destroy the Sonarr container"""
    click.echo("💣 Destroying Sonarr...")

    try:
        subprocess.run(["terraform", "destroy", "-auto-approve"], cwd=SONARR_TF_DIR)

        git_commit("Destroyed Sonarr successfully")
        click.echo("✅ Sonarr destroyed successfully")

    except subprocess.CalledProcessError as e:
        git_commit(f"Failed to destroy Sonarr - error code {e.returncode}")
        click.echo("❌ Destroy failed", fg="red")

@sonarr.command()
def status():
    """Check if Sonarr container is up"""
    result = subprocess.run(["docker", "ps", "--filter", "name=sonarr", "--format", "{{.Names}}"], capture_output=True, text=True)

    if "sonarr" in result.stdout:
        click.secho("✅ Sonarr is up", fg="green")
    else:
        click.secho("❌ Sonarr is down", fg="red")
