FROM centos:7
MAINTAINER xihua

ENV PATH /MyProject/my_project:$PATH

COPY . /MyProject

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
RUN yum install -y python3
RUN yum install -y wget lftp gcc gcc-c++ make openssl-devel pcre-devel pcre && yum clean all
RUN pip3 install tornado==6.0.4
RUN pip3 install requests==2.24.0
RUN pip3 install urllib3==1.25.10
RUN pip3 install SQLAlchemy==1.3.19
RUN pip3 install mysqlclient==2.0.1

WORKDIR /MyProject/my_project

CMD ["python3", "server.py"]
