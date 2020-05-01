From elasticsearch:6.4.0
LABEL description="Inventory app docker file"

RUN yum install epel-release -y
RUN yum install python-pip -y
RUN pip install Flask==0.12.2 requests SQLAlchemy==1.3.16

COPY . /inventory-app/
EXPOSE 8080/tcp
WORKDIR /inventory-app

ENTRYPOINT python app.py
