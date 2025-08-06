terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

variable "external_port" {
  description = "External port for Sonarr"
  type = number
  default = 8989
}

variable "puid" {
  description = "User ID for Sonarr process"
  type = string
  default = "1000"
}

variable "pgid" {
  description = "Group ID for Sonarr process"
  type = string
  default = "1000"
}

variable "timezone" {
  description = "Timezone for Sonarr"
  type = string
  default = "America/Chicago"
}

variable "config_path" {
  description = "Host path for Sonarr config"
  type = string
  default = "/mnt/testconfigs/sonarr"
}

variable "image_tag" {
  description = "Sonarr image tag"
  type = string
  default = "latest"
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_image" "sonarr" {
  name = "lscr.io/linuxserver/sonarr:${var.image_tag}"
}

resource "docker_container" "sonarr" {
  image   = docker_image.sonarr.name
  name    = "sonarr"
  restart = "unless-stopped"
  env = ["PUID=${var.puid}", "PGID=${var.pgid}", "TZ=${var.timezone}"]

  ports {
    internal = 8989
    external = var.external_port
  }

  volumes {
    host_path      = var.config_path
    container_path = "/config"
  }
}
