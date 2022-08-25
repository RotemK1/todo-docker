#! /bin/bash

# declare -a curl_list=(`curl -sL -w "%{http_code}" -I "app_container:5000/search?refer=curltest" -o /dev/null` `curl -sL -w "%{http_code}" -I "app_container:5000/list" -o /dev/null` `curl -sL -w "%{http_code}" -I "app_container:5000" -o /dev/null` `curl -sL -w "%{http_code}" -I -X POST "app_container:5000/action?name=tat&desc=11" -o /dev/null`)
# for status_code in ${curl_list[@]};do
#         if (($status_code >= 200 && $status_code < 400));then
#                 echo $status_code
#         else
#             exit 1
#         fi
# done
website="app_container:5000"
declare -a curl_list=('localhost:5000/search?refer=curltest' 'localhost:5000/list' '-X POST localhost:5000/action?name=tat&desc=11')

for action in "${curl_list[@]}";do
        #echo $action
        status_code=`curl -sL -w %{http_code} -I $action -o /dev/null\n | tail -1`
        echo $action
        if (($status_code >= 200 && $status_code < 400));then
                echo $status_code
        else
            exit 1
        fi
done