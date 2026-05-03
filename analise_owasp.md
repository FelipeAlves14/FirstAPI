analise_owasp.md 

# Análise de Segurança – Módulo Centro de Treinamento

---

## 1. A01:2025 - Broken Access Control

### Problema

O sistema não implementa autenticação nem autorização, permitindo acesso irrestrito às rotas.

### Evidências no código

```python
@centro_treinamento_router.post("/")
async def post(...)
```

```python
@centro_treinamento_router.get("/")
async def get(...)
```

### Não há:

- Verificação de usuário autenticado
- Controle de permissões
- Restrição por perfil 

### Impacto

- Qualquer usuário pode:
  - Criar centros de treinamento
  - Consultar todos os dados
- Compromete a integridade e confiabilidade do sistema

### Como resolver

 Implementar autenticação (JWT, OAuth2):

```python
from fastapi import Depends
from app.auth import get_current_user

@centro_treinamento_router.post("/")
async def post(..., user=Depends(get_current_user)):
```

Restringir ações administrativas:

```python
if not user.is_admin:
    raise HTTPException(status_code=403, detail="Sem permissão")
```

---

## A10:2025 - Mishandling of Exceptional Conditions

### Problema

Tratamento incorreto de exceções e uso inadequado de códigos HTTP.

### Evidências

```python
except IntegrityError:
    raise HTTPException(
        status_code=status.HTTP_303_SEE_OTHER,
        detail=f"Já existe um centro de treinamento cadastrado com o nome: {centro_treinamento_model.nome}"
    )
```

### Problemas

- Uso incorreto de `303 SEE OTHER`
- Exposição de informação interna 
- Possível erro se `centro_treinamento_model` não estiver consistente

### Impacto

- Vazamento de informações
- API inconsistente
- Facilita enumeração de dados

### Como resolver

Corrigir código HTTP:

```python
raise HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Centro de treinamento já cadastrado"
)
```

Evitar expor dados internos

Implementar handler global de exceções

---

## 3. A02:2025 - Security Misconfiguration

### Problema

Configuração insegura relacionada à exposição de dados e ausência de proteção contra abuso.

### Evidências

```python
async def get(db_session: database_dependency):
    centros_treinamento = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
```

### Endpoint:

- Público
- Retorna todos os registros
- Sem limitação de acesso real (apenas paginação)
- Sem rate limiting

### Impacto

- Coleta massiva de dados (scraping)
- Sobrecarga do sistema
- Possível uso malicioso da API

### Como resolver

 Implementar rate limiting:

```python
@limiter.limit("10/minute")
```

 Restringir acesso a usuários autenticados

 Implementar logs e monitoramento

---

##  Conclusão 

A análise dos módulos de **Atleta**, **Categoria** e **Centro de Treinamento** revelou um padrão consistente de vulnerabilidades, especialmente relacionadas à ausência de controle de acesso, tratamento inadequado de exceções e configurações inseguras.

Essas falhas permitem que usuários não autenticados realizem operações críticas, exponham dados e explorem o comportamento da aplicação. Tais vulnerabilidades violam princípios fundamentais de segurança como **confidencialidade**, **integridade** e **disponibilidade**.

A adoção de mecanismos de **autenticação**, **autorização**, **validação de entradas**, **tratamento adequado de exceções** e **proteção contra abuso** (rate limiting) é essencial para mitigar os riscos identificados e garantir a segurança do sistema.