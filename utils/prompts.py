import click

def get_media_service_config(service_name, defaults):
    """Get configuration for media services (Sonarr, Radarr, etc.)"""
    click.echo(f"🔧 Configuring {service_name} deployment...")
    
    config = {}
    config['external_port'] = click.prompt('External port', default=defaults['port'], type=int)
    config['config_path'] = click.prompt('Config directory path', default=defaults['config_path'])
    config['puid'] = click.prompt('User ID (PUID)', default='1000')
    config['pgid'] = click.prompt('Group ID (PGID)', default='1000')
    config['timezone'] = click.prompt('Timezone', default='America/Chicago')
    config['image_tag'] = click.prompt('Image tag', default='latest')
    
    return config
