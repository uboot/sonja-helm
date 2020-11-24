import docker
import os
import re
import string
import sys
import tarfile

from conanci.config import logger
from io import BytesIO


docker_image_pattern = ("([a-z0-9\\.-]+(:[0-9]+)?/)?"
                        "[a-z0-9\\.-/]+([:@][a-z0-9\\.-]+)$")


def create_build_tar(build_os, url, user, password):
    if build_os == "Linux":
        script_template_name = "build.sh.in"
    else:
        script_template_name = "build.ps1.in"
    script_name = script_template_name[:-3]

    # read and configure build script
    setup_file_path = os.path.join(os.path.dirname(__file__), script_template_name)
    with open(setup_file_path) as setup_template_file:
        template = string.Template(setup_template_file.read())
    script = template.substitute(conan_url=url,
                                 conan_user=user,
                                 conan_password=password)

    # place into archive
    f = BytesIO()
    tar = tarfile.open(mode="w", fileobj=f)
    tarinfo = tarfile.TarInfo(script_name)
    content = BytesIO(bytes(script, "utf-8"))
    tarinfo.size = len(content.getbuffer())
    tar.addfile(tarinfo, content)
    tar.close()
    f.seek(0)
    return f


class Builder(object):
    def __init__(self, build_os, image):
        self.__client = docker.from_env()
        self.__image = image
        self.__build_os = build_os
        self.__container = None

    def __enter__(self):
        return self

    def pull(self):
        m = re.match(docker_image_pattern, self.__image)
        if not m:
            raise Exception("The image '{0}' is not a valid "
                            "docker image name".format(self.__image))
        if m.group(3) == ":local":
            logger.info("Do not pull local image '%s'", self.__image)
            return

        logger.info("Pull docker image '%s'", self.__image)
        self.__client.images.pull(self.__image)

    def setup(self, url, user, password):
        logger.info("Setup docker container")
        build_tar = create_build_tar(self.__build_os, url, user, password)

        if self.__build_os == "Linux":
            command = "sh /build.sh"
        else:
            command = 'cmd /s /c "powershell -File C:\\build.ps1"'

        self.__container = self.__client.containers.create(image=self.__image,
                                                           command=command)

        if self.__build_os == "Linux":
            build_data_dir = "/"
        else:
            build_data_dir = "C:\\"
        result = self.__container.put_archive(build_data_dir, data=build_tar)
        if not result:
            raise Exception("Failed to copy build files to container '{0}'"\
                            .format(self.__container.short_id))

    def run(self):
        logger.info("Start build in container '{0}'"\
                    .format(self.__container.short_id))
        self.__container.start()
        logs = self.__container.logs(stream=True, follow=True)
        for line in logs:
            logger.info(line.decode("utf-8").strip("\n\r"))
        result = self.__container.wait()
        if result.get("StatusCode"):
            raise Exception("Build in container '{0}' failed with status '{1}'".format(
                            self.__container.short_id, result.get("StatusCode")))

    def remove(self):
        self.__container.remove()

    def __exit__(self, type, value, traceback):
        if not self.__container:
            return

        try:
            logger.info("Remove all temporary docker containers")
            self.__container.remove()
        except docker.errors.ImageNotFound:
            pass