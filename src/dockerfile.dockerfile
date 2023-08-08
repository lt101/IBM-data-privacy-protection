FROM openjdk:19
WORKDIR /src
COPY . /src
RUN ./gradlew clean build -x test --refresh-dependencies
CMD ["/bin/sh", "-c", "./gradlew run --args='arg1 arg2'"]