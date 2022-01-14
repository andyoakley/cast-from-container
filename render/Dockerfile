FROM ubuntu

ARG CHROME_VERSION=96.0.4664.110-1
ARG CHROMEDRIVER_VERSION=96.0.4664.45

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install python3-pip xvfb curl unzip

# install chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add 
RUN bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" 
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable=$CHROME_VERSION

# install chromedriver
WORKDIR /tmp
RUN wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/local/bin

# sometimes useful
#RUN pip3 install catt
#CMD ["catt", "cast", "https://www.youtube.com/watch?v=ZsB5EARgFG4"]

RUN pip3 install selenium

RUN mkdir /app
WORKDIR /app
COPY main.py /app/
COPY script.py /app/
COPY wrapper /app/

RUN chown 1000:1000 /app
USER 1000:1000
ENV HOME=/app

#CMD ["xvfb-run", "-a", "python3", "headful.py"]
CMD ["/app/wrapper"]
