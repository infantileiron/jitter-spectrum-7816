import {useState} from 'react';
import type {Workspace} from '../stores/workspace';
import type {BackfillResult,Correction,Point} from '../types/domain';
import {PageHeading} from '../components/common/PageHeading';
import {SignalTrace} from '../components/SignalTrace';
import {Notice} from '../components/common/Notice';
import {create,backfill} from '../api/datasets';
import {useAsync} from '../hooks/useAsync';
import {number,date} from '../utils/format';
export function Datasets({data,canWrite,refresh}:{data:Workspace;canWrite:boolean;refresh:()=>Promise<void>}){
 const [selected,setSelected]=useState(''),[link,setLink]=useState(''),[name,setName]=useState(''),[source,setSource]=useState('jitter_observations.json'),[text,setText]=useState('');
 const [late,setLate]=useState(''),[conflicts,setConflicts]=useState<Correction[]|null>(null),[pending,setPending]=useState<Point[]|null>(null),[summary,setSummary]=useState<BackfillResult|null>(null);
 const ds=data.datasets.find(d=>d.id===selected)||data.datasets[0];
 const links=ds?[...new Set(ds.points.map(p=>p.link_id))].sort():[];
 const active=links.includes(link)?link:links[0];
 const rows=(ds?.points.filter(p=>p.link_id===active)||[]).sort((a,b)=>a.time_minutes-b.time_minutes);
 const batches=data.backfills.filter(b=>b.dataset_id===ds?.id);
 const task=useAsync(),fill=useAsync();
 async function submit(points:Point[],confirm:boolean){
  const res=await backfill(ds!.id,{points,confirm_corrections:confirm});
  if(res.status==='needs_confirmation'){setConflicts(res.corrections);setPending(points);setSummary(null);return}
  setConflicts(null);setPending(null);setSummary(res);setLate('');await refresh();
 }
 return <><PageHeading label="02 / TIMESTAMPED OBSERVATIONS" title="每一个数，都带着采样时刻。">时间为分钟，抖动值为ms。<br/>同链路重复时间拒绝，输入乱序会按时间稳定排序。</PageHeading>
 <section className="paper"><div className="section-heading"><h2>链路离线观测</h2><div className="filters"><select aria-label="选择观测集" value={ds?.id||''} onChange={e=>{setSelected(e.target.value);setLink('');setConflicts(null);setSummary(null)}}>{data.datasets.map(d=><option key={d.id} value={d.id}>{d.name}</option>)}</select><select aria-label="观测链路" value={active||''} onChange={e=>setLink(e.target.value)}>{links.map(l=><option key={l}>{l}</option>)}</select></div></div>
 {ds?<><div className="data-caption"><b>{rows.length}点 / {active}</b><span>{ds.source}</span><span>数据版本 v{ds.version}</span><span>无补零或插值</span></div><SignalTrace points={rows.map(p=>({...p,residual_ms:0}))}/><div className="table-scroll"><table><thead><tr><th>序号</th><th>链路</th><th>时间 / 分钟</th><th>抖动 / ms</th></tr></thead><tbody>{rows.slice(0,30).map((p,i)=><tr key={p.time_minutes}><td>{i+1}</td><td>{p.link_id}</td><td>{number(p.time_minutes,6)}</td><td>{number(p.jitter_ms,6)}</td></tr>)}</tbody></table></div><p className="caption">表格预览30点，图线与算法使用窗口内全量实际观测。线段连接仅为阅读，不代表重采样。</p></>:<Notice>请导入带link_id、time_minutes和jitter_ms的观测，保留真实时间间隔。</Notice>}</section>
 {canWrite&&ds&&<section className="paper"><h2>链路补采 · 向原观测集追加迟到记录</h2><p className="caption">按链路与采样时刻识别同一点：新时刻追加，同值重复投递跳过不新增，异值修正需逐项确认。目标：{ds.name}（当前 v{ds.version}）。</p>
 <form className="grid-form" onSubmit={e=>{e.preventDefault();fill.execute(()=>submit(JSON.parse(late),false))}}><label className="wide">补采点JSON<textarea rows={4} required value={late} onChange={e=>setLate(e.target.value)} placeholder={'[{"link_id":"BY-01","time_minutes":480,"jitter_ms":12.6}, …]'}/></label>{fill.error&&<Notice error>{fill.error}</Notice>}<button disabled={fill.busy||!!conflicts}>核查并补采</button></form>
 {conflicts&&<><Notice error>{conflicts.length}处同链路同时刻的异值修正，尚未写入。请逐项核对，确认后才会覆盖原值。</Notice><div className="table-scroll"><table><thead><tr><th>链路</th><th>时间 / 分钟</th><th>原值 / ms</th><th>修正值 / ms</th></tr></thead><tbody>{conflicts.map(c=><tr key={c.link_id+c.time_minutes}><td>{c.link_id}</td><td>{number(c.time_minutes,6)}</td><td>{number(c.old_jitter_ms,6)}</td><td><b>{number(c.new_jitter_ms,6)}</b></td></tr>)}</tbody></table></div><div className="button-row"><button disabled={fill.busy} onClick={()=>fill.execute(()=>submit(pending!,true))}>确认修正并写入</button><button className="secondary" onClick={()=>{setConflicts(null);setPending(null)}}>放弃本次补采</button></div></>}
 {summary?.status==='applied'&&<Notice>已写入：新增{summary.added}点，跳过重复{summary.duplicates}点，确认修正{summary.corrections.length}点；数据版本推进到 v{summary.dataset_version}。{summary.affected_windows?.length?`受影响窗口：${summary.affected_windows.join('、')}，${summary.stale_runs}条旧结果已标过期，可在周期与幅相页重算。`:'补采点不在任何已固定窗口内，既有结果不受影响。'}</Notice>}
 {summary?.status==='noop'&&<Notice>重复投递：{summary.duplicates}点均已存在，未新增观测，数据版本不变。</Notice>}</section>}
 {ds&&<section className="paper"><h2>补采记录</h2>{batches.length?<div className="table-scroll"><table><thead><tr><th>时间</th><th>操作者</th><th>新增</th><th>重复跳过</th><th>确认修正</th><th>数据版本</th></tr></thead><tbody>{batches.map(b=><tr key={b.id}><td>{date(b.created_at)}</td><td>{b.actor}</td><td>{b.added}</td><td>{b.duplicates}</td><td>{b.corrections.length ? <details><summary>{b.corrections.length}处</summary>{b.corrections.map(c=><small key={c.link_id+c.time_minutes}>{c.link_id} @{number(c.time_minutes,3)}：{number(c.old_jitter_ms,4)}→{number(c.new_jitter_ms,4)}</small>)}</details>:0}</td><td>v{b.dataset_version}</td></tr>)}</tbody></table></div>:<p className="caption">尚无补采。迟到记录会直接追加到原观测集，不必另建新集。</p>}</section>}
 {canWrite&&<section className="paper"><h2>导入离线观测</h2><form className="grid-form" onSubmit={e=>{e.preventDefault();task.execute(async()=>{await create({name,source,points:JSON.parse(text)});setName('');setText('');await refresh()})}}><label>观测集名称<input required minLength={2} value={name} onChange={e=>setName(e.target.value)}/></label><label>来源文件名<input value={source} onChange={e=>setSource(e.target.value)}/></label><label className="wide">观测点JSON<textarea rows={4} required value={text} onChange={e=>setText(e.target.value)} placeholder={'[{"link_id":"BY-01","time_minutes":0,"jitter_ms":12.5}, …]'}/></label>{task.error&&<Notice error>{task.error}</Notice>}<button disabled={task.busy}>核查并导入</button></form></section>}</>
}
