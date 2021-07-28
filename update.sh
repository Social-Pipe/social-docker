cd reactapp
git checkout release
git pull
cd ..
git checkout develop
git pull
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
