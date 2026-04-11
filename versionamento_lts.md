# Análise de Versionamento Semântico e LTS

> Atividade: Identificar se o versionamento semântico e o LTS estão disponíveis em dois componentes de software do projeto.

---

## Componentes Analisados

| Componente | Versão no projeto | Papel |
|---|---|---|
| **Pydantic** | 2.7.1 | Validação de dados e modelos |
| **PostgreSQL** | (via `asyncpg==0.29.0`) | Banco de dados |

---

## 1. Pydantic

### Versionamento Semântico

**Disponível**

O Pydantic segue o padrão **Semantic Versioning** (`MAJOR.MINOR.PATCH`) de forma explícita e documentada:

- **MAJOR** — mudanças incompatíveis com versões anteriores (ex: V1 → V2)
- **MINOR** — novas funcionalidades retrocompatíveis; também pode conter features experimentais
- **PATCH** — correções de bugs

A política oficial declara que não haverá breaking changes dentro de releases minor do V2:

> *"We will not intentionally make breaking changes in minor releases of V2. Functionality marked as deprecated will not be removed until the next major V3 release."*

**Evidência:** https://docs.pydantic.dev/latest/version-policy/

O histórico completo de releases está disponível em: https://github.com/pydantic/pydantic/releases

---

### LTS 

**Disponível (para versões major anteriores)**

O Pydantic adota uma política de suporte estendido as versões major anteriores após o lançamento de uma nova. Especificamente:

- O **Pydantic V1** teve desenvolvimento ativo encerrado após o lançamento do V2 mas continuou recebendo **correções críticas de bugs e vulnerabilidades de segurança** por um período definido (até o lançamento do V3).
- A documentação afirma: *"Active development of V1 has already stopped, however critical bug fixes and security vulnerabilities will be fixed in V1 until the release of Pydantic V3."*
- O ciclo de major releases é previsto para **aproximadamente uma vez por ano**, com suporte a versão anterior garantido nesse intervalo.

Isso configura um modelo de suporte de longo prazo equivalente ao LTS, mesmo sem usar esse nome formalmente.

**Evidência (Política de versões):** https://docs.pydantic.dev/latest/version-policy/  
**Evidência (Discussão sobre EOL do V1):** https://github.com/pydantic/pydantic/discussions/7505

---

## 2. PostgreSQL

### Versionamento Semântico

**Disponível (esquema próprio mas equivalente)**

O PostgreSQL utiliza um esquema de versionamento numérico com semântica clara e documentada:

- A partir da **versão 10**, o formato é `MAJOR.MINOR` (ex: `16.3`), onde:
  - **MAJOR** indica mudanças arquiteturais significativas (requer dump/restore para upgrade)
  - **MINOR** traz apenas correções de bugs e patches de segurança, sem breaking changes

Antes da versão 10 o formato era `MAJOR.MINOR.PATCH` (ex: `9.6.4`). A mudança foi feita justamente para simplificar e tornar o versionamento mais intuitivo

> *"Starting with PostgreSQL 10, a major version is indicated by increasing the first part of the version, e.g. 10 to 11."*

 **Evidência (Política de versionamento oficial):** https://www.postgresql.org/support/versioning/

---

### LTS 

**Disponível — 5 anos por major version**

O PostgreSQL possui uma das políticas de LTS mais claras e formalmente definidas entre os projetos open source:

> *"The PostgreSQL Global Development Group supports a major version for 5 years after its initial release. After this, a final minor version will be released and the software will then be unsupported (end-of-life)."*

Cada major version recebe **5 anos de suporte** com correções de bugs e patches de segurança. Ao atingir o EOL (End of Life), é publicada uma última minor release e o suporte é encerrado.

**Situação atual das versões suportadas:**

| Versão | Lançamento | EOL previsto |
|---|---|---|
| PostgreSQL 17 | Set/2024 | Nov/2029 |
| PostgreSQL 16 | Set/2023 | Nov/2028 |
| PostgreSQL 15 | Out/2022 | Nov/2027 |
| PostgreSQL 14 | Set/2021 | Nov/2026 |
| PostgreSQL 13 | Set/2020 | Nov/2025 |

**Evidência (Política de suporte oficial):** https://www.postgresql.org/support/versioning/  
**Evidência (Tabela de EOL detalhada):** https://endoflife.date/postgresql

---
