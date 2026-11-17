import React from 'react';
import { LayoutDashboard, ListChecks, FlaskConical, GitBranch, Layers3, X } from 'lucide-react';
const menu = [
  ['dashboard','Огляд', LayoutDashboard],
  ['requirements','Вимоги', ListChecks],
  ['tests','Тест-кейси', FlaskConical],
  ['trace','Матриця трасування', GitBranch],
];
export default function Sidebar({ page, navigate, opened, close }) {
 return <><div className={'sidebar-overlay '+(opened?'visible':'')} onClick={close}/>
  <aside className={'sidebar '+(opened?'open':'')}>
   <div className="brand"><div className="brand-mark"><Layers3 size={22}/></div><div><strong>TraceFlow</strong><small>Requirements QA</small></div><button className="mobile-close icon-btn" aria-label="Закрити меню" onClick={close}><X size={19}/></button></div>
   <div className="nav-caption">РОБОЧИЙ ПРОСТІР</div>
   <nav aria-label="Головна навігація">{menu.map(([key, title, Icon])=><button key={key} className={'nav-item '+(page===key?'active':'')} onClick={()=>{navigate(key);close();}}><Icon size={18}/><span>{title}</span></button>)}</nav>
   <div className="sidebar-bottom"><div className="help-icon">?</div><div><strong>Навчальний проєкт</strong><small> Вебсистема трасування</small></div></div>
  </aside></>;
}
