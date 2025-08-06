terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

variable "external_port" {
  description = "External port for Radarr"
  type = number
  default = 7878
}

variable "puid" {
  description = "User ID for Radarr process"
  type = string
  default = "1000"
}

variable "pgid" {
  description = "Group ID for Radarr process"
  type = string
  default = "1000"
}

variable "timezone" {
  description = "Timezone for Radarr"
  type = string
  default = "America/Chicago"
}

variable "config_path" {
  description = "Host path for Radarr config"
  type = string
  default = "/mnt/testconfigs/radarr"
}

variable "image_tag" {
  description = "Radarr image tag"
  type = string
  default = "latest"
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_image" "radarr" {
  name = "lscr.io/linuxserver/radarr:${var.image_tag}"
}

resource "docker_container" "radarr" {
  image   = docker_image.radarr.name
  name    = "radarr"
  restart = "unless-stopped"
  env = ["PUID=${var.puid}", "PGID=${var.pgid}", "TZ=${var.timezone}"]

  ports {
    internal = 7878
    external = var.external_port
  }

  volumes {
    host_path      = var.config_path
    container_path = "/config"
  }
}
