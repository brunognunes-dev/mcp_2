
import asyncio

from mcp import Client
from server import mcp


async def main():
    print("Conectando ao servidor MCP...")

    async with Client(mcp) as client:
        print("\n[OK] Conexão estabelecida com sucesso!")

        # 1. Listar ferramentas disponíveis
        resultado_tools = await client.list_tools()
        print("\nFerramentas disponíveis:")
        for ferramenta in resultado_tools.tools:
            print(f"- {ferramenta.name}: {ferramenta.description}")

        # 2. Executar a ferramenta de listagem
        print("\nConsultando documentos no Supabase (listar_documentos)...")
        resultado_listar = await client.call_tool(
            "listar_documentos",
            {"limite": 5},
        )
        print("Resultado da listagem:")
        print(resultado_listar)

        # 3. Testar a ferramenta de pesquisa textual
        print("\nTestando pesquisa no Supabase (pesquisar_documentos)...")
        resultado_busca = await client.call_tool(
            "pesquisar_documentos",
            {"termo": "teste", "limite": 5},
        )
        print("Resultado da pesquisa:")
        print(resultado_busca)


if __name__ == "__main__":
    asyncio.run(main())

