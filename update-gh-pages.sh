# Always recreate the gh-pages branch!
BRANCH=$(git symbolic-ref -q --short HEAD || git describe --tags --exact-match 2> /dev/null || git rev-parse --short HEAD)
git checkout master
git checkout -B gh-pages master
DOCGEN=1 ./run-tests.sh $TRAVIS_PYTHON_VERSION
git status
git add doc/
git commit -m "Travis CI updated python$TRAVIS_PYTHON_VERSION coverage report."
git push
git checkout $BRANCH