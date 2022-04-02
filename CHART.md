# Sonja Helm Chart

This chart installs an instance of Sonja on a Kubernetes cluster (e.g.
[Minikube](https://minikube.sigs.k8s.io/)).

```
$ export RELEASE=<release-name>
$ cd <this-repository>
$ helm install $RELEASE chart/ -f <path-to-your-values>
```

In this example `<path-to-your-value>` should point to a `*.yml` file which
potentially overrides some of the parameters of the chart. The `<release-name>`
can be any suitable identifier.

## Ingress

Per default the chart installs a TLS enabled ingress for the provided host name.
An SSL certificate for the host name has to provided as a secret. The name of
the secret must equal the release name of the installed chart. The example below
creates and installs a self-signed certificate. Make sure that the "server FQDN"
for the certificate and the host name chart parameter match.

```
$ export RELEASE=<release-name>

$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
      -out tls.crt \
      -keyout tls.key

$ kubectl create secret tls $RELEASE \
      --key tls.key \
      --cert tls.crt
```

Alternatively, disable the ingress and expose the service
`<release-name>-sonja-public` in some other way.

## Authentification

For user authentification a secret has to be provided. It is used to encrypt the
authentification tokens of signed in users. Create some random value,
e.g.

```
$ openssl rand -hex 32
```

and provide it as a chart parameter.

When a Sonja release is installed for the first time an empty database is
initialized and one initial admin user is automatically created. The name and
password of this user can be provided as chart parameters.

## Initial Setup

You can provide the name of an initial ecosystem as a chart value. In this case
an ecosystem is created when the Sonja database is initialized the first time.
The ecosystem will contain some sample data which serves as a starting point for
first experiments with Sonja.

## Agents

Sonja requires at least one agent which uses a Docker-in-Docker approach to run
builds. Each agent can run only one build at a time. For parallel builds several
agents have to be created (`linux.replicas` and `windows.replicas`).

Linux agents should work on any Kubernetes cluster which allows privileged
containers.

Windows agents are more difficult to set up. They consist of a Linux container
which connects to a virtual Windows machine. The Windows machine then runs
builds in Windows docker containers.

Enabling Windows agents requires the following steps:

1. Install [kubevirt](https://kubevirt.io/) on the Kubernetes cluster
2. Prepare a qemu disk image:
    - based on a Windows operating system
    - has [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
    - has [cloudbase-init](https://cloudbase.it/cloudbase-init/) installed
    
   The [Packer](https://www.packer.io/) script
   [here](https://github.com/uboot/packer-windows/blob/win-qemu/windows_server_20h2_docker.json)
   can be used to automatically provision such an image.

3. Copy the disk image to a docker image (e.g.
   [Dockerfile](https://github.com/uboot/packer-windows/blob/win-qemu/Dockerfile.windows_20h2_docker))
   and publish it to a image repository which can be reached from the Kubernetes
   cluster.

Then set the `windows.image` chart parameter to the location of the image.

## Docker

Sonja builds Conan packages inside Docker containers. Depending on the exact
setup some Docker parameters have to be tweaked. Sometimes, if the build
container lives behind several layers of network virtualization, a smaller MTU
has to be used for network traffic from the container.

If the builds require docker
images from insecure registries these registries can be defined in a chart
parameter. Otherwise Docker would refuse to download images from such
registries.


## Parameters

### Ingress

| Name               | Description    | Value   |
| ------------------ | -------------- | ------- |
| `ingress.enabled`  | Enable ingress | `true`  |
| `ingress.hostName` | Host name      | `sonja` |


### Authentification

| Name             | Description                         | Value                                                              |
| ---------------- | ----------------------------------- | ------------------------------------------------------------------ |
| `auth.secretKey` | Secret key for authorization tokens | `1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef` |
| `auth.user`      | Name of the initial user            | `user`                                                             |
| `auth.password`  | Password of initial user            | `paSSw0rd`                                                         |


### Initial Setup

| Name               | Description                                  | Value         |
| ------------------ | -------------------------------------------- | ------------- |
| `initialEcosystem` | Name of the initial ecosystem with demo data | `MyEcosystem` |


### Agents

| Name               | Description                                                                 | Value                              |
| ------------------ | --------------------------------------------------------------------------- | ---------------------------------- |
| `linux.replicas`   | Number of Linux docker agents                                               | `1`                                |
| `windows.image`    | Docker image which contains a virtual disk with an installed Windows system | `registry:5000/windows20h2:latest` |
| `windows.replicas` | Number of Windows docker agents                                             | `0`                                |


### Docker

| Name                 | Description                          | Value  |
| -------------------- | ------------------------------------ | ------ |
| `mtu`                | MTU of the build (docker) containers | `1450` |
| `insecureRegistries` | List of insecure docker registries   | `[]`   |


### Mysql

| Name                      | Description       | Value    |
| ------------------------- | ----------------- | -------- |
| `mysql.auth.rootPassword` | Database password | `secret` |


