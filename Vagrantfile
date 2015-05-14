#!/usr/bin/env ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "precise32"

  # The url from where the 'config.vm.box' box will be fetched.
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  config.vm.network :forwarded_port, guest: 80, host: 8500
  config.ssh.forward_agent = true

  # Share devops folder with guest VM. 
  config.vm.synced_folder './devops', '/vagrant/devops', 
      :mount_options => ['fmode=666']

  # provision the virtual machine
  config.vm.provision :shell, :path => "devops/provision.sh"

  # Prevent Ubuntu Precise DNS resolution from mysteriously failing
  # http://askubuntu.com/a/239454
  config.vm.provider "virtualbox" do |vb| 
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  # Cache apt-get package downloads to speed things up
  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
    config.cache.enable :generic, { :cache_dir => "/var/cache/pip" }
  end

end