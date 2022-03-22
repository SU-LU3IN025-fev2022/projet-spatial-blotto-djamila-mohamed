#!/bin/bash

i=0;
while [ $i -lt 3 ]; do
  python3 semaine2-3.py
  sleep 2
  let "i=i+1"
done
