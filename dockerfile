FROM centos:7
MAINTAINER xihua

ENV PATH /MyProject/my_project:$PATH

COPY . /MyProject

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
RUN yum install -y python3
RUN yum install -y yum install gcc python3-devel mysql-devel
RUN pip3 install --user -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com -r /MyProject/requirements

WORKDIR /MyProject/my_project

CMD ["python3", "server.py"]
