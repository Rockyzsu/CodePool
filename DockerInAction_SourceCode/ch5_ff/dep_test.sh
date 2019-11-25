#!/bin/sh

if [ -z ${DATABASE_PORT+x} ]
then 
	echo "Link alias 'database' was not set!"
	exit
else 
	exec "$@"
fi
