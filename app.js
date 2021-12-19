// var arguments = process.argv.splice(1);
var options = process.argv;

// options[2] #接受者
// options[3] #type
// options[4] #value
// options[5] #时间戳
// options[6] #index

// print process.argv
process.argv.forEach(function (val, index, array) {
  console.log(index + ': ' + val);
});

var address = "0xa9e75f8838c7173412f229a7cd13a6b6e0fe6e39";
var sender = "0x210729036108b7dd19bba5141e181a47a619a46f";
var netUrl = "https://data-seed-prebsc-1-s1.binance.org:8545";
var netDes = "Binance Smart Chain testnet";
var chainId = 97;
var key = "c9272ab7edd9f7a77c8f281069a817574dec743867c21270e2a7da098179d5d5";


var Web3 = require("web3");
//创建web3对象
var web3 = new Web3();
// 连接到以太坊节点
web3.setProvider(new Web3.providers.HttpProvider(netUrl));
// var version = web3.version.node;
// console.log(web3);

var abi = [{
    "constant": true,
    "inputs": [
    {
        "internalType": "address",
        "name": "_owner",
        "type": "address"
    }
    ],
    "name": "balanceOf",
    "outputs": [
    {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
    }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
},{
    "constant": false,
    "inputs": [
    {
        "internalType": "address",
        "name": "_to",
        "type": "address"
    },
    {
        "internalType": "uint256",
        "name": "_value",
        "type": "uint256"
    }
    ],
    "name": "transfer",
    "outputs": [
    {
        "internalType": "bool",
        "name": "",
        "type": "bool"
    }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
}];
 

var metacoin = new web3.eth.Contract(abi,address);
// var account = web3.eth.accounts.privateKeyToAccount("");
// console.log("account-----",account);

metacoin.methods.balanceOf(sender).call({from: sender}, function(error, result){
    console.log("function---metacoin-balanceOf error-",error)
    console.log("function---metacoin-balanceOf result-",result)
});



var Tx = require('ethereumjs-tx').Transaction;

const privateKey = Buffer.from(
  key,
  'hex',
)
web3.eth.getTransactionCount(sender,function(error,result){
	console.log("getTransactionCount----result-",result);
	var rawTx = {}
	if(options[3] == 1){
		rawTx = {
		  nonce:result,
		  gasPrice: '0x2540be400',
		  gasLimit: '0x186a0',
		  gas:'0xc350',
		  to:address,
		  data: metacoin.methods.transfer(options[2],options[4]).encodeABI()
		}
	}
	
	console.log("data----",metacoin.methods.transfer(options[2],options[4]).encodeABI())

	// var BSC_FORK = Common.forCustomChain(
	//     'mainnet',
	//     {
	//         name: 'Binance Smart Chain Mainnet',
	//         networkId: 56,
	//         chainId: 56,
	//         url: 'https://bsc-dataseed.binance.org/'
	//     },
	//     'istanbul',
	// );
	var Common = require('ethereumjs-common').default;
	var BSC_FORK = Common.forCustomChain(
	    'ropsten',
	    {
	        name: netDes,
	        networkId: chainId,
	        chainId: chainId,
	        url: netUrl
	    },
	    'istanbul',
	);

	var tx = new Tx(rawTx,{ 'common': BSC_FORK });//{ 'common': BSC_FORK }
	tx.sign(privateKey);

	var serializedTx = tx.serialize();
	console.log("serializedTx----",serializedTx)
	console.log("serializedTx.toString('hex')----",serializedTx.toString('hex'))
	web3.eth.sendSignedTransaction("0x" + serializedTx.toString('hex'), function(err, hash) {
	  if (!err){
	  	console.log("sendSignedTransaction----hash ",hash); 
	  }else{
	  	console.log("sendSignedTransaction----err ",err);
	  }
		
	});
});








