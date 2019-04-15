## Postgresql in docker 

### Pull Docker image
`docker pull postgres` or `docker pull postgres:10`

### Create directory
`mkdir -p $HOME/docker/volumes/postgres`

### Run
`docker run --rm --name pg10docker -e POSTGRES_PASSWORD=docker -e POSTGRES_USER=docker -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres:10`

### Display which program use port 
`sudo netstat -ltnp | grep -w ':5432'`


### Run sql script
`curl -s http://dorokhin.moscow/buckup/backup.sql | sudo -u postgres psql`


```sql
insert into url_data_store values ('192.168.2.1');
insert into url_data_store values ('192.168.2.1/24');

select * from url_data_store;

```
