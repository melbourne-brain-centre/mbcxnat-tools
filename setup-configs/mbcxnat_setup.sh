## Installing MBC xnat form a single script

# Install docker and docker -compose

sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io

# Install java open-jdk 8 

sudo apt-get install openjdk-8-jdk

# Install nginx 

sudo apt-get install nginx


# setting up service

sudo su


## Setup nginx 
cp ./nginx/mbcxnat /etc/nginx/sites-available/

rm /etc/nginx/sites-enabled/default

cd /etc/nginx/sites/enabled

ln -s /etc/sites-avaliable/mbcxnat mbcxnat

systemctl restart nginx.service

ZZ
