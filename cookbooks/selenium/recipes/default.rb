if platform?("ubuntu","debian")
  include_recipe "selenium::apt"
end

USER=node['selenium']['user']

group USER

user USER do
  comment "selenium user"
  gid USER
  #system true
  shell "/bin/bash"
  home node['selenium']['home']
end

#folder for pids
directory '/var/run/selenium' do
  mode "0775"
  owner "root"
  group "root"
  action :create
  recursive true
end

directory node['selenium']['server']['installpath'] do
  owner USER
  recursive true
end

directory node['selenium']['home']+'init/' do
  mode "0775"
  owner USER
  group USER
  action :create
  recursive true
end

version = node['selenium']['server']['version']
version_tuple = version.split('.')

if version_tuple[1].to_i < 39
  download_path = "http://selenium.googlecode.com/files/selenium-server-standalone-#{version}.jar"
else
  download_path = "http://selenium-release.storage.googleapis.com/#{version_tuple[0,2].join('.')}/selenium-server-standalone-#{version}.jar"
end

remote_file File.join(node['selenium']['server']['installpath'], 'selenium-server-standalone.jar') do
  source download_path
  action :create_if_missing
  mode 0644
  owner USER
  group USER
end
