import os
import subprocess
import click

BAZARR_TF_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'terraform', 'bazarr'))
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
def bazarr():
    """Manage Bazarr via Terraform"""
    pass

@bazarr.command()
def deploy():
    """Deploy the Bazarr container with interactive configuration"""
    click.echo("🔧 Configuring Bazarr deployment...")

    external_port = click.prompt('External port', default=6767, type=int)
    config_path = click.prompt('Config directory path', default='/mnt/testconfigs/bazarr')
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

    tfvars_path = f"{BAZARR_TF_DIR}/terraform.tfvars"
    with open(tfvars_path, "w") as f:
        f.write(tfvars_content)

    click.echo("🚀 Deploying Bazarr with Terraform...")

    try:
        subprocess.run(["terraform", "init"], cwd=BAZARR_TF_DIR, check=True)
        subprocess.run(["terraform", "apply", "-auto-approve"], cwd=BAZARR_TF_DIR, check=True)

        git_commit(f"Deployed Bazarr on port {external_port} with tag {image_tag}")
        click.echo("✅ Bazarr deployed successfully")
        
    except subprocess.CalledProcessError as e:
        git_commit(f"Failed to deploy Bazarr - error code {e.returncode}")
        click.echo("❌ Deployment failed", fg="red")


@bazarr.command()
def destroy():
    """Destroy the Bazarr container"""
    click.echo("💣 Destroying Bazarr...")

    try:
        subprocess.run(["terraform", "destroy", "-auto-approve"], cwd=BAZARR_TF_DIR)

        git_commit("Destroyed Bazarr successfully")
        click.echo("✅ Bazarr destroyed successfully")

    except subprocess.CalledProcessError as e:
        git_commit(f"Failed to destroy Bazarr - error code {e.returncode}")
        click.echo("❌ Destroy failed", fg="red")

@bazarr.command()
def status():
    """Check if Bazarr container is up"""
    result = subprocess.run(["docker", "ps", "--filter", "name=bazarr", "--format", "{{.Names}}"], capture_output=True, text=True)

    if "bazarr" in result.stdout:
        click.secho("✅ Bazarr is up", fg="green")
    else:
        click.secho("❌ Bazarr is down", fg="red")
