import { suggestMarkets, suggestProducts } from '../services/api.js';

function createInput(config) {
  const group = document.createElement('label');
  group.className = 'form-group';

  const span = document.createElement('span');
  span.textContent = config.label;

  const wrapper = document.createElement('div');
  wrapper.className = 'input-wrapper';

  const field = config.multiline ? document.createElement('textarea') : document.createElement('input');
  field.name = config.name;
  if (!config.multiline) {
    field.type = config.type || 'text';
  }
  field.placeholder = config.placeholder || '';
  field.required = Boolean(config.required);
  field.autocomplete = 'off';

  wrapper.append(field);

  if (config.suggestions) {
    const listWrapper = document.createElement('div');
    listWrapper.className = 'suggestion-panel hidden';
    const ul = document.createElement('ul');
    listWrapper.append(ul);
    wrapper.append(listWrapper);
    attachSuggestionBehavior(field, listWrapper, config.suggestions.fetch, config.suggestions.template);
  }

  group.append(span, wrapper);
  return { group, field };
}

function attachSuggestionBehavior(input, container, fetcher, template) {
  let debounceId;

  const renderItems = (items) => {
    const list = container.querySelector('ul');
    list.innerHTML = '';
    if (!items.length) {
      container.classList.add('hidden');
      return;
    }

    items.forEach((item) => {
      const li = document.createElement('li');
      li.textContent = template ? template(item) : item.name;
      li.addEventListener('mousedown', (event) => {
        event.preventDefault();
        input.value = item.name;
        container.classList.add('hidden');
      });
      list.append(li);
    });

    container.classList.remove('hidden');
  };

  input.addEventListener('input', () => {
    const term = input.value.trim();
    if (!term) {
      container.classList.add('hidden');
      return;
    }
    clearTimeout(debounceId);
    debounceId = setTimeout(async () => {
      try {
        const items = await fetcher(term);
        renderItems(items);
      } catch (error) {
        container.classList.add('hidden');
      }
    }, 200);
  });

  input.addEventListener('blur', () => {
    setTimeout(() => container.classList.add('hidden'), 150);
  });
}

function optional(value) {
  if (!value) return null;
  const trimmed = value.trim();
  return trimmed.length ? trimmed : null;
}

export function initEntryForm(rootElement, onSubmit) {
  const form = document.createElement('form');
  form.className = 'entry-form';

  const statusBox = document.createElement('div');
  statusBox.className = 'entry-message hidden';

  const productTitle = document.createElement('h3');
  productTitle.textContent = 'Product details';

  const productGrid = document.createElement('div');
  productGrid.className = 'form-grid';
  const productName = createInput({
    label: 'Product name',
    name: 'product_name',
    placeholder: 'e.g., Rice 5kg',
    required: true,
    suggestions: {
      fetch: suggestProducts,
      template: (item) => `${item.name} · ${item.brand || 'No brand'}`,
    },
  });
  const productBrand = createInput({ label: 'Brand', name: 'product_brand', placeholder: 'e.g., Camil' });
  const productUnit = createInput({ label: 'Unit', name: 'product_unit', placeholder: 'kg, L, pack' });
  const productCategory = createInput({ label: 'Category', name: 'product_category', placeholder: 'Grocery' });
  const productDescription = createInput({
    label: 'Description',
    name: 'product_description',
    placeholder: 'Optional details',
    multiline: true,
  });
  productGrid.append(
    productName.group,
    productBrand.group,
    productUnit.group,
    productCategory.group,
    productDescription.group,
  );

  const marketTitle = document.createElement('h3');
  marketTitle.textContent = 'Market details';

  const marketGrid = document.createElement('div');
  marketGrid.className = 'form-grid';
  const marketName = createInput({
    label: 'Market name',
    name: 'market_name',
    placeholder: 'e.g., Super Bom Preço',
    required: true,
    suggestions: {
      fetch: suggestMarkets,
      template: (item) => `${item.name} · ${item.city || ''}`.trim(),
    },
  });
  const neighborhood = createInput({ label: 'Neighborhood', name: 'market_neighborhood', placeholder: 'Botafogo' });
  const city = createInput({ label: 'City', name: 'market_city', placeholder: 'Rio de Janeiro' });
  const state = createInput({ label: 'State', name: 'market_state', placeholder: 'RJ' });
  const address = createInput({ label: 'Address', name: 'market_address', placeholder: 'Street, number' });
  marketGrid.append(marketName.group, neighborhood.group, city.group, state.group, address.group);

  const priceTitle = document.createElement('h3');
  priceTitle.textContent = 'Price details';

  const priceGrid = document.createElement('div');
  priceGrid.className = 'form-grid';
  const priceValue = createInput({
    label: 'Price (BRL)',
    name: 'price_value',
    type: 'number',
    placeholder: '0.00',
    required: true,
  });
  priceValue.field.step = '0.01';
  priceValue.field.min = '0';

  const promoField = document.createElement('label');
  promoField.className = 'form-group inline';
  const promoCheckbox = document.createElement('input');
  promoCheckbox.type = 'checkbox';
  promoCheckbox.name = 'price_promo';
  const promoText = document.createElement('span');
  promoText.textContent = 'Promotion active';
  promoField.append(promoCheckbox, promoText);

  const stock = createInput({ label: 'Stock status', name: 'price_stock', placeholder: 'Available, low stock…' });
  const notes = createInput({
    label: 'Notes',
    name: 'price_notes',
    placeholder: 'Optional observations',
    multiline: true,
  });
  const dateField = createInput({
    label: 'Price date/time',
    name: 'price_datetime',
    type: 'datetime-local',
    placeholder: '',
  });

  priceGrid.append(priceValue.group, promoField, stock.group, dateField.group, notes.group);

  const submitButton = document.createElement('button');
  submitButton.type = 'submit';
  submitButton.className = 'primary-button';
  submitButton.textContent = 'Save entry';

  form.append(
    productTitle,
    productGrid,
    marketTitle,
    marketGrid,
    priceTitle,
    priceGrid,
    submitButton,
  );

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const payload = {
      product: {
        name: productName.field.value.trim(),
        brand: optional(productBrand.field.value),
        unit: optional(productUnit.field.value),
        category: optional(productCategory.field.value),
        description: optional(productDescription.field.value),
      },
      market: {
        name: marketName.field.value.trim(),
        neighborhood: optional(neighborhood.field.value),
        city: optional(city.field.value),
        state: optional(state.field.value),
        address: optional(address.field.value),
      },
      price: {
        price: Number(priceValue.field.value),
        promo: promoCheckbox.checked,
        stock_status: optional(stock.field.value),
        notes: optional(notes.field.value),
        last_updated: optional(dateField.field.value)
          ? new Date(dateField.field.value).toISOString()
          : null,
      },
    };
    onSubmit(payload);
  });

  rootElement.append(form, statusBox);

  function setLoading(isLoading) {
    submitButton.disabled = isLoading;
    submitButton.textContent = isLoading ? 'Saving...' : 'Save entry';
  }

  function showMessage(message, variant = 'info') {
    statusBox.textContent = message;
    statusBox.className = `entry-message ${variant}`;
    statusBox.classList.remove('hidden');
  }

  function hideMessage() {
    statusBox.classList.add('hidden');
  }

  return {
    setLoading,
    showMessage,
    hideMessage,
    reset: () => form.reset(),
  };
}
