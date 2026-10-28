# Supabase RAG MCP Server

Servidor MCP (**Model Context Protocol**) em Python para conectar agentes e ferramentas de IA à base de dados vetorial / RAG hospedada no **Supabase** (tabela `public.documents`).

---

## 🎯 Funcionalidades

- **`listar_documentos`** *(Tool)*: Lista os documentos/chunks mais recentes cadastrados na tabela `documents` com suporte a paginação (`limite` de 1 a 100).
- **`pesquisar_documentos`** *(Tool)*: Realiza busca textual no conteúdo (`content`) usando correspondência de padrão (`ilike`).
- **`supabase://documents/schema`** *(Resource)*: Retorna os metadados e estrutura de campos da tabela (`id`, `content`, `metadata`, `embedding`).
- **`consultar_documentos`** *(Prompt)*: Template de prompt guiado para agentes responderem dúvidas baseando-se estritamente nas consultas ao banco.

---

## 📁 Estrutura do Projeto

```text
mcp_2/
├── .env                  # Variáveis de ambiente e credenciais (ignorado no Git)
├── .gitignore            # Regras de exclusão do Git
├── .vscode/
│   └── mcp.json          # Configuração do MCP Server no VS Code / Claude Desktop / IDEs
├── requirements.txt      # Dependências do Python (mcp, python-dotenv, requests)
├── server.py             # Servidor MCP e integração com a API REST do Supabase
└── test_mcp.py           # Script cliente para testar ferramentas e conexão MCP
```

---

## 📋 Pré-requisitos

- **Python 3.10+** instalado no sistema.
- Um projeto ativo no [Supabase](https://supabase.com).
- A tabela `public.documents` criada no Supabase (comum em arquiteturas RAG).

---

## 🚀 Passo a Passo de Instalação e Execução

### Passo 1: Clonar ou Acessar a Pasta do Projeto

Abra o terminal no diretório do projeto:

```bash
cd "mcp_2"
```

---

### Passo 2: Criar e Ativar o Ambiente Virtual (`venv`)

Recomenda-se isolar as dependências em um ambiente virtual.

**No Windows (PowerShell / Prompt de Comando):**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

> *Dica*: Se o PowerShell bloquear a execução de scripts, execute antes:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

**No Linux ou macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### Passo 3: Instalar as Dependências

Com o ambiente virtual ativado, instale os pacotes necessários:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Passo 4: Configurar as Variáveis de Ambiente (`.env`)

Crie ou edite o arquivo `.env` na raiz do projeto com os seguintes valores:

```env
SUPABASE_URL=https://SEU_PROJECT_REF.supabase.co
SUPABASE_API_TOKEN=SUA_ANON_OU_PUBLISHABLE_API_KEY
SUPABASE_REF_PROJECT=SEU_PROJECT_REF
```

#### Onde encontrar esses dados no painel do Supabase:
1. Acesse o dashboard do seu projeto no Supabase.
2. Vá em **Project Settings** (ícone de engrenagem) > **API**.
3. Copie:
   - **Project URL**: `https://<project-ref>.supabase.co` (preencha em `SUPABASE_URL`).
   - **Reference ID**: o código do projeto (preencha em `SUPABASE_REF_PROJECT`).
   - **Project API Keys**: copie a chave **`anon` / `publishable`** (ou `service_role` se desejar bypassar RLS em leitura) e preencha em `SUPABASE_API_TOKEN`.

---

### Passo 5: Testar a Conexão com o Supabase e MCP

Para validar se o servidor e a autenticação com o banco do Supabase estão funcionando perfeitamente, execute o script de teste incluído:

**No Windows:**
```powershell
.\.venv\Scripts\python.exe test_mcp.py
```

**No Linux/macOS:**
```bash
python test_mcp.py
```

**Saída esperada:**
```text
Conectando ao servidor MCP...

[OK] Conexão estabelecida com sucesso!

Ferramentas disponíveis:
- listar_documentos: Lista os documentos mais recentes da base de dados do RAG (tabela documents).
- pesquisar_documentos: Pesquisa documentos pelo texto do conteudo (filtro ilike) na base RAG.

Consultando documentos no Supabase (listar_documentos)...
Resultado da listagem:
meta=... content=[] is_error=False result_type='complete'
```

---

### Passo 6: Executar o Servidor MCP

O servidor utiliza transporte padrão via **STDIO** (padrão oficial para comunicação de clientes MCP locais):

```bash
python server.py
```

> **Nota:** Como o servidor aguarda conexões via STDIO, ao executá-lo diretamente no terminal ele ficará em execução aguardando mensagens no formato JSON-RPC. Para encerrar, pressione `Ctrl + C`.

---

## 🛠️ Como Conectar o Servidor ao seu Assistente / IDE

### 1. No VS Code / Claude Dev / Antigravity IDE
O projeto já conta com o arquivo [mcp.json](file:///.vscode/mcp.json) dentro da pasta `.vscode/`:

```json
{
  "servers": {
    "supabase": {
      "command": "python",
      "args": [
        "c:/Users/Bruno Gabriel/Documents/IA GENERATIVA/mcp_2/server.py"
      ]
    }
  }
}
```
*(Certifique-se de apontar para o executável `python.exe` da sua `.venv` ou certifique-se de que o Python ativo contenha as dependências instaladas).*

### 2. Testar via MCP Inspector Oficial
Você pode testar visualmente todas as ferramentas e resources no navegador com o MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python server.py
```

---

## 🔒 Segurança

- O arquivo `.env` nunca deve ser enviado para o repositório (`.gitignore` já configurado).
- Use credenciais de leitura apropriadas (`anon`/`publishable` com políticas de RLS ativas) para limitar o acesso aos dados sensíveis.

