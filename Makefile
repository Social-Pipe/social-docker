init:
	git submodule init
	git submodule update
dev:
	docker-compose up -d --build
down:
	docker-compose down --remove-orphans --volumes
prod_update:
	git checkout develop
	git pull
	git submodule update
	docker-compose -f docker-compose.prod.yml down
	docker-compose -f docker-compose.prod.yml build --no-cache
	docker-compose -f docker-compose.prod.yml up -d
merge_reactapp:
	cd reactapp
	git checkout develop
	git pull
	git checkout release
	git push
	git merge develop
	cd ..
	git commit -am "update submodule ref"
	git push