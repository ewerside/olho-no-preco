const currencyFormatter = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
});

const dateFormatter = new Intl.DateTimeFormat('pt-BR', {
  dateStyle: 'short',
  timeStyle: 'short',
});

function formatCurrency(value) {
  return currencyFormatter.format(value);
}

function buildStatCard(label, value, detail) {
  const wrapper = document.createElement('div');
  wrapper.className = 'stat-card';

  const labelEl = document.createElement('span');
  labelEl.textContent = label;

  const valueEl = document.createElement('strong');
  valueEl.textContent = value;

  const detailEl = document.createElement('div');
  detailEl.className = 'stat-detail';
  detailEl.textContent = detail;

  wrapper.append(labelEl, valueEl, detailEl);
  return wrapper;
}

function buildPriceItem(entry, isBest) {
  const item = document.createElement('div');
  item.className = `price-item${isBest ? ' best' : ''}`;

  const header = document.createElement('header');
  header.textContent = `${entry.market.name} (${entry.market.neighborhood})`;

  const value = document.createElement('div');
  value.className = 'value';
  value.textContent = formatCurrency(entry.price);

  const notes = document.createElement('small');
  const tags = [];
  if (entry.promo) tags.push('Promoção ativa');
  if (entry.stock_status) tags.push(entry.stock_status);
  notes.textContent = `${tags.join(' • ') || 'Preço regular'} · Atualizado em ${dateFormatter.format(
    new Date(entry.last_updated)
  )}`;

  const extra = document.createElement('small');
  if (entry.notes) {
    extra.textContent = entry.notes;
  }

  item.append(header, value, notes);
  if (entry.notes) {
    item.append(extra);
  }
  return item;
}

export function createProductCard(result) {
  const card = document.createElement('article');
  card.className = 'product-card';

  const header = document.createElement('div');
  header.className = 'product-header';

  const title = document.createElement('h3');
  title.textContent = result.product.name;

  const subtitle = document.createElement('span');
  subtitle.textContent = `${result.product.brand || 'Marca diversa'} · ${result.product.unit}`;

  const badge = document.createElement('span');
  badge.className = 'badge';
  badge.textContent = result.product.category;

  header.append(title, subtitle, badge);

  const statsGrid = document.createElement('div');
  statsGrid.className = 'stats-grid';

  statsGrid.append(
    buildStatCard(
      'Mais barato',
      formatCurrency(result.stats.min_price),
      result.stats.min_price_market.name
    ),
    buildStatCard(
      'Mais caro',
      formatCurrency(result.stats.max_price),
      result.stats.max_price_market.name
    ),
    buildStatCard('Média', formatCurrency(result.stats.avg_price), 'base em ' + result.stats.market_count + ' mercados'),
    buildStatCard('Variação', formatCurrency(result.stats.price_spread), 'diferença entre extremos')
  );

  const priceList = document.createElement('div');
  priceList.className = 'price-list';

  const ordered = [...result.prices].sort((a, b) => a.price - b.price);
  ordered.forEach((entry, index) => {
    priceList.append(buildPriceItem(entry, index === 0));
  });

  card.append(header, statsGrid, priceList);
  return card;
}
