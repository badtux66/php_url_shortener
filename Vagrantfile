# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'socket'
require 'timeout'

$network_interface = `sudo iw dev | awk '$1=="Interface"{print $2}'`.strip
$subnet = `ip -4 addr show $network_interface | awk '/inet 192.168./{split($2,a,"."); print a[3]}'`.strip

def get_available_ip(base_ip, subnet)
  ip_parts = base_ip.split(".")
  ip_parts[2] = subnet
  (1..254).each do |octet|
    ip_parts[3] = octet.to_s
    candidate_ip = ip_parts.join(".")
    begin
      timeout(1) { TCPSocket.new(candidate_ip, 22) }
    rescue Errno::ETIMEDOUT, Errno::ECONNREFUSED, Timeout::Error
      return candidate_ip
    end
  end
  raise "No available IP addresses in the subnet"
end

Vagrant.configure("2") do |config|

  # LAMP server
  config.vm.define "gshortener" do |gshortener|
    gshortener.vm.box = "eurolinux-vagrant/rocky-9"
    gshortener.vm.hostname = "gshortener.pusula.local"
    gshortener_ip = get_available_ip("192.168.#{$subnet}.21", $subnet)
    gshortener.vm.network "public_network",
      bridge: $network_interface,
      ip: gshortener_ip,
      dhcp: true
    # ...

  # Jenkins server
  config.vm.define "jenkins" do |jenkins|
    jenkins.vm.box = "eurolinux-vagrant/rocky-9"
    jenkins.vm.hostname = "jenkins01.pusula.local"
    jenkins_ip = get_available_ip("192.168.#{$subnet}.22", $subnet)
    jenkins.vm.network "public_network",
      bridge: $network_interface,
      ip: jenkins_ip,
      dhcp: true
    # ...

  # Configure global settings for all VMs
  # ...
end
