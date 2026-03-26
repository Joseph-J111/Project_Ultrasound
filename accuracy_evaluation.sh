#!/bin/bash  

#Simple bash that calculates average and variance on 100 reads of $FILE

FILE="/dev/DUsound"
for ((i=0 ; i<100 ; i++))
do
  VALUES[$i]=$(od -An -t d4 -N4 "$FILE" | tr -d ' ')
  echo "Valeur $i : ${VALUES[$i]}"
done

SUM=0
for val in "${VALUES[@]}"; do
  SUM=$((SUM + val))
done
MOYENNE=$((SUM / 100))

SQUARES=0
for val in "${VALUES[@]}"; do
  CARRE=$((val * val))
  SQUARES=$((SQUARES + CARRE))
done

MOYENNE_CARRES=$((SQUARES / 100))
VARIANCE=$((MOYENNE_CARRES - (MOYENNE * MOYENNE)))

echo "Moyenne (entière) : $MOYENNE"
echo "Variance (entière) : $VARIANCE"

