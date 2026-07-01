# Plano de implantacao

## Cenario

Empresa: Academia de Crossfit Forca & Foco  
Sistema: check-in antecipado de aulas  
Dominio simulado: `checkin.forcaefoco.com.br`  
Ambiente alvo: servidor Linux em nuvem, com Python 3 e SQLite  
Ambiente alternativo: Vercel com banco Supabase

## Infraestrutura provisionada

Para fins de entrega academica, o provisionamento foi planejado e simulado com os seguintes recursos:

| Recurso | Configuracao |
| --- | --- |
| Provedor de nuvem | AWS, Azure, GCP ou equivalente |
| Servidor | 1 VM Linux Ubuntu LTS |
| CPU/RAM | 1 vCPU, 1 GB RAM |
| Disco | 20 GB SSD |
| Banco | SQLite local em `data/checkins.sqlite3` |
| Porta publica | 80/443 via proxy reverso |
| Porta interna | 8000 |
| Backup | Copia diaria do arquivo SQLite |

## Infraestrutura Vercel + Supabase

Para publicacao em plataforma serverless, o projeto tambem esta preparado para:

| Recurso | Configuracao |
| --- | --- |
| Hospedagem | Vercel |
| Entrada da aplicacao | `api/index.py` |
| Roteamento | `vercel.json` |
| Banco | Supabase/Postgres |
| Schema | `supabase/schema.sql` |
| Variaveis | `SUPABASE_URL`, `SUPABASE_KEY` |

## Passos de implantacao na Vercel

1. Criar um projeto no Supabase.
2. Abrir o SQL Editor do Supabase e executar o conteudo de `supabase/schema.sql`.
3. Criar um projeto na Vercel apontando para este repositorio.
4. Configurar as variaveis de ambiente na Vercel:

```text
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-ou-service-role
```

5. Fazer o deploy pela Vercel.
6. Validar o endpoint:

```text
https://seu-projeto.vercel.app/api/health
```

## Passos de implantacao

1. Criar uma VM Linux Ubuntu LTS no provedor de nuvem.
2. Liberar trafego HTTP/HTTPS no firewall do provedor.
3. Instalar Python 3:

```bash
sudo apt update
sudo apt install -y python3
```

4. Enviar os arquivos do projeto para `/opt/forca-foco-checkin`.
5. Executar a aplicacao:

```bash
cd /opt/forca-foco-checkin
python3 app.py
```

6. Configurar um servico `systemd` para iniciar automaticamente:

```ini
[Unit]
Description=Forca e Foco Check-in
After=network.target

[Service]
WorkingDirectory=/opt/forca-foco-checkin
ExecStart=/usr/bin/python3 /opt/forca-foco-checkin/app.py
Restart=always
User=www-data

[Install]
WantedBy=multi-user.target
```

7. Configurar proxy reverso com Nginx:

```nginx
server {
    listen 80;
    server_name checkin.forcaefoco.com.br;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Simulacao de registro de dominio

Dominio escolhido: `forcaefoco.com.br`  
Subdominio do sistema: `checkin.forcaefoco.com.br`

Registros DNS simulados:

| Tipo | Nome | Valor |
| --- | --- | --- |
| A | `checkin` | IP publico da VM |
| CNAME | `www.checkin` | `checkin.forcaefoco.com.br` |

## Criterios de aceite

- O formulario solicita nome do aluno e horario desejado.
- O sistema grava o check-in no banco configurado: Supabase em producao ou SQLite local.
- A ocupacao das turmas e exibida na tela.
- O sistema impede novas reservas quando o limite da turma e atingido.
- O endpoint `/api/health` responde com `status: ok`.
- A recepcao possui manual de operacao.
