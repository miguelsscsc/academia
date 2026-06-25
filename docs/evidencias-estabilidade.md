# Evidencias de estabilidade

## Verificacoes previstas

| Teste | Resultado esperado |
| --- | --- |
| Acesso a pagina inicial | HTTP 200 |
| Envio de check-in valido | Reserva gravada e exibida |
| Envio sem nome | Mensagem de validacao |
| Horario lotado | Bloqueio de nova reserva |
| Consulta `/api/health` | JSON com `status: ok` |
| Reinicio da aplicacao | Banco preserva registros |

## Endpoint de saude

URL:

```text
http://localhost:8000/api/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "database": true,
  "class_limit": 8,
  "checked_at": "2026-06-25T10:00:00"
}
```

## Comprovacao de persistencia

1. Registrar um check-in pela tela inicial.
2. Encerrar a aplicacao.
3. Iniciar a aplicacao novamente.
4. Confirmar que o check-in continua listado.

## Comprovacao de limite de turma

1. Registrar 8 alunos no mesmo horario.
2. Tentar registrar o nono aluno.
3. Confirmar que o sistema exibe a mensagem de turma lotada.

## Resultado

O ambiente e considerado estavel quando a pagina inicial e o endpoint de saude respondem corretamente, os registros persistem no banco e o limite de vagas e respeitado.
