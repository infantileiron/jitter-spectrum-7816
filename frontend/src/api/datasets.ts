import {request,post} from './client';import type {Dataset,Backfill,BackfillResult} from '../types/domain';
export const list=()=>request<Dataset[]>('/datasets');
export const create=(data:unknown)=>post<Dataset>('/datasets',data);
export const backfill=(id:string,data:unknown)=>post<BackfillResult>('/datasets/'+id+'/backfill',data);
export const backfills=()=>request<Backfill[]>('/datasets/backfills');
