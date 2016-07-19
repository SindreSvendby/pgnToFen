#!/bin/sh
while true; do
  python $2 &
  PID=$!
  inotifywait -e modify $1
  kill $PID
done
