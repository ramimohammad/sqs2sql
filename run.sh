#!/bin/bash
sudo apt update -y 
sudo apt install unzip -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf aws*
aws configure set aws_access_key_id fakekey; aws configure set aws_secret_access_key fakesecret; aws configure set default.region ap-southeast-1
cp env .env
python3.10 -m venv venv
. ./venv/bin/activate
pip install -U pip
pip install -r requirements.txt
sudo docker-compose up -d
./message-generators/linux
