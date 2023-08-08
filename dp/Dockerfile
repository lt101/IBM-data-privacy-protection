FROM openjdk:19
WORKDIR /dp
COPY . /dp
RUN microdnf install findutils
RUN ./gradlew clean build -x test --refresh-dependencies
CMD ./gradlew run --args='arg1 arg2'
