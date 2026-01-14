terraform {
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.53.0"
    }
  }
}

# Empty provider block tells Terraform to use your OS_ variables
provider "openstack" {}

# Create the Ubuntu VM
resource "openstack_compute_instance_v2" "vm_nginx" {
  name            = "ubuntu-nginx-terraform"
  image_name      = "Ubuntu-20.04"
  flavor_name     = "m1.lean"
  key_pair        = "test"
  security_groups = ["default"]

  network {
    name = "safe-net"
  }
}

# Output the IP address
output "ip_internal" {
  value = openstack_compute_instance_v2.vm_nginx.network.0.fixed_ip_v4
}
