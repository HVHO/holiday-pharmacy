# delete tmp files
rm -r tmp

# prepare zip file to deploy
mkdir tmp
cp -r crawler tmp
cd tmp

# prepare main.py file
echo 'import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "package"))
from crawler.src.main import main
import requests
def handler(event, context):
    main(event, context)
    return { "status" : 200 }' >> lambda_function.py


# install dependencies
mkdir package
pip3 install -t ./package -r ../requirements.txt
zip -r9 function.zip  ./package/*

zip -rg function.zip  lambda_function.py \
                      crawler/src/main.py \
                      crawler/src/config \
                      crawler/src/db \
                      crawler/src/map_client \
                      crawler/src/parser \
					            package/* \
                      -x '*.json' -x '*/chrome-driver/*' -x  '*/.idea/*' -x '*.DS_Store*' -x '*/.git/*'

# upadte aws lambda code
aws lambda update-function-code --function-name holiday-pharmacy-2 --zip-file fileb://function.zip 
