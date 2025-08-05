import os
import subprocess
import click

SONARR_TF_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'terraform', 'sonarr'))

@click.group()
def sonarr():
    """Manage Sonarr via Terraform"""
    pass

@sonarr.command()
def deploy():
    """Deploy the Sonarr container"""
    click.echo("🚀 Deploying Sonarr with Terraform...")
    subprocess.run(["terraform", "init"], cwd=SONARR_TF_DIR)
    subprocess.run(["terraform", "apply", "-auto-approve"], cwd=SONARR_TF_DIR)

@sonarr.command()
def destroy():
    """Destroy the Sonarr container"""
    click.echo("💣 Destroying Sonarr...")
    subprocess.run(["terraform", "destroy", "-auto-approve"], cwd=SONARR_TF_DIR)

@sonarr.command()
def status():
    """Check if Sonarr container is up"""
    result = subprocess.run(["docker", "ps", "--filter", "name=sonarr", "--format", "{{.Names}}"], capture_output=True, text=True)
    if "sonarr" in result.stdout:
        click.secho("✅ Sonarr is up", fg="green")
    else:
        click.secho("❌ Sonarr is down", fg="red")
