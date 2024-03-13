echo "stopping 80"
nginx -c conf/nginx.conf -s stop -p nginx/80
echo "stopping 4000"
nginx -c conf/nginx.conf -s stop -p nginx/4000
echo "OK"
