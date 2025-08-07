terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

variable "external_port" {
  description = "External port for Prowlarr"
  type = number
  default = 9696
}

variable "puid" {
  description = "User ID for Prowlarr process"
  type = string
  default = "1000"
}

variable "pgid" {
  description = "Group ID for Prowlarr process"
  type = string
  default = "1000"
}

variable "timezone" {
  description = "Timezone for Prowlarr"
  type = string
  default = "America/Chicago"
}

variable "config_path" {
  description = "Host path for Prowlarr config"
  type = string
  default = "/mnt/testconfigs/prowlarr"
}

variable "image_tag" {
  description = "Prowlarr image tag"
  type = string
  default = "latest"
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_image" "prowlarr" {
  name = "lscr.io/linuxserver/prowlarr:${var.image_tag}"
}

resource "docker_container" "prowlarr" {
  image   = docker_image.prowlarr.name
  name    = "prowlarr"
  restart = "unless-stopped"
  env = ["PUID=${var.puid}", "PGID=${var.pgid}", "TZ=${var.timezone}"]

  ports {
    internal = 9696
    external = var.external_port
  }

  volumes {
    host_path      = var.config_path
    container_path = "/config"
  }
}
