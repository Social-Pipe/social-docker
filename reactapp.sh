cd reactapp
git checkout develop
git pull
git checkout release
git merge develop
cd ..
git commit -am "update submodule ref"
git push