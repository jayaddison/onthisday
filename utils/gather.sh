#!/bin/sh

BASE=`dirname $0`

for month in `seq 1 12`;
do
	monthidx=$((month - 1));
	monthdir=${BASE}/data/${monthidx};
	monthname=`date -d 2000-${month}-01 +%B`;

	mkdir -p ${monthdir};
	for day in `cal ${month} 2000 | tail -n +3`;
	do
		dayfile=${monthdir}/${day}.json;

		if [ ! -f ${dayfile} ];
		then
			python extract.py ${monthname}_${day} > ${dayfile};
			sleep 0.5;
		fi;
	done;
done;
