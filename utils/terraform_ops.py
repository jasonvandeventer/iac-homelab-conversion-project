import os
import subprocess
import click

def git_commit(message, iac_root):
    """Helper function to commit changes"""
    try:
        subprocess.run(["git", "add", "."], cwd=iac_root, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=iac_root, check=True)
        click.echo(f"📝 Committed: {message}")
    except subprocess.CalledProcessError:
        click.echo("⚠️  Git commit failed (maybe no changes)"))

def write_tfvars(tf_dir, tfvars_data):
    """Write Terraform variables to file"""
    tfvars_path = f"{tf_dir}/terraform.tfvars"

    # Convert dict to HCL format
    tfvars_content = ""
    for key, value in tfvars_data.items():
        if isinstance(value, str):
            tfvars_content += f'{key} = "{value}"\n'
        else:
            tfvars_content += f'{key} = {value}\n'

    with open(tfvars_path, "w") as f:
        f.write(tfvars_content)

def terraform_deploy(service_name, tf_dir, iac_root):
    """Execute Terraform deployment"""
    click.echo(f"🚀 Deploying {service_name} with Terraform...")

    try:
        subprocess.run(["terraform", "init"], cwd=tf_dir, check=True)
        subprocess.run(["terraform", "apply", "-auto-approve"], cwd=tf_dir, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def terraform_destroy(service_name, tf_dir, iac_root):
    """Execute Terraform destroy"""
    click.echo(f"💥 Destroying {service_name}...")

    try:
        subprocess.run(["terraform", "destroy", "-auto-approve"], cwd=tf_dir, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def docker_status_check(container_name):
    """Check if Docker container is running"""
    result = subprocess.run(
        ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    return container_name in result.stdout


