## IMPORTAÇÕES
import os
import json
import requests
from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_API_TOKEN = os.getenv("SUPABASE_API_TOKEN", "")
SUPABASE_REF_PROJECT = os.getenv("SUPABASE_REF_PROJECT", "")

# Garante a URL base correta do projeto Supabase
if not SUPABASE_URL:
    if SUPABASE_REF_PROJECT:
        SUPABASE_URL = f"https://{SUPABASE_REF_PROJECT}.supabase.co"
elif "api.supabase.com" in SUPABASE_URL and SUPABASE_REF_PROJECT:
    SUPABASE_URL = f"https://{SUPABASE_REF_PROJECT}.supabase.co"

mcp = MCPServer("supabase")


def _get_headers() -> dict:
    return {
        "apikey": SUPABASE_API_TOKEN,
        "Authorization": f"Bearer {SUPABASE_API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def buscar_docs_rest(endpoint: str, params: dict | None = None) -> list | dict:
    """Realiza requisições HTTP GET na API REST (PostgREST) do Supabase."""
    url = f"{SUPABASE_URL}/rest/v1/{endpoint.lstrip('/')}"
    response = requests.get(url, headers=_get_headers(), params=params)
    response.raise_for_status()
    return response.json()


@mcp.tool()
def listar_documentos(limite: int = 20) -> list:
    """Lista os documentos mais recentes da base de dados do RAG (tabela documents)."""
    if not 1 <= limite <= 100:
        raise ValueError("O limite deve estar entre 1 e 100.")

    params = {
        "select": "id,content,metadata",
        "limit": limite,
    }
    return buscar_docs_rest("documents", params=params)


@mcp.tool()
def pesquisar_documentos(termo: str, limite: int = 10) -> list:
    """Pesquisa documentos pelo texto do conteudo (filtro ilike) na base RAG."""
    if not 1 <= limite <= 100:
        raise ValueError("O limite deve estar entre 1 e 100.")

    params = {
        "select": "id,content,metadata",
        "content": f"ilike.*{termo}*",
        "limit": limite,
    }
    return buscar_docs_rest("documents", params=params)


@mcp.resource("supabase://documents/schema")
def descrever_documentos() -> str:
    """Retorna a estrutura dos campos da tabela documents do RAG."""
    schema_info = {
        "tabela": "public.documents",
        "descricao": "Tabela de documentos e chunks do banco RAG.",
        "campos": [
            {"nome": "id", "tipo": "bigint/uuid", "descricao": "Identificador do documento"},
            {"nome": "content", "tipo": "text", "descricao": "Texto / conteúdo do documento ou chunk"},
            {"nome": "metadata", "tipo": "jsonb", "descricao": "Metadados adicionais (fonte, página, autor, etc.)"},
            {"nome": "embedding", "tipo": "vector", "descricao": "Vetor de embeddings para busca semântica"},
        ],
    }
    return json.dumps(schema_info, indent=4, ensure_ascii=False)


@mcp.prompt()
def consultar_documentos(pergunta: str) -> str:
    """Orienta a consulta e a explicacao sobre os documentos do banco RAG."""
    return f"""
    Você é um assistente que responde perguntas sobre os documentos do banco de dados RAG
    armazenados no Supabase na tabela public.documents.

    Pergunta do usuário: {pergunta}

    Para buscar informações:
    1. Utilize a tool `pesquisar_documentos` para procurar por termos-chave.
    2. Utilize a tool `listar_documentos` para obter a listagem dos documentos.
    3. Consulte `supabase://documents/schema` se precisar entender a estrutura dos campos.

    Responda em português, de forma clara e objetiva com base apenas nos dados retornados.
    """


if __name__ == "__main__":
    mcp.run(transport="stdio")