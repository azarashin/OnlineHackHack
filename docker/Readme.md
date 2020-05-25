# how to construct docker environment. 

```
sudo docker compose up -d

sudo ./init-mysql.sh

```

## directory structure

|-- mount
|   |-- db
|   |    |-- data
|   |    |-- my.cnf
|   |    |-- sql
|   |        |-- 001-create-tables.sql
|   |        |-- init-database.sh
|   |-- nodered
|   |-- nginx
|       |-- public
|-- docker-compose.yml
|-- init-mysql.sh


## initial table for mysql

edit 001-create-tables.sql
