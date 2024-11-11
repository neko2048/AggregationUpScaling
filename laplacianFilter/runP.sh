#!/bin/bash
fileName=tildeLaplaceFilterFor39.py
#for i in 1.0 2.0 4.0 8.0 16.0
for i in 1.0 4.0 
do
    python $fileName  105 106 16 $i & wait
    python $fileName  152 153 16 $i & wait
    python $fileName  159 160 16 $i & wait
    #python $fileName   0   1 $i & wait
    #python $fileName   1 200 $i &
    #python $fileName 200 400 $i &
    #python $fileName 400 625 $i &
    wait
done
#fileName=laplaceFilterFor39.py
#python $fileName    0    1 2
#python $fileName    1  200 2 &
#python $fileName  200  400 2 &
#python $fileName  400  625 2 &
#wait
