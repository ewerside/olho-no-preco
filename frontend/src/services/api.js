const DEFAULT_API_URL = 'http://127.0.0.1:8000';
const API_BASE_URL = window.API_BASE_URL || DEFAULT_API_URL;

async function handleResponse(response) {
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || 'Erro ao consultar a API.');
  }
  return response.json();
}

export async function searchProducts(term = '') {
  const params = new URLSearchParams();
  if (term.trim()) {
    params.append('query', term.trim());
  }
  const url = `${API_BASE_URL}/products/search${params.toString() ? `?${params}` : ''}`;
  const response = await fetch(url);
  return handleResponse(response);
}
