import type {User} from '../types/domain';
export function readUser():User|null{try{return JSON.parse(localStorage.getItem('spectrum-user')||'null')}catch{return null}}
export function saveSession(token:string,user:User){localStorage.setItem('spectrum-token',token);localStorage.setItem('spectrum-user',JSON.stringify(user))}
export function clearSession(){localStorage.removeItem('spectrum-token');localStorage.removeItem('spectrum-user')}
