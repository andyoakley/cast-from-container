# Cast to Chromecast from a dockerized headless browser

The Chromecast has a recent Chrome browser but has a weak CPU that cannot render complex sites. What if we could render content in a container on a more powerful machine and cast the tab instead? Nice idea, but Chromecast discovery typically doesn't work inside Docker unless `--net=host` is used. This is due to the Chromecast discovery mechanism which uses TTL=1 to avoid discovery of cross-subnet devices. Using host networking isn't a great solution especially in a Kubernetes setup.

Therefore, this pair of containers does two things:

1. Advertise the Chromecast inside the Docker network using [Static-UPnP](https://github.com/nigelb/Static-UPnP). Thanks NigelB!
1. Host a Chrome instance and start tab mirroring.

[Blog post with more details](https://andyoakley.com/2021/12/cast-from-container/)

## Usage

The renderer will wait until the Chromecast device is free before casting to it. If the casting session is interrupted, the container will exit, so having a restart policy is a good idea.

The `/app/script.py` file in the `render` container exposes a single method which takes a Selenium ChromeDriver object. See [examples/scripts/](examples/scripts/) for some examples.

## Orchestration examples

- [docker-compose](examples/docker-compose/)
- Kubernetes [deployment and configmap](examples/kubernetes/)

## Todo

- Images are heavy and could be trimmed with some minor effort.

## References

- https://ndportmann.com/chrome-in-docker/
- [Static-UPnP](https://github.com/nigelb/Static-UPnP). 
