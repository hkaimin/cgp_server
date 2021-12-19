echo $1 #接受者
echo $2 #type
echo $3	#value
echo $4 #时间戳
echo $5	#index

toStr=$1
typeInt=$2
valueInt=$3
timeStr=$4
indexInt=$5
logName="log/${timeStr}_${toStr}_${typeInt}_app.log"
# echo ${logName}
node web3test/app.js ${toStr} ${typeInt} ${valueInt} ${timeStr} ${indexInt} > ${logName}