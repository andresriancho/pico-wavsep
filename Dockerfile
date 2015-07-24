FROM java:openjdk-7u79-jdk

RUN apt-get update
RUN apt-get install -y curl netcat mysql-client

# Copy pico-wavsep source code
COPY . /

EXPOSE 8080
CMD ["/docker/run.sh"]


