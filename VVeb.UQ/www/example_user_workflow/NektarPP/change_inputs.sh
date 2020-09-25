#!/bin/bash

adv=`head -n 1 input_mc.csv`
poly=`head -n 2 input_mc.csv | tail -n 1`
printf -v poly_int '%d' "$poly" 2>/dev/null

command="sed 's/advx            = 2.0/advx            = "$adv"/g' ADR_conditions.xml | sed 's/NUMMODES=\"5\"/NUMMODES=\""$poly_int"\"/g' > tmp.txt"
sh -c "$command"
mv tmp.txt ADR_conditions.xml
