#/usr/bin/env bash

# path to fast forward #
FF_PATH="/home/perry/Documents/Research/ff/ff"

# find optimal plan using fd on input domain and problem #
${FF_PATH} -o $1 -f $2|grep -E "[0-9][0-9]*:"|sed 's/^.*: //' 
