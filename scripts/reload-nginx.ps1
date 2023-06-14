echo "copying dist"
./copy-dist.ps1
echo "reloading 80"
nginx -c conf/nginx.conf -s reload -p nginx/80
echo "reloading 4000"
nginx -c conf/nginx.conf -s reload -p nginx/4000
echo "OK"