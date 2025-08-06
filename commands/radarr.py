import os
import subprocess
import click

RADARR_TF_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'terraform', 'radarr'))
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
def radarr():
    """Manage Radarr via Terraform"""
    pass

@radarr.command()
def deploy():
    """Deploy the Radarr container with interactive configuration"""
    click.echo("🔧 Configuring Radarr deployment...")

    external_port = click.prompt('External port', default=7878, type=int)
    config_path = click.prompt('Config directory path', default='/mnt/testconfigs/radarr')
    puid = click.prompt('User ID (PUID)', default='1000')
    pgid = click.prompt('Group ID (PGID)', default='1000')
    timezone = click.prompt('Timezone', default='America/Chicago')
    image_tag = click.prompt('Image tag', default='latest')

    tfvars_content = f'''external_port = {external_port}
config_path = "{config_path}"
puid = "{puid}"
pgid = "{pgid}"
timezone = "{timezone}"
image_tag = "{image_tag}"
'''

    tfvars_path = f"{RADARR_TF_DIR}/terraform.tfvars"
    with open(tfvars_path, "w") as f:
        f.write(tfvars_content)

    click.echo("🚀 Deploying Radarr with Terraform...")

    try:
        subprocess.run(["terraform", "init"], cwd=RADARR_TF_DIR, check=True)
        subprocess.run(["terraform", "apply", "-auto-approve"], cwd=RADARR_TF_DIR, check=True)

        git_commit(f"Deployed Radarr on port {external_port} with tag {image_tag}")
        click.echo("✅ Radarr deployed successfully")
        
    except subprocess.CalledProcessError as e:
        git_commit(f"Failed to deploy Radarr - error code {e.returncode}")
        click.echo("❌ Deployment failed", fg="red")


@radarr.command()
def destroy():
    """Destroy the Radarr container"""
    click.echo("💣 Destroying Radarr...")

    try:
        subprocess.run(["terraform", "destroy", "-auto-approve"], cwd=RADARR_TF_DIR)

        git_commit("Destroyed Radarr successfully")
        click.echo("✅ Radarr destroyed successfully")

    except subprocess.CalledProcessError as e:
        git_commit(f"Failed to destroy Radarr - error code {e.returncode}")
        click.echo("❌ Destroy failed", fg="red")

@radarr.command()
def status():
    """Check if Radarr container is up"""
    result = subprocess.run(["docker", "ps", "--filter", "name=radarr", "--format", "{{.Names}}"], capture_output=True, text=True)

    if "radarr" in result.stdout:
        click.secho("✅ Radarr is up", fg="green")
    else:
        click.secho("❌ Radarr is down", fg="red")
