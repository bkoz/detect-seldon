#!/bin/bash

# $RANDOM returns a different random integer at each invocation.
# Nominal range: 0 - 32767 (signed 16-bit integer).

# RANGE defines the largest random rumber

ROUTE_NAME=detection-redhat
RANGE=100
MAXCOUNT=100
count=1

function doCurls {
	r=$1
	for j in `seq $r`
	do 
		curl -X POST $(oc get route ${ROUTE_NAME} -o jsonpath='{.spec.host}')/api/v1.0/predictions -H 'Content-Type: application/json' -d '{ "data": { "ndarray": [[5.1, 3.5, 1.4, 0.2]] } }'
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

#
# curl -X POST iris-model-default-ml-mon.apps.ocp.2ff8.sandbox379.opentlc.com/api/v1.0/predictions -H 'Content-Type: application/json' -d '{ "data": { "ndarray": [[5.1, 3.5, 1.4, 0.2]] } }'
# {"data":{"names":["t:0","t:1","t:2"],"ndarray":[[0.8780303050242898,0.12195890005075304,1.0794924957147601e-05]]},"meta":{}}
#
