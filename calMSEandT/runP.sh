#!/bin/bash
fileName=calMSEandT.py
for i in 16
do
    #python $fileName   0   1 $i
    #echo $
    python $fileName 2000 2100 $i &
    python $fileName 2100 2200 $i &
    python $fileName 2200 2300 $i &
    python $fileName 2300 2400 $i &
    python $fileName 2400 2500 $i &
    #python $fileName 500 601 $i &
    #python $fileName   50  100 $i &
    #python $fileName  100  150 $i &
    #python $fileName  150  200 $i &
    #python $fileName  200  250 $i &
    #python $fileName  250  301 $i &
    #wait
    #python $fileName  300  350 $i &
    #python $fileName  350  400 $i &
    #python $fileName  400  450 $i &
    #python $fileName  450  500 $i &
    #python $fileName  500  550 $i &
    #python $fileName  550  601 $i &
    wait
done
