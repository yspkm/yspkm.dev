sudo docker-compose down
sh docker-compose logs
sudo docker-compose up -d --build
sh docker-compose logs
sh migrate.sh
sh docker-compose logs
