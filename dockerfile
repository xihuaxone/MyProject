# Base images 基础镜像
FROM centos:7

#MAINTAINER 维护者信息
MAINTAINER xihua

#ENV 设置环境变量
ENV PATH /MyProject/my_project:$PATH

#ADD  文件放在当前目录下，拷过去会自动解压
ADD . /MyProject

#RUN 执行以下命令
RUN yum install -y python3
RUN yum install -y wget lftp gcc gcc-c++ make openssl-devel pcre-devel pcre && yum clean all
RUN pip3 install tornado==6.0.4

#WORKDIR 相当于cd
WORKDIR /MyProject/my_project

#CMD 运行以下命令
CMD ["python3", "server.py"]


# docker build -f ./dockerfile -t my_project:{{version}} .
# sudo docker run -p 8080:8080 --net=host --name=my_project -d {{image id}}