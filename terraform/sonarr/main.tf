terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_image" "sonarr" {
  name = "lscr.io/linuxserver/sonarr:latest"
}

resource "docker_container" "sonarr" {
  image   = docker_image.sonarr.name
  name    = "sonarr"
  restart = "unless-stopped"
  env = ["PUID=1000", "PGID=1000", "TZ=America/Chicago"]

  ports {
    internal = 8989
    external = 8989
  }

  volumes {
    host_path      = "/mnt/testconfigs/sonarr"
    container_path = "/config"
  }
}
