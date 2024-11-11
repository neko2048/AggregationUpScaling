#!/bin/bash
fileName=saveQvThBuoyancy.py
for i in 1
do
    python $fileName 345 346   $i &
    python $fileName 427 428   $i &
done
