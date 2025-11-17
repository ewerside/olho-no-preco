export function initSearchForm(rootElement, onSearch) {
  const form = document.createElement('form');
  const input = document.createElement('input');
  input.type = 'search';
  input.placeholder = 'Digite o nome do produto ou categoria (ex.: arroz, higiene...)';
  input.autocomplete = 'off';

  const button = document.createElement('button');
  button.type = 'submit';
  button.textContent = 'Buscar';

  form.append(input, button);

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    onSearch(input.value);
  });

  rootElement.append(form);

  function setLoading(isLoading) {
    button.disabled = isLoading;
    button.textContent = isLoading ? 'Buscando...' : 'Buscar';
  }

  return { setLoading, focus: () => input.focus() };
}
