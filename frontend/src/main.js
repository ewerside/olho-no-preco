import { initSearchForm } from './components/searchForm.js';
import { renderResults, renderStatus } from './components/productList.js';
import { searchProducts } from './services/api.js';

const searchRoot = document.getElementById('search-root');
const resultsRoot = document.getElementById('results');
const resultsHint = document.getElementById('results-hint');

const searchForm = initSearchForm(searchRoot, handleSearch);
renderStatus(resultsRoot, 'Pesquise por um item para ver o comparativo de preços.');

async function handleSearch(rawTerm) {
  const term = rawTerm.trim();
  searchForm.setLoading(true);
  renderStatus(resultsRoot, 'Carregando resultados...');

  try {
    const data = await searchProducts(term);
    if (!term) {
      resultsHint.textContent = 'Mostrando todos os produtos disponíveis.';
    } else {
      resultsHint.textContent = `Resultados para "${term}"`;
    }
    renderResults(resultsRoot, data);
  } catch (error) {
    console.error(error);
    renderStatus(
      resultsRoot,
      'Não foi possível buscar os produtos. Verifique se a API está rodando em http://127.0.0.1:8000.',
      'error'
    );
  } finally {
    searchForm.setLoading(false);
  }
}
