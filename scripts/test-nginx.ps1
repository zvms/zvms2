echo "testing 80"
nginx -c conf/nginx.conf -T -p nginx/80
echo "testing 4000"
nginx -c conf/nginx.conf -T -p nginx/4000
echo "OK"