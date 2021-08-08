#!/bin/bash


export PYTHONPATH=~/miniconda3/bin/python3
export PYTHONHOME=~/miniconda3/bin/python3

echo "checking if the python script is already running"

SERVICE="tweetBot"
if pgrep -x "$SERVICE" >/dev/null
then
    echo "$SERVICE is running"
else
    echo "$SERVICE stopped"
    echo "starting $SERVICE"
    bash -c "exec -a tweetBot python3 ./favretweet.py" 
    

fi


