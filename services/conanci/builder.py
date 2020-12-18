import docker
import os
import re
import string
import tarfile
import threading

from conanci.config import logger
from io import BytesIO


docker_image_pattern = ("([a-z0-9\\.-]+(:[0-9]+)?/)?"
                        "[a-z0-9\\.-/]+([:@][a-z0-9\\.-]+)$")

# docker run --name conan -d --rm -p 9300:9300 -v /path-to-server-config:/root/.conan_server conanio/conan_server:1.28.1


def create_build_tar(build_os, parameters):
    if build_os == "Linux":
        script_template_name = "build.sh.in"
    else:
        script_template_name = "build.ps1.in"
    script_name = script_template_name[:-3]

    # read and configure build script
    setup_file_path = os.path.join(os.path.dirname(__file__), script_template_name)
    with open(setup_file_path) as setup_template_file:
        template = string.Template(setup_template_file.read())
    script = template.substitute(parameters)

    # place into archive
    f = BytesIO()
    tar = tarfile.open(mode="w", fileobj=f, dereference=True)
    tarinfo = tarfile.TarInfo(script_name)
    content = BytesIO(bytes(script, "utf-8"))
    tarinfo.size = len(content.getbuffer())
    tar.addfile(tarinfo, content)
    ssh_key_path = os.path.join(parameters["ssh_dir"], parameters["ssh_key"])
    tar.add(name=ssh_key_path, arcname=parameters["ssh_key"])
    known_hosts_path = os.path.join(parameters["ssh_dir"], "known_hosts")
    tar.add(name=known_hosts_path, arcname="known_hosts")
    tar.close()
    f.seek(0)
    return f


class Builder(object):
    def __init__(self, build_os, image):
        self.__client = docker.from_env()
        self.__image = image
        self.__build_os = build_os
        self.__container = None
        self.__logs = None
        self.__cancel_lock = threading.Lock()
        self.__cancelled = False

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

    def setup(self, parameters):
        logger.info("Setup docker container")
        build_tar = create_build_tar(self.__build_os, parameters)

        # with open("build.tar", "wb") as f:
        #     f.write(build_tar.read())
        # build_tar.seek(0)

        if self.__build_os == "Linux":
            command = "sh /build.sh"
        else:
            command = 'cmd /s /c "powershell -File C:\\build.ps1"'

        self.__container = self.__client.containers.create(image=self.__image,
                                                           command=command)
        logger.info("Created docker container '%s'", self.__container.short_id)

        if self.__build_os == "Linux":
            build_data_dir = "/"
        else:
            build_data_dir = "C:\\"
        result = self.__container.put_archive(build_data_dir, data=build_tar)
        if not result:
            raise Exception("Failed to copy build files to container '{0}'"\
                            .format(self.__container.short_id))

    def run(self):
        with self.__cancel_lock:
            if self.__cancelled:
                logger.info("Build was cancelled")
                return
            logger.info("Start build in container '{0}'" \
                        .format(self.__container.short_id))
            self.__container.start()
            self.__logs = self.__container.logs(stream=True, follow=True)
        for line in self.__logs:
            logger.info(line.decode("utf-8").strip("\n\r"))
        with self.__cancel_lock:
            self.__logs = None
            if self.__cancelled:
                logger.info("Build was cancelled")
                return

        result = self.__container.wait()
        if result.get("StatusCode"):
            raise Exception("Build in container '{0}' failed with status '{1}'".format(
                            self.__container.short_id, result.get("StatusCode")))

    def cancel(self):
        with self.__cancel_lock:
            logger.info("Cancel build")
            self.__cancelled = True
            if self.__logs:
                logger.info("Close logs")
                self.__logs.close()

    def __exit__(self, type, value, traceback):
        if not self.__container:
            return

        try:
            logger.info("Stop docker container '%s'", self.__container.short_id)
            self.__container.stop()
        except docker.errors.APIError:
            pass

        try:
            logger.info("Remove docker container '%s'", self.__container.short_id)
            self.__container.remove()
        except docker.errors.APIError:
            pass
