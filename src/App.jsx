
import React, { useEffect, useState } from 'react';

import Sidebar from './components/Sidebar';
import Header from './components/Header';
import RequirementModal from './components/RequirementModal';

import Dashboard from './pages/Dashboard';
import Requirements from './pages/Requirements';
import Tests from './pages/Tests';
import Traceability from './pages/Traceability';

import { api } from './api';

const meta = {
  dashboard: [
    'Огляд',
    'Ключові показники та активність проєкту',
  ],
  requirements: [
    'Вимоги',
    'Управління вимогами системи',
  ],
  tests: [
    'Тест-кейси',
    'Каталог тестових сценаріїв',
  ],
  trace: [
    'Матриця трасування',
    'Контроль покриття вимог тестами',
  ],
};

export default function App() {
  const [page, setPage] = useState('dashboard');
  const [menu, setMenu] = useState(false);
  const [modal, setModal] = useState(undefined);

  const [requirements, setRequirements] = useState([]);
  const [tests, setTests] = useState([]);
  const [links, setLinks] = useState([]);

  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  // Завантаження даних із Django API
  useEffect(() => {
    let cancelled = false;

    async function loadData() {
      try {
        setLoading(true);
        setError('');

        const [r, t, l] = await Promise.all([
          api.requirements(),
          api.tests(),
          api.links(),
        ]);

        console.log('Вимоги з Django:', r);
        console.log('Тести з Django:', t);
        console.log("Зв'язки з Django:", l);

        if (!cancelled) {
          setRequirements(r);
          setTests(t);
          setLinks(l);
        }
      } catch (e) {
        console.error('Помилка Django API:', e);

        if (!cancelled) {
          setError(
            `${e.message} — перевірте підключення до Django API.`
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadData();

    return () => {
      cancelled = true;
    };
  }, []);

  // Виконання операцій із відображенням помилок
  async function execute(action) {
    setBusy(true);
    setError('');

    try {
      await action();
      return true;
    } catch (e) {
      console.error('Помилка операції:', e);
      setError(e.message);
      return false;
    } finally {
      setBusy(false);
    }
  }

  // Створення або редагування вимоги
  async function saveRequirement(form) {
    const ok = await execute(async () => {
      if (modal) {
        const updated = await api.updateRequirement(
          modal.id,
          form
        );

        setRequirements((previous) =>
          previous.map((item) =>
            item.id === modal.id ? updated : item
          )
        );
      } else {
        const created = await api.createRequirement(form);

        setRequirements((previous) => [
          created,
          ...previous,
        ]);
      }
    });

    if (ok) {
      setModal(undefined);
    }
  }

  // Видалення вимоги
  async function deleteRequirement(item) {
    if (!window.confirm(
      `Видалити вимогу «${item.title}»?`
    )) {
      return;
    }

    const ok = await execute(async () => {
      await api.deleteRequirement(item.id);
    });

    if (ok) {
      setRequirements((previous) =>
        previous.filter((x) => x.id !== item.id)
      );

      setLinks((previous) =>
        previous.filter(
          (link) =>
            String(link.requirementId ?? link.requirement) !==
            String(item.id)
        )
      );
    }
  }

  // Створення зв'язку між вимогою і тестом
  async function addLink(item) {
    await execute(async () => {
      const created = await api.createLink(item);

      setLinks((previous) => [
        ...previous,
        created,
      ]);
    });
  }

  // Видалення зв'язку
  async function removeLink(id) {
    if (!window.confirm("Видалити зв'язок?")) {
      return;
    }

    const ok = await execute(async () => {
      await api.deleteLink(id);
    });

    if (ok) {
      setLinks((previous) =>
        previous.filter((item) => item.id !== id)
      );
    }
  }

  return (
    <div className="app-shell">
      <Sidebar
        page={page}
        navigate={setPage}
        opened={menu}
        close={() => setMenu(false)}
      />

      <div className="main-area">
        <Header
          title={meta[page][0]}
          subtitle={meta[page][1]}
          openMenu={() => setMenu(true)}
        />

        <main className="content">
          {error && (
            <div className="alert" role="alert">
              {error}

              <button
                onClick={() => setError('')}
                aria-label="Закрити повідомлення"
              >
                ×
              </button>
            </div>
          )}

          {loading ? (
            <div className="loading">
              Завантаження даних...
            </div>
          ) : (
            <>
              {page === 'dashboard' && (
                <Dashboard
                  requirements={requirements}
                  tests={tests}
                  links={links}
                  navigate={setPage}
                />
              )}

              {page === 'requirements' && (
                <Requirements
                  requirements={requirements}
                  links={links}
                  onAdd={() => setModal(null)}
                  onEdit={setModal}
                  onDelete={deleteRequirement}
                />
              )}

              {page === 'tests' && (
                <Tests
                  tests={tests}
                  links={links}
                />
              )}

              {page === 'trace' && (
                <Traceability
                  requirements={requirements}
                  tests={tests}
                  links={links}
                  addLink={addLink}
                  removeLink={removeLink}
                  busy={busy}
                />
              )}
            </>
          )}
        </main>

        <footer className="footer">
          © 2026 TraceFlow · Навчальний проєкт
          <span>Вебсистеми трасування</span>
        </footer>
      </div>

      {modal !== undefined && (
        <RequirementModal
          item={modal}
          onClose={() => setModal(undefined)}
          onSave={saveRequirement}
          busy={busy}
        />
      )}
    </div>
  );
}
