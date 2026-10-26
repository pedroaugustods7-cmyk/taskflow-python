# 🚀 TaskFlow — Gerenciador de Tarefas Full Stack

Aplicação web Full Stack desenvolvida com Python e FastAPI para gerenciamento de tarefas, com uma interface intuitiva e armazenamento persistente em SQLite.

## Sobre o projeto

O TaskFlow permite organizar atividades do dia a dia por meio de uma aplicação web. Foi desenvolvido como projeto de portfólio para aplicar conhecimentos de desenvolvimento Full Stack, APIs REST, integração com banco de dados e testes automatizados.

## Tecnologias utilizadas

**Back-end**
- Python
- FastAPI
- SQLite
- Pydantic

**Front-end**
- HTML5
- CSS3
- JavaScript

**Testes e versionamento**
- Pytest
- HTTPX
- Git e GitHub

## Funcionalidades

- Cadastro de tarefas
- Listagem automática de tarefas
- Edição de tarefas
- Exclusão de tarefas
- Marcação de tarefas concluídas
- Persistência de dados com SQLite
- Documentação interativa da API
- Testes automatizados dos principais endpoints

## Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/taskflow-python.git
cd taskflow-python
```

### 2. Crie o ambiente virtual

```bash
python -m venv .venv
```

### 3. Instale as dependências

No Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Inicie o servidor

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

### 5. Acesse a aplicação

- Aplicação: http://127.0.0.1:8000
- Documentação da API: http://127.0.0.1:8000/docs

## Testes automatizados

Para executar:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Foram implementados cinco testes automatizados para as funcionalidades principais da API.

## Próximas melhorias

- Filtros de tarefas
- Prioridades e prazos
- Melhorias na responsividade
- Deploy em ambiente de produção

## Objetivo

Demonstrar conhecimentos em desenvolvimento Full Stack com Python, construção de APIs REST, persistência de dados, integração entre front-end e back-end e qualidade de software.