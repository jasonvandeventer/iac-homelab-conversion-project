import os
import subprocess
import click

PROWLARR_TF_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'terraform', 'prowlarr'))
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
def prowlarr():
    """Manage Prowlarr via Terraform"""
    pass

@prowlarr.command()
def deploy():
    """Deploy the Prowlarr container with interactive configuration"""
    click.echo("🔧 Configuring Prowlarr deployment...")

    external_port = click.prompt('External port', default=9696, type=int)
    config_path = click.prompt('Config directory path', default='/mnt/testconfigs/prowlarr')
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

    tfvars_path = f"{PROWLARR_TF_DIR}/terraform.tfvars"
    with open(tfvars_path, "w") as f:
        f.write(tfvars_content)

    click.echo("🚀 Deploying Prowlarr with Terraform...")

    try:
        subprocess.run(["terraform", "init"], cwd=PROWLARR_TF_DIR, check=True)
        subprocess.run(["terraform", "apply", "-auto-approve"], cwd=PROWLARR_TF_DIR, check=True)

        git_commit(f"Deployed Prowlarr on port {external_port} with tag {image_tag}")
        click.echo("✅ Prowlarr deployed successfully")
        
    except subprocess.CalledProcessError as e:
        git_commit(f"Failed to deploy Prowlarr - error code {e.returncode}")
        click.echo("❌ Deployment failed", fg="red")


@prowlarr.command()
def destroy():
    """Destroy the Prowlarr container"""
    click.echo("💣 Destroying Prowlarr...")

    try:
        subprocess.run(["terraform", "destroy", "-auto-approve"], cwd=PROWLARR_TF_DIR)

        git_commit("Destroyed Prowlarr successfully")
        click.echo("✅ Prowlarr destroyed successfully")

    except subprocess.CalledProcessError as e:
        git_commit(f"Failed to destroy Prowlarr - error code {e.returncode}")
        click.echo("❌ Destroy failed", fg="red")

@prowlarr.command()
def status():
    """Check if Prowlarr container is up"""
    result = subprocess.run(["docker", "ps", "--filter", "name=prowlarr", "--format", "{{.Names}}"], capture_output=True, text=True)

    if "prowlarr" in result.stdout:
        click.secho("✅ Prowlarr is up", fg="green")
    else:
        click.secho("❌ Prowlarr is down", fg="red")
