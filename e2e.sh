#! /bin/bash

website="app_container:5000"
declare -a curl_list=("$website/search?refer=curltest" "$website/list" "-X POST $website/action?name=tat&desc=11")


for action in "${curl_list[@]}";do
        #echo $action
        status_code=`curl -sL -w %{http_code} -I $action -o /dev/null\n | tail -1`
        
        if (($status_code >= 200 && $status_code < 400));then
                echo "$action status-code : $status_code"
        else
            exit 1
        fi
done
