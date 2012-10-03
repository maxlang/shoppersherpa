pushd "$(git rev-parse --show-toplevel)"

pip install virtualenv

virtualenv .


source ./Scripts/activate
./Scripts/activate.bat

pip install hg+https://bitbucket.org/wkornewald/django-nonrel
pip install hg+https://bitbucket.org/wkornewald/djangotoolbox
pip install git+https://github.com/django-nonrel/mongodb-engine

popd