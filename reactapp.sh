cd reactapp
git checkout develop
git pull
git checkout release
git push
git merge develop
cd ..
git commit -am "update submodule ref"
git push