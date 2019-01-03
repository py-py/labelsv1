FROM python:3-slim
RUN mkdir /label
WORKDIR /label
ADD . .
ENV ENVIRONMENT=prod
RUN pip install -r requirements.txt
RUN sh ./start.sh