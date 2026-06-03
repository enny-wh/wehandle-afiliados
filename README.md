# WeHandle Afiliados — Ranking automático

Atualização diária automática do ranking de cupons via GitHub Actions + Sympla API.

## Configuração (fazer uma única vez)

### 1. Adicionar secrets no GitHub
No repositório: **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Valor |
|--------|-------|
| `SYMPLA_TOKEN` | Token gerado em Minha Conta → Integrações na Sympla |
| `SYMPLA_EVENT_ID` | ID do evento (está na URL do evento no painel) |

### 2. Habilitar o workflow
O arquivo `.github/workflows/ranking.yml` já está configurado.
O job roda automaticamente todo dia às 09h (horário de Brasília).
Para rodar manualmente: **Actions → Atualizar ranking de afiliados → Run workflow**

## Estrutura
```
├── fetch_ranking.py          # Script que chama a Sympla API
├── data/
│   └── ranking.json          # Resultado atualizado diariamente
└── .github/workflows/
    └── ranking.yml           # Agendamento automático
```

## Como o artefato do ranking consome os dados
O artefato aponta para a URL raw do `data/ranking.json` neste repositório:
```
https://raw.githubusercontent.com/SEU_ORG/SEU_REPO/main/data/ranking.json
```
