# Supabase MCP Server

Este projeto cria um servidor MCP (Model Context Protocol) para consultar e expor dados do Supabase em um formato amigável para agentes e ferramentas de IA.

## Objetivo

O servidor conecta com um projeto Supabase remoto e expõe endpoints para:

- listar documentos recentes;
- consultar metadados da tabela `public.documents`;
- servir contexto útil para agentes que precisam responder perguntas sobre os dados armazenados no banco.

## Estrutura do projeto

- `server.py`: implementação do servidor MCP e integrações com o Supabase.
- `.env`: variáveis de ambiente locais com credenciais e configuração do projeto.
- `.gitignore`: evita que arquivos sensíveis e artefatos locais sejam versionados.

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SUPABASE_URL=https://api.supabase.com/v1/projects
SUPABASE_REF_PROJECT=SEU_REF_DO_PROJETO
SUPABASE_SECRET_KEY=SUA_SECRET_KEY
# ou, se preferir:
# SUPABASE_API_TOKEN=SUA_API_TOKEN
```

Importante:

- nunca versionar o arquivo `.env`;
- manter chaves e tokens fora do repositório;
- usar um ambiente local seguro para desenvolvimento.

## Dependências

As dependências do projeto são definidas em `requirements.txt`.

Para instalar:

```bash
pip install -r requirements.txt
```

## Execução

Rodar o servidor:

```bash
python server.py
```

Ou, se estiver usando ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
python server.py
```

## Observação sobre segurança

Este projeto usa credenciais do Supabase para autenticar consultas no banco. Todas as informações sensíveis foram protegidas pelo arquivo `.gitignore`, e o `.env` deve permanecer fora do controle de versão.

## Funcionalidades principais

O servidor implementa operações para:

- consultar os documentos recentes;
- descrever o schema da tabela `public.documents`;
- orientar consultas e respostas baseadas no contexto do banco.

## Responsabilidade do uso

Use as credenciais apenas no ambiente local e nunca exponha tokens em logs, commits, screenshots ou arquivos compartilhados.
