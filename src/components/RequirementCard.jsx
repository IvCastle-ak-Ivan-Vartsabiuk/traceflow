import React from 'react';
import {Pencil,Trash2} from 'lucide-react';
export const statuses={draft:['Чернетка','draft'],active:['Активна','active'],completed:['Виконана','completed']};
export const priorities={low:['Низький','low'],medium:['Середній','medium'],high:['Високий','high']};
export default function RequirementCard({item,testCount,onEdit,onDelete}){
 const [s,sc]=statuses[item.status]||[item.status,'draft'];const [priority,pc]=priorities[item.priority]||[item.priority,'medium'];
 return <article className="req-card"><div className="req-first"><span className="req-id">{item.code||`REQ-${String(item.id).padStart(3,'0')}`}</span><span className={'pill '+sc}>{s}</span></div><h3>{item.title}</h3><p>{item.description||'Опис відсутній'}</p><div className="card-bottom"><div><span className={'priority-dot '+pc}></span>{priority} · {testCount} тестів</div><div className="card-actions"><button onClick={()=>onEdit(item)} aria-label={'Редагувати '+item.title}><Pencil size={16}/></button><button onClick={()=>onDelete(item)} aria-label={'Видалити '+item.title}><Trash2 size={16}/></button></div></div></article>;
}
