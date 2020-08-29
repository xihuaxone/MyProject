# MyProject
This is a project for fun... or not? I don't know.

This is a project developed based on python3.5

To install mysqlclient in ubuntu, you need to install depended packages first, command:
sudo apt-get install libmysqld-dev

To generate model file, you need to install package: sqlacodegen. Usage demo:
sqlacodegen mysql://{{uname}}:{{passwd}}@{{host}}:3306/my_project?charset=utf8 > ./models.py