# Lab: Lambda Python 3.9 → 3.13 via PR + OIDC (custo zero)

Este lab cria um repositório mínimo com uma Lambda **sem gatilhos**, **concorrência reservada = 0** (não processa chamadas) e **retention de logs** curta.
Fluxo:
1) Repositório começa com `python3.9` no código/manifesto.
2) Workflow `Propose runtime upgrade` abre um **Pull Request** que altera para `python3.13`.
3) Ao **mergear o PR**, o workflow de deploy aplica a mudança na AWS via **OIDC do GitHub** (sem chaves long-lived).

> **Sem custos**: Sem triggers, sem invocações, concorrência = 0 e sem provisioned concurrency. IAM não tem custo. Logs só existem se você invocar manualmente (retenção 1 dia).

## Pré‑requisitos (uma vez só na sua conta de teste)
- **IAM Role da Lambda** (execução da função): anote o ARN em `LAMBDA_EXECUTION_ROLE_ARN` (policy: `AWSLambdaBasicExecutionRole`).  
- **IAM Role para OIDC do GitHub** (deploy): crie um Role com trust no provedor OIDC do GitHub e permissões mínimas para Lambda e CloudWatch Logs da função. Anote em `AWS_ROLE_TO_ASSUME`.
- **GitHub Secrets** no seu repositório:
  - `AWS_ROLE_TO_ASSUME` — ARN do role OIDC de deploy.
  - `AWS_REGION` — ex.: `us-east-1`.
  - `LAMBDA_FUNCTION_NAME` — ex.: `lab-renata-python`.
  - `LAMBDA_EXECUTION_ROLE_ARN` — ARN do role de execução da Lambda.
- **Proteção de branch** no `main`: exigir PR para merge.

## Como usar
1. **Faça o push** deste conteúdo para seu repositório Git.
2. Na aba **Actions**, rode manualmente **“Propose runtime upgrade (3.9 → 3.13)”**. Isso criará um PR.
3. Revise e **faça merge** do PR.
4. O workflow **“Deploy on merge”** fará:
   - criação/atualização da Lambda com o runtime definido,
   - **concorrência reservada = 0** (sem custo por invocação),
   - retenção de logs = 1 dia.

> Você pode chamar o deploy manualmente (workflow dispatch) se precisar.

## Invocação opcional (se desejar testar manualmente)
- Remova a concorrência 0 temporariamente (ou rode o invoke local via SAM).  
  **Importante:** invocações consomem free tier — mantenha chamadas **mínimas** ou nenhuma.

## Estrutura
```
.
├─ lambda_function.py
├─ requirements.txt
├─ template.yaml
├─ README.md
└─ .github/workflows
   ├─ propose-runtime-upgrade.yml
   └─ deploy-on-merge.yml
```

---

## Segurança e custos
- **Nenhum trigger** associado → a função não executa sozinha.
- **Reserved concurrency = 0** → evita execuções acidentais.
- **Sem provisão** e **memória 128MB** → limites mínimos.
- **Log retention 1 dia** → se alguém invocar, minimiza custo de armazenamento.
