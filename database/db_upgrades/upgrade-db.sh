#!/bin/bash
docker-compose exec -T db sh -c 'mysql -u slaveuser -pslavepass boxing -e "create table if not exists local_db_version (version_num integer not null)"'

VERSION=$(docker-compose exec -T db sh -c "mysql -u slaveuser -pslavepass boxing -e \"select version_num from local_db_version\"" | tr -d -c 0-9)

if [[ -z "$VERSION" ]] || [[ $VERSION == 0 ]]; then
    echo "Setting initial version"
    VERSION=0
    docker-compose exec -T db sh -c "mysql -u slaveuser -pslavepass boxing -e 'insert local_db_version values ($VERSION)"
fi

echo "You are on: $VERSION"
echo "Checking for updates..."

for update in `ls ./*.sql | sort -n -t_ -k 2`; do
    echo "Checking $update"

    noext=$(cut -d. -f2 <<< $update)
    thisversion=$(cut -d_ -f2 <<< $noext)

    if [[ $VERSION -lt $thisversion ]]; then
        echo "Updating to version: $thisversion"
        docker-compose exec -T db sh -c "mysql -u slaveuser -pslavepass boxing < /var/db_upgrades/${update}"
        VERSION=$thisversion
    fi
done

docker-compose exec -T db sh -c "mysql -u slaveuser -pslavepass boxing -e 'update local_db_version set version_num=${VERSION}'"
echo "You are now on: $VERSION"