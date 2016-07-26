#!/bin/sh
while true; do
  $2 &
  PID=$!
  inotifywait -e modify $1
  kill $PID
done
