export const number=(v:number|null|undefined,d=3)=>v==null?'不适用':v.toFixed(d);
export const date=(v:string)=>new Date(v).toLocaleString('zh-CN',{hour12:false});
