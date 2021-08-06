# Full instructions for MBCXNAT installation

### Machine Setup
1. Ubuntu server prefered for Xnat installation.
2. Make sure the machine is up to date.
3. Prerequisits for XNAT setup:
	- Docker and Docker-compose
		https://docs.docker.com/engine/install/ubuntu/
		https://docs.docker.com/compose/install/
	- nginx
	- git
	- java > openjdk-8

---

### Download necessary source file
1. Clone the xnat repo form github and use following commands
	`git clone https://github.com/NrgXnat/xnat-docker-compose` 
	`cd xnat-docker-compose`
	`git checkout features/dependency-mgmt`

---

### Configure docker-compose
1. Replace the docker-compose.yml with custom file form mbcgithub
2. Download myProps.env fom mbcgithub and place in the same dir as docker-compose.yml
3. Download xnat-data and postgres-data directories in the same dir

---
### Configure nginx
1. Goto /etc/nginx/sites-available and put xnat conf form mbcgithub
2. Remove the symlink from sites-enabled and add symlink xnat -> /etc/nginx/sites-available/xnat
3. Put all ssl certificates in the corresponding path from xnat conf file

---
## XNAT startup commands

1. Build Xnat containers
	- For the first startup docker containers needs to be build with following command from dir with docker-compose.yml
	- `sudo ./gradlew -PenvFile=myProps.env -Pmanifest=manifest-XNAT-ML-18.json composeBuild`
2. Start Xnat Service
	- This will start xnat-web, xnat-db and traefik
	- `sudo ./gradlew composeUp`
3. Stop Xnat Service
	- This will stop xnat-web, xnat-db and traefik
	- `sudo ./gradlew composeDown`
4. Check Status
	- `sudo docker ps -a`
5. Restart just xnat-web
	- Get the container-id for xnatweb using docker ps -a
	- `sudo docker restart {container-id}`
