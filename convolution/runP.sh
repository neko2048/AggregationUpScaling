#!/bin/bash
fileName=gaussianConvolveLargeW.py #gaussianConvolveW.py
for i in 16
do 
    python $fileName   0   1   $i & wait
    #python $fileName   1  50   $i &
    #python $fileName  50 100   $i &
    #python $fileName 100 150   $i &
    #python $fileName 150 200   $i &
    #python $fileName 200 250   $i &
    #python $fileName 250 300   $i &
    #python $fileName 300 353   $i &
    python $fileName   1 100   $i &
    python $fileName 100 200   $i &
    python $fileName 200 300   $i &
    python $fileName 300 400   $i &
    python $fileName 400 500   $i &
    python $fileName 500 625   $i &
    wait
done
