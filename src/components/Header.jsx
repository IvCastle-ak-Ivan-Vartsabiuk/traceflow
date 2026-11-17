import React from 'react';
import { Menu, Bell, CircleHelp } from 'lucide-react';
export default function Header({ title, subtitle, openMenu }) {
 return <header className="header"><div className="header-left"><button onClick={openMenu} className="icon-btn mobile-menu" aria-label="Відкрити меню"><Menu size={22}/></button><div><div className="crumbs">Робочий простір <span>/</span> {title}</div><h1>{title}</h1><p>{subtitle}</p></div></div><div className="header-right"><button className="icon-btn header-icon" title="Демонстраційний режим" aria-label="Довідка" onClick={()=>alert('Демоінтерфейс. Дані надає локальний JSON Server.') }><CircleHelp size={19}/></button><button className="icon-btn header-icon" title="Сповіщення" aria-label="Сповіщення" onClick={()=>alert('Нових сповіщень немає.') }><Bell size={19}/></button><div className="avatar" title="Демо-користувач">AD</div></div></header>;
}
