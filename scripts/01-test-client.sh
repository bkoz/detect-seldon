#!/bin/bash

# $RANDOM returns a different random integer at each invocation.
# Nominal range: 0 - 32767 (signed 16-bit integer).

# RANGE defines the largest random rumber

RANGE=100
MAXCOUNT=100
count=1

function doCurls {
	r=$1
	for j in `seq $r`
	do
		python3 01-test-detection.py
	done
}

echo
echo "$MAXCOUNT iterations:"
echo "---------------"
while [ "$count" -le $MAXCOUNT ]      # Generate 10 ($MAXCOUNT) random integers.
do
  number=$RANDOM
  let "number %= $RANGE"
  echo $number curls
  doCurls $number
  let "count += 1"  # Increment count.
  let x=$RANDOM%$RANGE
  echo "sleep for $x"
  sleep $x
done
