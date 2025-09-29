# OlhoNoPreco

> Projeto da disciplina de **Extração e Preparação de Dados (Ibmec)**. Plataforma colaborativa para coleta e análise de preços de mercado a partir de **notas fiscais** (foto + chave de acesso).
> **Integrantes:** Ewerton Arrais, João Gabriel, Miguel Veiga.

## Sumário

* [Contexto](#contexto)
* [Arquitetura (versão AP1)](#arquitetura-versão-ap1)
* [Resultados da AP1](#resultados-da-ap1)
* [Como rodar](#como-rodar)
* [Esquema de dados](#esquema-de-dados)
* [Limitações e riscos](#limitações-e-riscos)
* [Roteiro (próximos passos)](#roteiro-próximos-passos)
* [Links úteis](#links-úteis)

---

## Contexto

Preços de alimentos variam entre bairros e mudam rapidamente. O **OlhoNoPreco** cria uma visão comunitária desses preços: usuários enviam **fotos de cupons/notas** e/ou **chaves de acesso** da NFC-e; o sistema extrai itens, quantidades e valores e consolida para análise.

---

## Arquitetura (versão AP1)

1. **OCR baseline (foto do cupom)** — OpenCV + Tesseract para demonstrar pipeline e limitações.
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

## Limitações e riscos

* **Mudanças de layout** no site da SEFAZ podem exigir pequenos ajustes de seletores.
* **Normalização de produto** (mesmo item com nomes diferentes) exige NCM/EAN + *matching* semântico.
* **Privacidade**: evitar armazenar dados pessoais (CPF, chave completa) e aplicar anonimização/amostragem.
* **Conformidade**: respeitar termos de uso; se automatizar coleta, usar *rate limiting*, cache e logs.

---

## Roteiro (próximos passos)

1. **Coleta automatizada** por chave (serviço “ponte” robusto).
2. **Resolução de entidades** (produto canônico por NCM/EAN + *string matching*/embeddings).
3. **Aplicativo ao consumidor** (comparação de preços por produto/região).

---

## Links úteis

* **Colab da AP1:** [https://colab.research.google.com/drive/1Ovk_y-clmc5Xnew177JYzjAu1PBTgv7x?authuser=1#scrollTo=Py_eeQc6_RRn](https://colab.research.google.com/drive/1Ovk_y-clmc5Xnew177JYzjAu1PBTgv7x?authuser=1#scrollTo=Py_eeQc6_RRn)
* **Consulta por Chave de Acesso (SEFAZ-RJ):** [https://consultadfe.fazenda.rj.gov.br/consultaDFe/paginas/consultaChaveAcesso.faces](https://consultadfe.fazenda.rj.gov.br/consultaDFe/paginas/consultaChaveAcesso.faces)
* **Artigo (Overleaf):** [https://www.overleaf.com/project/68ace74927bd39e5ea1c3930](https://www.overleaf.com/project/68ace74927bd39e5ea1c3930)
