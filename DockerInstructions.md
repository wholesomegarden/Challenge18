<!-- DockerInstructions.md -->

docker container prune

# 1. Create network
docker network create selenium

# 2. Run Selenium grid/standalone container
docker run -d -p 4444:4444 -p 5900:5900 --name firefox --network selenium -v /dev/shm:/dev/shm selenium/standalone-firefox-debug:3.14.0-curium

# 3. Build python/webwhatsapi docker base image
docker build -t webwhatsapi .

# 4. Run client container
docker run --network selenium -it -e SELENIUM='http://firefox:4444/wd/hub' -v $(pwd):/app  webwhatsapi /bin/bash -c "pip install ./;pip list;python sample/remote.py"
