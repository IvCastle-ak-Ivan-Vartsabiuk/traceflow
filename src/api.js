
const base = 'http://127.0.0.1:8000/api';

async function request(path, options = {}) {
  const response = await fetch(`${base}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });


  if (!response.ok) {
    throw new Error(`Помилка сервера (${response.status})`);
  }

  return response.status === 204 ? null : response.json();
}

export const api = {
  requirements: () => request('/requirements/'),

  tests: () => request('/test-cases/'),

  links: () => request('/trace-links/'),

  createRequirement: (item) =>
    request('/requirements/', {
      method: 'POST',
      body: JSON.stringify(item),
    }),

  updateRequirement: (id, item) =>
    request(`/requirements/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(item),
    }),

  deleteRequirement: (id) =>
    request(`/requirements/${id}/`, {
      method: 'DELETE',
    }),

  createLink: (item) =>
    request('/trace-links/', {
      method: 'POST',
      body: JSON.stringify(item),
    }),

  deleteLink: (id) =>
    request(`/trace-links/${id}/`, {
      method: 'DELETE',
    }),
};
