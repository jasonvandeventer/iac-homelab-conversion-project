terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

variable "external_port" {
  description = "External port for Bazarr"
  type = number
  default = 6767
}

variable "puid" {
  description = "User ID for Bazarr process"
  type = string
  default = "1000"
}

variable "pgid" {
  description = "Group ID for Bazarr process"
  type = string
  default = "1000"
}

variable "timezone" {
  description = "Timezone for Bazarr"
  type = string
  default = "America/Chicago"
}

variable "config_path" {
  description = "Host path for Bazarr config"
  type = string
  default = "/mnt/testconfigs/bazarr"
}

variable "image_tag" {
  description = "Bazarr image tag"
  type = string
  default = "latest"
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_image" "bazarr" {
  name = "lscr.io/linuxserver/bazarr:${var.image_tag}"
}

resource "docker_container" "bazarr" {
  image   = docker_image.bazarr.name
  name    = "bazarr"
  restart = "unless-stopped"
  env = ["PUID=${var.puid}", "PGID=${var.pgid}", "TZ=${var.timezone}"]

  ports {
    internal = 6767
    external = var.external_port
  }

  volumes {
    host_path      = var.config_path
    container_path = "/config"
  }
}
