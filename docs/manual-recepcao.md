# Manual da recepcao

## Acesso

Endereco do sistema:

```text
https://checkin.forcaefoco.com.br
```

No ambiente local de testes:

```text
http://localhost:8000
```

## Como registrar um check-in

1. Abra o sistema no navegador.
2. Digite o nome completo do aluno no campo "Nome do aluno".
3. Selecione o horario desejado.
4. Confira a quantidade de vagas exibida ao lado do horario.
5. Clique em "Confirmar check-in".
6. Verifique a mensagem de confirmacao na tela.

## Controle de lotacao

Cada turma possui limite de 8 alunos. Quando a turma atingir o limite, o sistema bloqueia novas reservas para aquele horario e exibe uma mensagem de aviso.

## Conferencia das reservas

A secao "Ultimos check-ins" mostra os registros mais recentes, com:

- nome do aluno;
- horario da aula;
- data e hora do registro.

## Procedimento em caso de erro

- Se o nome estiver vazio, solicite o nome do aluno e tente novamente.
- Se a turma estiver cheia, ofereca outro horario disponivel.
- Se a pagina nao abrir, comunique a equipe tecnica e informe o horario da tentativa.
- Se houver duvida sobre estabilidade, acesse `/api/health` e confira se aparece `status: ok`.

## Boas praticas

- Registrar o check-in antes da chegada do aluno na aula.
- Nao cadastrar nomes abreviados quando houver risco de duplicidade.
- Conferir a ocupacao antes de confirmar a reserva.
- Manter a tela aberta durante o expediente para acompanhar novas reservas.
