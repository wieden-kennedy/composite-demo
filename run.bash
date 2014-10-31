#!/bin/bash
# Test network down speed to see if importing the images from s3 is a good idea
THRESHOLD=10
echo "==> Testing network speed..."
START=$(date +%s)
wget -q -O /dev/null https://s3-us-west-2.amazonaws.com/composite-vagrant/docker_assets/speed_test_25.dat
END=$(date +%s)
DIFF=$((END-START))
IMPORT='true'

# if download time is greater than threshold, offer option to build containers locally
if [ ${DIFF} -gt ${THRESHOLD} ];then
    echo "Your internet speeds indicate it will take some time to download the Docker images from S3. Building locally may decrease the time to get Composite up and running. Build locally?"
    select res in "build locally" "import anyway"; do
        case $res in
            "import anyway")
                break
                ;;
            "build locally")
                IMPORT='false'
                break
                ;;
        esac
    done
fi

if [ ${IMPORT} == 'true' ]; then
fab import_container && fab run
else
    fab build && fab run
fi
