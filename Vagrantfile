# -*- mode: ruby -*-
# vi: set ft=ruby :

$network_interface = `sudo iw dev | awk '$1=="Interface"{print $2}'`.strip
$subnet = `ip -4 addr show $network_interface | awk '/inet 192.168./{split($2,a,"."); print a[3]}'`.strip

Vagrant.configure("2") do |config|

  # LAMP server
  config.vm.define "gshortener" do |gshortener|
    gshortener.vm.box = "openlogic/rockylinux-8"
    gshortener.vm.hostname = "gshortener.pusula.local"
    gshortener.vm.network "public_network",
      bridge: $network_interface,
      ip: "192.168.#{$subnet}.21",
      dhcp: true
    gshortener.vm.provider "vmware_desktop" do |v|
      v.gui = true
      v.memory = 2048
      v.cpus = 2
    end
    gshortener.vm.provision "ansible" do |ansible|
      ansible.limit = "all"
      ansible.playbook = "ansible/gshortener/gshortener.yml"
    end
  end

  # Jenkins server
  config.vm.define "jenkins" do |jenkins|
    jenkins.vm.box = "openlogic/rockylinux-8"
    jenkins.vm.hostname = "jenkins01.pusula.local"
    jenkins.vm.network "public_network",
      bridge: $network_interface,
      ip: "192.168.#{$subnet}.22",
      dhcp: true
    jenkins.vm.synced_folder ".", "/vagrant"
    jenkins.vm.provider "vmware_desktop" do |v|
      v.gui = true
      v.memory = 2048
      v.cpus = 2
    end
    jenkins.vm.provision "ansible" do |ansible|
      ansible.limit = "all"
      ansible.playbook = "ansible/jenkins/jenkins.yml"
    end
  end

  # Configure global settings for all VMs
  config.vm.provider "vmware_desktop" do |v|
    v.whitelist_verified = true
    v.vmx["ethernet0.virtualDev"] = "vmxnet3"
    v.vmx["ethernet1.virtualDev"] = "vmxnet3"
    v.memory = 2048
    v.cpus = 2
  end

end