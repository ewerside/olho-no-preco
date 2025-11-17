import { createProductCard } from './productCard.js';

export function renderStatus(root, message, variant = 'info') {
  root.innerHTML = '';
  const box = document.createElement('div');
  box.className = `status-message ${variant === 'error' ? 'error-message' : ''}`;
  box.textContent = message;
  root.append(box);
}

export function renderResults(root, results) {
  root.innerHTML = '';
  if (!results.length) {
    renderStatus(root, 'Nenhum produto encontrado com esse termo. Tente algo como \"arroz\".');
    return;
  }

  results.forEach((result) => {
    root.append(createProductCard(result));
  });
}
