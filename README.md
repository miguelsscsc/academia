# Sistema de Check-in - Forca & Foco

Entrega do desafio de implantacao de um sistema web para reservas antecipadas de vagas nas aulas da Academia de Crossfit **Forca & Foco**.

## Objetivo

Controlar a quantidade de alunos por turma, evitando superlotacao e permitindo que a recepcao acompanhe as reservas em tempo real.

## Funcionalidades

- Formulario web de check-in com nome do aluno e horario desejado.
- Validacao de limite de vagas por horario.
- Armazenamento das reservas em Supabase quando configurado.
- Fallback local em SQLite para desenvolvimento sem variaveis de ambiente.
- Listagem de reservas confirmadas.
- Endpoint de saude para comprovacao de estabilidade do ambiente.
- Documentacao de infraestrutura, dominio simulado e treinamento da recepcao.

## Estrutura

```text
.
|-- api/
|   `-- index.py
|-- app.py
|-- data/
|   `-- .gitkeep
|-- docs/
|   |-- evidencias-estabilidade.md
|   |-- implantacao.md
|   `-- manual-recepcao.md
|-- static/
|   `-- styles.css
|-- scripts/
|   `-- test_supabase.py
|-- supabase/
|   `-- schema.sql
|-- .env.example
|-- requirements.txt
|-- vercel.json
`-- README.md
```

## Como executar localmente

Requisito: Python 3.10 ou superior.

```bash
python app.py
```

Acesse:

```text
http://localhost:8000
```

Endpoint de estabilidade:

```text
http://localhost:8000/api/health
```

## Banco de dados

Sem variaveis de ambiente do Supabase, o banco local e criado automaticamente em:

```text
data/checkins.sqlite3
```

Para usar Supabase, crie a tabela executando o arquivo:

```text
supabase/schema.sql
```

Depois crie um arquivo `.env` a partir de `.env.example` e preencha:

```text
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-do-supabase
SUPABASE_TABLE=checkins
```

Opcionalmente, use `SUPABASE_TABLE` para trocar o nome da tabela. O padrao e `checkins`.

Para testar a conexao localmente:

```bash
pip install -r requirements.txt
python scripts/test_supabase.py
```

Se o teste responder `Conexao OK`, execute o site:

```bash
python app.py
```

## Deploy na Vercel

O projeto ja inclui:

- `vercel.json` para redirecionar as rotas para a funcao Python.
- `api/index.py` como entrada serverless da Vercel.
- `requirements.txt` com a dependencia do Supabase.

Na Vercel, adicione `SUPABASE_URL` e `SUPABASE_KEY` em **Settings > Environment Variables** antes de publicar.

## Entregaveis

- Aplicacao web funcional: [app.py](app.py)
- Plano de implantacao: [docs/implantacao.md](docs/implantacao.md)
- Manual da recepcao: [docs/manual-recepcao.md](docs/manual-recepcao.md)
- Evidencias de estabilidade: [docs/evidencias-estabilidade.md](docs/evidencias-estabilidade.md)
