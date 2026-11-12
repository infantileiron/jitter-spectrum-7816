import {request,post} from './client';import type {Window} from '../types/domain';
export const list=()=>request<Window[]>('/windows');
export const create=(data:unknown)=>post<Window>('/windows',data);
