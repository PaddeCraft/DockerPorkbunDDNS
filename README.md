[![Docker Publish CI](https://github.com/PaddeCraft/DockerPorkbunDDNS/actions/workflows/registry.yaml/badge.svg)](https://github.com/PaddeCraft/DockerPorkbunDDNS/actions/workflows/registry.yaml)
![Last Commit](https://img.shields.io/github/last-commit/PaddeCraft/DockerPorkbunDDNS/master)
![GitHub Issues](https://img.shields.io/github/issues/PaddeCraft/DockerPorkbunDDNS)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/PaddeCraft/DockerPorkbunDDNS)


# DockerPorkbunDDNS

A docker image for dynamic dns using Porkbun.

**This project is not related to or affiliated with Porkbun.**

## Getting started

There is a prebuilt image available. If you want to build it yourself, you may use the `build_docker.sh` script.

After the first container start, if no config is found, it will create one and exit. You can then edit the values to fit your use case.

### Docker Compose example

```yaml
services:
    ddns:
        image: ghcr.io/paddecraft/dockerporkbun_ddns:latest
        volumes:
            - "/your/path/for/config:/config"
```

### Docker Run example

```shell
docker run -v "/your/path/for/config:/config" ghcr.io/paddecraft/dockerporkbun_ddns:latest
```

## Contributing

If you found an issue, feel free to report it or to open a pull request.

### Local development

I recommend you setup a virtual environment with `python -m venv .venv`. It is already ignored in the `.gitignore`. The entrypoint script is configured to work without the docker container, using the config path `./config.json` by default (configurable through environment `CONFIG_PATH`).

There is also a mode to test the core functionality if `TEST_MODE=true` is set in the environment.

## Special thanks to

- [mietzen/porkbun-ddns](https://github.com/mietzen/porkbun-ddns): An API wrapper for Porkbun making my life a whole lot easier
