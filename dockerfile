FROM centos:7
MAINTAINER xihua

ENV PATH /MyProject/my_project:$PATH

COPY . /MyProject

RUN yum install -y python3
RUN yum install -y wget lftp gcc gcc-c++ make openssl-devel pcre-devel pcre && yum clean all
RUN pip3 install tornado==6.0.4

WORKDIR /MyProject/my_project

CMD ["python3", "server.py"]


# docker build -f ./dockerfile -t my_project:{{version}} .
# sudo docker run -p 8080:8080 --net=host --name=my_project -v /usr/local/my_project/logs/:/MyProject/my_project/logs/ -d {{image id}}