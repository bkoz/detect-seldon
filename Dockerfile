# FROM image-registry.openshift-image-registry.svc:5000/openshift/python-38
FROM registry.redhat.io/rhel8/python-38
USER root
RUN dnf install -y mesa-libGL
COPY . /app
WORKDIR /app
EXPOSE 5000
RUN pip install --upgrade pip && pip install -r requirements.txt

ENV MODEL_NAME Detection
ENV API_TYPE REST
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0

CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE --persistence $PERSISTENCE --log-level INFO
# CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE --persistence $PERSISTENCE --log-level DEBUG
