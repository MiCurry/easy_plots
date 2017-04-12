import os.path as path
import docker

print "Testing Docker Client"
client = docker.from_env()
out = client.containers.run('basemap', 'python plot.py test').strip()
assert (out == "All Systems Go")
print "PASSED"
