FROM python:3.8

RUN mkdir /app
WORKDIR /app

RUN git clone https://github.com/nigelb/Static-UPnP.git
RUN cd Static-UPnP && pip install ".[interfaces]"

COPY config/ /app/config/
COPY healthcheck.py /app/

HEALTHCHECK CMD python /app/healthcheck.py

USER 1000:1000
CMD ["static_upnp", "--config-dir", "config/"]
