docker stop rfgateway
docker rm rfgateway
docker build -t danobot/rfgateway .
docker run -d --restart=unless-stopped -e MQTT_HOST="tower.local" -v $(pwd)/receive-cached.py:/app/script.py --privileged=true --name rfgateway danobot/rfgateway
