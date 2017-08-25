# $1 is the port, $2 the number of repetitions, $3 is the number of trials, $4 is the number of agents, and $5$ is the number of defense npcs

# ./HFO/bin/HFO --offense-agents=3 --defense-npcs=1 --fullstate --headless --trials=33100 --port=$1 --frames-per-trial=200
for I in $(seq 1 1 $2)
do
./HFO/bin/HFO --no-logging --offense-agents=$4 --defense-npcs=$5 --fullstate --headless --trials=$3 --port=$1 --frames-per-trial=200
done
