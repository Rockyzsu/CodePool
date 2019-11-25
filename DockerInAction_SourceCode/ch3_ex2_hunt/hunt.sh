#!/bin/sh

printf "Thanks for running the Docker in Action Chapter 3 scavenger hunt.\nEnter the password: "
read pass
secret=5a9854360fc3ffe8043ef37fa2d7d507dcf7fafc

if `echo $pass | sha1sum | grep -q $secret`; then
    echo "Congratulations! You've found the password using Docker Hub and used an interactive container!" 
elif [ "$pass" == "$secret" ]; then
    echo "Incorrect. You won't find the answer in this image without some serious compute power."
else
    echo "Incorrect. Maybe you could find another image that contains the answer?"
fi

