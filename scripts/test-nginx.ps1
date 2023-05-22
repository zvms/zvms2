echo "reloading 80"
nginx -c conf/nginx.conf -T -p nginx/80
echo "reloading 4000"
nginx -c conf/nginx.conf -T -p nginx/4000
echo "OK"