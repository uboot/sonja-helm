import docker
import string
import re


setup_template = string.Template(
"""sh -c \" \
conan remote clean \
&& conan remote add server $conan_url \
&& conan user -r server -p $conan_password $conan_user \
\"
"""
)

source_template = string.Template(
"""sh -c \" \
mkdir conanci \
&& cd conanci \
&& git init \
&& git remote add origin $git_url \
&& git fetch origin $git_sha \
&& git checkout FETCH_HEAD \
\"
"""
)

build_template = string.Template(
"""sh -c \" \
conan create $package_path $channel
\"
"""
)

conan_user = "agent"
conan_url = "conan-server"
conan_password = "demo"
docker_image_pattern = "([a-z0-9\\.-]+(:[0-9]+)?)?[a-z0-9\\.-/]+[:@]([a-z0-9\\.-]+)$"
git_url = "https://github.com/uboot/conan-ci.git"
git_sha = "ce8ad84282be5583989bdbdf0c42e95a53527657"
package_path = "./conanci/packages/hello/"
channel = "@user/latest"

image = "conanio/gcc9:1.29.2"
if not re.match(docker_image_pattern, image):
    print("The image '%s' is not a valid docker image name", image)

setup_script = setup_template.substitute(conan_url=conan_url, conan_user=conan_user, conan_password=conan_password)
source_script = source_template.substitute(git_url=git_url, git_sha=git_sha)
build_script = build_template.substitute(package_path=package_path, channel=channel)

client = docker.from_env()
client.images.pull(image)

try:
    setup = client.containers.create(image=image, command=setup_script)
    setup.start()
    setup.wait()
    setup.commit(repository="setup", tag="local")
    setup.remove()

    source = client.containers.create(image="setup:local", command=source_script)
    source.start()
    source.wait()
    source.commit(repository="source", tag="local")
    source.remove()

    info = client.containers.run(
        image="source:local",
        command="conan inspect -a name -a version {0}".format(package_path),
        remove=True)
    print(info)

    build = client.containers.create(image="source:local", command=build_script)
    build.start()
    build.wait()
    build.commit(repository="build", tag="local")
    build.remove()

    reply = client.containers.run(
        image="build:local",
        command="conan upload --confirm {0}".format("hello"), remove=True)
    print(reply)

except Exception as e:
    print(e)
    pass

client.images.remove("setup:local")
client.images.remove("source:local")
client.images.remove("build:local")