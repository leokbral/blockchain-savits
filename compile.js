const fs=require('fs'), path=require('path'), solc=require('solc');
const dir=process.argv[2]||'contracts/contracts';
const out=process.argv[3]||'build';
const sources={};
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.sol')))
  sources[f]={content:fs.readFileSync(path.join(dir,f),'utf8')};
const input={language:'Solidity',sources,settings:{
  evmVersion:'paris',
  optimizer:{enabled:true,runs:200},
  outputSelection:{'*':{'*':['abi','evm.bytecode.object','evm.deployedBytecode.object','metadata']}}}};
const o=JSON.parse(solc.compile(JSON.stringify(input)));
let fatal=false;
(o.errors||[]).forEach(e=>{console.error(e.severity.toUpperCase()+': '+e.formattedMessage.trim());if(e.severity==='error')fatal=true;});
if(fatal){process.exit(1);}
fs.mkdirSync(out,{recursive:true});
const arts={};
for(const f in o.contracts) for(const c in o.contracts[f]){
  arts[c]={abi:o.contracts[f][c].abi,bytecode:'0x'+o.contracts[f][c].evm.bytecode.object,
           deployedSize:o.contracts[f][c].evm.deployedBytecode.object.length/2};
}
fs.writeFileSync(path.join(out,'artifacts.json'),JSON.stringify(arts,null,1));
console.log('compilado:',Object.keys(arts).join(', '),'| solc',solc.version());
for(const c in arts) console.log('  ',c,'runtime size:',arts[c].deployedSize,'bytes');
