## IMPORTAÇÕES
import requests, os, json
from dotenv import load_dotenv
from mcp.server import MCPServer

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_TOKEN = os.getenv("SUPABASE_API_TOKEN")
SUPABASE_REF_PROJECT = os.getenv("SUPABASE_REF_PROJECT")

## FUNÇÕES

mcp = MCPServer('Supabase')

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("supabase")

def buscar_docs(sql) -> list:
     # Requisição ao Supabase
        response = requests.post(
            f"{SUPABASE_URL}/{SUPABASE_REF_PROJECT}/database/query",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {SUPABASE_API_TOKEN}"
            },
            json={
                "query": f"{sql}",
                "read_only": True
            }
        )   
        #response.raise_for_status()  
        data = response.json()
        return data
       

@mcp.tool()
def listar_documentos(limite: int = 20) -> list:
    """Lista os documentos mais recentes, com limite entre 1 e 100."""
    if not 1 <= limite <= 100:
        raise ValueError("O limite deve estar entre 1 e 100.")
    sql = f"""
          SELECT
              id,
              nome_arquivo,
              categoria,
              status,
              percentual_sucesso,
              criado_em
          FROM public.documentos
          ORDER BY criado_em DESC
          LIMIT {limite};
    """
    return buscar_docs(sql) 

@mcp.resource("supabase://documentos/schema")
def descrever_documentos() -> str:
    """Retorna os metadados atuais da tabela public.documentos."""
    sql = """
        SELECT
            column_name,
            data_type,
            character_maximum_length,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'documentos'
        ORDER BY ordinal_position;
    """

    colunas = buscar_docs(sql)

    if not colunas:
        raise RuntimeError("Não foi possível encontrar o schema de public.documentos.")

    return json.dumps(
        {
            "tabela": "public.documentos",
            "descricao": "Metadados dos documentos processados.",
            "colunas": colunas,
        },
        indent=4,
        ensure_ascii=False,
    )

@mcp.prompt()
def consultar_documentos(pergunta: str) -> str:
    """Orienta a consulta e a explicação dos metadados dos documentos."""
    return f"""
    Você é um assistente que responde perguntas sobre os documentos registrados
    na tabela public.documentos.

    Pergunta do usuário: {pergunta}

    Consulte os dados usando a tool listar_documentos.
    Use supabase://documentos/schema como referência para interpretar os campos.

    Responda em português, de forma clara e concisa. Baseie a resposta somente
    nos dados retornados pelas tools. Não invente informações e informe quando
    os dados consultados não forem suficientes para responder.
    """



## CHAMAR A FUNÇÃO

if __name__ == "__main__":
    #resultado = consultar_documentos()
    #print(resultado)
    mcp.run(transport="stdio")