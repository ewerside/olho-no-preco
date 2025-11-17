# OlhoNoPreco

> Projeto da disciplina de **Extração e Preparação de Dados (Ibmec)**. Plataforma colaborativa para coleta e análise de preços de mercado a partir de **notas fiscais** (foto + chave de acesso).
> **Integrantes:** Ewerton Arrais, João Gabriel, Miguel Veiga.

## Sumário

* [Contexto](#contexto)
* [Arquitetura (versão AP1)](#arquitetura-versão-ap1)
* [Resultados da AP1](#resultados-da-ap1)
* [Arquitetura (versão AP2)](#arquitetura-versão-ap2)
* [Resultados da AP2](#resultados-da-ap2)
* [Como rodar](#como-rodar)
* [Como rodar (AP2)](#como-rodar-ap2)
* [Esquema de dados](#esquema-de-dados)
* [Esquema de dados (AP2)](#esquema-de-dados-ap2)
* [Limitações e riscos](#limitações-e-riscos)
* [Limitações e riscos (AP2)](#limitações-e-riscos-ap2)
* [Roteiro (próximos passos)](#roteiro-próximos-passos)
* [Roteiro (AP2)](#roteiro-ap2)
* [Links úteis](#links-úteis)

---

## Contexto

Preços de alimentos variam entre bairros e mudam rapidamente. O **OlhoNoPreco** cria uma visão comunitária desses preços: usuários enviam **fotos de cupons/notas** e/ou **chaves de acesso** da NFC-e; o sistema extrai itens, quantidades e valores e consolida para análise.

---

## Arquitetura (versão AP1)

1. **OCR baseline (foto do cupom)** — Tesseract para demonstrar pipeline e limitações.
2. **Prova de conceito estruturada** — uso da **Chave de Acesso** para abrir a consulta pública e salvar o **HTML detalhado** da nota; extração **direta do DOM** (BeautifulSoup + lxml), sem OCR nem regex pesadas (pares `<label> → <span>` e classes CSS).
3. **Saída** — DataFrame/CSV com campos essenciais (descrição, quantidades, unidade, valores, NCM etc.).

---

## Resultados da AP1

* Notebook com:

  * pipeline de OCR (demonstração + limitações),
  * extração estruturada do **HTML** detalhado,
  * DataFrame final + CSV.
* Decisão técnica: priorizar **dados estruturados via chave/HTML** para escala.

---

## Arquitetura (versão AP2)

1. **Backend FastAPI + SQLite** — módulos separados para core/config, modelos (Market/Product/ProductPrice) e CRUDs. O banco é semeado com dados sintéticos via `backend/scripts/init_db.py`.
2. **Serviços e schemas** — `services/analytics.py` calcula estatísticas de preço e os schemas Pydantic cobrem busca, sugestões e criação de entradas.
3. **Frontend estático (HTML + ES Modules)** — interface única com abas para comparar preços e registrar novas entradas. CSS segue a paleta do mockup pastel e os componentes JS (busca, listagem e formulário) ficam em `frontend/src/components`.

---

## Resultados da AP2

* Catálogo sintético de mercados/produtos com múltiplas cotações em `backend/data/`.
* API REST com:
  * `/products/search` (comparativo por item),
  * `/products/{id}` (detalhe),
  * `/products/` e `/markets/suggest` (auto complete no frontend),
  * `/entries` (criação com upsert automático de produto/mercado + novo preço).
* Frontend em inglês com abas “Compare prices” e “Add entry”, mostrando cartões com menor/médio/maior preço e formulário com sugestões dinâmicas.
* README organizado contendo instruções específicas da AP1 e da AP2 para consulta rápida.

---

## Como rodar

### 1) Via Colab (recomendado na AP1)

**Colab AP1:** [https://colab.research.google.com/drive/1Ovk_y-clmc5Xnew177JYzjAu1PBTgv7x?authuser=1#scrollTo=Py_eeQc6_RRn](https://colab.research.google.com/drive/1Ovk_y-clmc5Xnew177JYzjAu1PBTgv7x?authuser=1#scrollTo=Py_eeQc6_RRn)

### 2) Local (opcional)

Requisitos:

```bash
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install pandas beautifulsoup4 lxml opencv-python-headless pytesseract
```

**Arquivos esperados (no repositório ou no Colab):**

```
nota/
├─ nota detalhada.html
├─ nota.jpg
└─ nota_cortada.jpg
```

* **HTML detalhado** (`nota/nota detalhada.html`) é a página salva da consulta pública da SEFAZ (aba **Produtos e Serviços**).
* **nota.jpg** / **nota_cortada.jpg** são imagens usadas no baseline de OCR (opcional).

O notebook lê:

* `nota/nota detalhada.html` para **extração por DOM** (sem OCR);
* `nota/nota.jpg` ou `nota/nota_cortada.jpg` para a parte **OCR** demonstrativa.

---

## Como rodar (AP2)

1. **Backend**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
   pip install -r backend/requirements.txt
   python -m backend.scripts.init_db  # recria o SQLite com dados sintéticos
   uvicorn backend.app.main:app --reload
   ```

   Endpoints principais:

   | Método | Rota | Descrição |
   | ------ | ---- | --------- |
   | GET | `/health` | Status da API |
   | GET | `/products/search?query=` | Busca+estatística por produto |
   | GET | `/products/{id}` | Detalhe de um produto específico |
   | GET | `/products/suggest` | Sugestões de nomes para autocomplete |
   | GET | `/markets/suggest` | Sugestões de mercados |
   | POST | `/entries` | Upsert de produto, mercado e preço |

2. **Frontend**

   ```bash
   python -m http.server 5173 -d frontend
   ```

   - Abas:
     - **Compare prices**: campo de busca, resultado resumido e cards com estatísticas.
     - **Add entry**: formulário com sugestões dinâmicas para produto e mercado (auto complete conforme digitação).
   - O CORS já libera `http://127.0.0.1:5173`, então basta visitar esse endereço enquanto o backend estiver ativo.

---

## Esquema de dados

Saída por item (principais colunas):

| coluna                 | descrição                                         |
| ---------------------- | ------------------------------------------------- |
| `descricao`            | Nome do produto conforme a nota                   |
| `quantidade`           | Quantidade (resumo)                               |
| `unidade`              | Unidade (resumo)                                  |
| `valor_item`           | Valor total do item (resumo)                      |
| `codigo_produto`       | Código do produto (detalhes)                      |
| `ncm`                  | NCM                                               |
| `unidade_comercial`    | Unidade comercial (detalhes)                      |
| `quantidade_comercial` | Quantidade comercial (detalhes)                   |
| `valor_unitario`       | Valor unitário de comercialização                 |
| `valor_item_calc`      | `quantidade_comercial * valor_unitario`           |
| `valor_item_final`     | `valor_item` se existir; senão, `valor_item_calc` |

Metadados (podem acompanhar o DF): `chave_acesso`, `valor_total_nfe`, dados da loja (se presentes).

---

## Esquema de dados (AP2)

- **markets** (`id`, `name`, `neighborhood`, `city`, `state`, `address`, `phone`, `opening_hours`)
- **products** (`id`, `name`, `brand`, `unit`, `category`, `description`)
- **product_prices** (`id`, `product_id`, `market_id`, `price`, `currency`, `promo`, `stock_status`, `last_updated`, `notes`)

Observações:

* o endpoint `/entries` faz upsert de `products` e `markets` antes de criar o registro em `product_prices`;
* `services/analytics.py` calcula `min`, `max`, `avg`, spread e identifica em qual mercado apareceu cada extremo;
* o frontend ordena automaticamente os preços e destaca o menor valor (selo verde) para reforçar a mensagem de economia.

---

## Limitações e riscos

* **Mudanças de layout** no site da SEFAZ podem exigir pequenos ajustes de seletores.
* **Normalização de produto** (mesmo item com nomes diferentes) exige NCM/EAN + *matching* semântico.
* **Privacidade**: evitar armazenar dados pessoais (CPF, chave completa) e aplicar anonimização/amostragem.
* **Conformidade**: respeitar termos de uso; se automatizar coleta, usar *rate limiting*, cache e logs.

---

## Limitações e riscos (AP2)

* **Dados sintéticos** — os preços cadastrados não representam valores reais e devem ser trocados a cada experimento.
* **Sem autenticação** — qualquer pessoa que acesse a API pode inserir dados via `/entries`; ideal implementar autenticação e logging.
* **Infra local** — FastAPI + SQLite funcionam em demos, mas precisam de upgrade (PostgreSQL, deploy gerenciado) para uso contínuo.

---

## Roteiro (próximos passos)

1. **Coleta automatizada** por chave (serviço “ponte” robusto).
2. **Resolução de entidades** (produto canônico por NCM/EAN + *string matching*/embeddings).
3. **Aplicativo ao consumidor** (comparação de preços por produto/região).

---

## Roteiro (AP2)

1. **Backoffice autenticado** — proteger o endpoint de cadastro e permitir histórico das alterações.
2. **Filtros na comparação** — ordenar por bairro, faixa de preço, disponibilidade ou promoções em destaque.
3. **Integração com dados reais** — ligar o pipeline AP1 (HTML/Notas) ao banco da API, automatizando o seed.
4. **Testes automatizados** — pytest + FastAPI TestClient e testes de interface (Playwright) para evitar regressões.

---

## Links úteis

* **Colab da AP1:** [https://colab.research.google.com/drive/1Ovk_y-clmc5Xnew177JYzjAu1PBTgv7x?authuser=1#scrollTo=Py_eeQc6_RRn](https://colab.research.google.com/drive/1Ovk_y-clmc5Xnew177JYzjAu1PBTgv7x?authuser=1#scrollTo=Py_eeQc6_RRn)
* **Consulta por Chave de Acesso (SEFAZ-RJ):** [https://consultadfe.fazenda.rj.gov.br/consultaDFe/paginas/consultaChaveAcesso.faces](https://consultadfe.fazenda.rj.gov.br/consultaDFe/paginas/consultaChaveAcesso.faces)
* **Artigo (Overleaf):** [https://www.overleaf.com/project/68ace74927bd39e5ea1c3930](https://www.overleaf.com/project/68ace74927bd39e5ea1c3930)
* **Apresentação de Slides da AP1:** [https://docs.google.com/presentation/d/1PUeq5oab41M2VnJ16UtRCVFLYM4M7-Uw/edit?usp=sharing&ouid=110652581352670982634&rtpof=true&sd=true](https://docs.google.com/presentation/d/1PUeq5oab41M2VnJ16UtRCVFLYM4M7-Uw/edit?usp=sharing&ouid=110652581352670982634&rtpof=true&sd=true)
* **Comparador de métodos de OCR (Google AI Studio):** [https://ai.studio/apps/drive/1GVHMh4UgDWnOUoNq4Y4Nl66tJX4dNbLI](https://ai.studio/apps/drive/1GVHMh4UgDWnOUoNq4Y4Nl66tJX4dNbLI)

