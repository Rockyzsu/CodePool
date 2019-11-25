#!/bin/sh
printf "CH2 Example Mailer has started.\n"
while true
do
        MESSAGE=`nc -l -p 33333`
        printf "Sending email: %s\n" "$MESSAGE"
	sleep 1
done
