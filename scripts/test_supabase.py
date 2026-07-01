from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app import SUPABASE_TABLE, get_supabase_client, use_supabase


def main():
    if not use_supabase():
        print("Supabase nao configurado. Crie um arquivo .env baseado no .env.example.")
        return 1

    client = get_supabase_client()
    response = client.table(SUPABASE_TABLE).select("id").limit(1).execute()
    total = len(response.data)
    print(f"Conexao OK. Tabela '{SUPABASE_TABLE}' acessivel. Linhas lidas no teste: {total}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
