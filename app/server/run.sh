docker run -d \
  --name mysql-container \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=usuarios_db \
  -e MYSQL_USER=plof \
  -e MYSQL_PASSWORD=pass \
  -v /path/to/init.sql:/docker-entrypoint-initdb.d/init.sql \
  -p 3306:3306 \
  mysql:5.7

