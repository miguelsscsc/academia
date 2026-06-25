# Sistema de Check-in - Forca & Foco

Entrega do desafio de implantacao de um sistema web para reservas antecipadas de vagas nas aulas da Academia de Crossfit **Forca & Foco**.

## Objetivo

Controlar a quantidade de alunos por turma, evitando superlotacao e permitindo que a recepcao acompanhe as reservas em tempo real.

## Funcionalidades

- Formulario web de check-in com nome do aluno e horario desejado.
- Validacao de limite de vagas por horario.
- Armazenamento das reservas em banco SQLite.
- Listagem de reservas confirmadas.
- Endpoint de saude para comprovacao de estabilidade do ambiente.
- Documentacao de infraestrutura, dominio simulado e treinamento da recepcao.

## Estrutura

```text
.
├── app.py
├── data/
│   └── .gitkeep
├── docs/
│   ├── evidencias-estabilidade.md
│   ├── implantacao.md
│   └── manual-recepcao.md
├── static/
│   └── styles.css
└── README.md
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

O banco e criado automaticamente em:

```text
data/checkins.sqlite3
```

Tabela principal:

```sql
CREATE TABLE checkins (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_name TEXT NOT NULL,
  class_time TEXT NOT NULL,
  created_at TEXT NOT NULL
);
```

## Entregaveis

- Aplicacao web funcional: [app.py](app.py)
- Plano de implantacao: [docs/implantacao.md](docs/implantacao.md)
- Manual da recepcao: [docs/manual-recepcao.md](docs/manual-recepcao.md)
- Evidencias de estabilidade: [docs/evidencias-estabilidade.md](docs/evidencias-estabilidade.md)
