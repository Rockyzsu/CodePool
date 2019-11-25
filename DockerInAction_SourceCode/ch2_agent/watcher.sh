#!/bin/sh
while true
do
        if `printf "GET / HTTP/1.0\n\n" | nc -w 2 $INSIDEWEB_PORT_80_TCP_ADDR $INSIDEWEB_PORT_80_TCP_PORT | grep -q '200 OK'`
        then
		echo "System up."
        else 
        	printf "To: admin@work  Message: The service is down!" | nc $INSIDEMAILER_PORT_33333_TCP_ADDR $INSIDEMAILER_PORT_33333_TCP_PORT
                break
	fi

	sleep 1
done
