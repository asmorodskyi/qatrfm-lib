variable "count" {
    default = "2"
}

variable "network" {
}

variable "image" {
}

variable "basename" {
}

provider "libvirt" {
     uri = "qemu:///system"
}

resource "libvirt_volume" "myvdisk" {
  name = "qatrfm-vdisk-${var.basename}-${count.index}.qcow2"
  count = "${var.count}"
  pool = "default"
  source = "${var.image}"
  format = "qcow2"
}

resource "libvirt_network" "my_net" {
   name = "qatrfm-net-${var.basename}"
   addresses = ["${var.network}"]
   dhcp {
		enabled = false
	}
}

resource "libvirt_domain" "domain-sle" {
  name = "qatrfm-vm-${var.basename}-${count.index}"
  memory = "2048"
  vcpu = 2
  count = "${var.count}"

  network_interface {
    network_id = "${libvirt_network.my_net.id}"
    wait_for_lease = false
    addresses = ["0.0.0.0"]
  }

  network_interface {
    network_id = "${libvirt_network.my_net.id}"
    wait_for_lease = false
    addresses = ["0.0.0.0"]
  }

  disk {
   volume_id = "${libvirt_volume.myvdisk.*.id[count.index]}"
  }

  console {
    type        = "pty"
    target_port = "0"
    target_type = "serial"
  }

  console {
      type        = "pty"
      target_type = "virtio"
      target_port = "1"
  }

  graphics {
    type = "vnc"
    listen_type = "address"
    autoport = "true"
  }
}

output "domain_ips" {
    value = "${libvirt_domain.domain-sle.*.network_interface.0.addresses}"
}

output "domain_names" {
    value = "${libvirt_domain.domain-sle.*.name}"
}
