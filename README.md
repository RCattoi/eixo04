# Eixo04 - Orquestração de Dados com Airflow, Docker, PostgreSQL e Metabase - Alocação de Caçambas Alternativa

Este projeto é uma stack completa para orquestração de pipelines de dados utilizando Apache Airflow, bancos PostgreSQL, Metabase (BI) e Docker. O objetivo é facilitar a ingestão, atualização e visualização de dados de clientes a partir de arquivos Excel, com automação e rastreabilidade.

---

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Configurando o DBeaver para acessar o banco PostgreSQL](#configurando-o-dbeaver-para-acessar-o-banco-postgresql)
- [Passo a Passo para Rodar o Projeto](#passo-a-passo-para-rodar-o-projeto)
   - [Clone o repositório](#1-clone-o-repositório)
   - [Configure o arquivo .env](#2-configure-o-arquivo-env)
   - [Suba os serviços](#5-suba-os-serviços)
- [Resolução de Problemas Comuns](#resolução-de-problemas-comuns)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Documentação Técnica Completa do Sistema](#documentação-técnica-completa-do-sistema)
   - [Visão Geral do Projeto](#visão-geral-do-projeto)
   - [Arquitetura do Sistema](#arquitetura-do-sistema)
   - [Modelo de Dados](#modelo-de-dados)
   - [Fluxo de Dados Completo](#fluxo-de-dados-completo)
   - [Documentação Detalhada das DAGs](#documentação-detalhada-das-dags)
   - [Processo de Deploy e Inicialização](#processo-de-deploy-e-inicialização)
   - [Troubleshooting e Debugging](#troubleshooting-e-debugging)
   - [Melhorias Futuras Sugeridas](#melhorias-futuras-sugeridas)
   - [Referências e Documentação Adicional](#referências-e-documentação-adicional)


## Pré-requisitos

- **Docker** e **Docker Compose** instalados ([Download Docker Desktop](https://www.docker.com/products/docker-desktop/))
- **Git** (opcional, para clonar o repositório)
- **Windows** (as instruções consideram ambiente Windows, mas funcionam em Linux/Mac com pequenas adaptações)
- **DBeaver** ([Download DBeaver Community](https://dbeaver.io/download/))
  - O DBeaver é obrigatório para acessar, visualizar e manipular os bancos de dados PostgreSQL criados pelos containers. Ele facilita a inspeção das tabelas, execução de queries e depuração dos dados processados pelas DAGs do Airflow.

---

## Configurando o DBeaver para acessar o banco PostgreSQL

1. Instale o DBeaver normalmente pelo link acima.
2. Com os containers do projeto rodando, abra o DBeaver e clique em "Nova Conexão" > PostgreSQL.
3. Preencha os campos conforme o serviço desejado:
   - **Host:** `localhost`
   - **Porta:** `5433` (para o banco de dados de dados, serviço `data-postgres`)
   - **Database:** o nome do banco (ex: `metabase` ou outro definido no `.env`)
   - **Usuário:** o valor de `POSTGRES_USER` do seu `.env`
   - **Senha:** o valor de `POSTGRES_PASSWORD` do seu `.env`
4. Teste a conexão e salve.

Você pode criar conexões separadas para o banco do Airflow (porta padrão 5432, banco `airflow`, usuário `airflow`, senha `airflow`) e para o banco de dados de dados (porta 5433, conforme acima).

Assim, você poderá acompanhar a criação de tabelas, inserção de dados e depuração de eventuais problemas diretamente pelo DBeaver.

---

## Passo a Passo para Rodar o Projeto

### 1. Clone o repositório

```sh
git clone https://github.com/RCattoi/eixo04.git
cd eixo04
```

### 2. Configure o arquivo `.env`

Crie o arquivo `.env` na raiz do projeto com o seguinte conteúdo e complete com as variáveis:

``` text
AIRFLOW_IMAGE_NAME=<VALOR>
AIRFLOW_UID=<VALOR>
POSTGRES_USER=<VALOR>
POSTGRES_PASSWORD=<VALOR>
POSTGRES_DB=<VALOR>
AIRFLOW_USER=<VALOR>
AIRFLOW_PASSWORD=<VALOR>
_PIP_ADDITIONAL_REQUIREMENTS=<VALOR>
```

> **Atenção:**
>
> - Não coloque espaços antes/depois do `=`.
> - Não deixe linhas em branco no meio das variáveis.
> - Não compartilhe seu `.env` com senhas em repositórios públicos.

### 3. (Opcional) Ajuste a porta do nginx

Por padrão, o nginx expõe a porta 80. Se ela estiver ocupada (ex: por IIS, Skype, Apache), altere no `docker-compose.yaml`:

``` text
    ports:
      - '8081:80'
```

Assim, acesse o Metabase em <http://localhost:8081>.

### 4. Remova volumes antigos (importante para evitar conflitos de banco)

Sempre que mudar variáveis do banco no `.env`, execute:

```sh
docker-compose down -v
```

Isso remove os volumes persistentes e garante que o banco será criado corretamente.

### 5. Suba os serviços

```sh
docker-compose up --build
```

Aguarde até que todos os containers estejam rodando. O processo pode demorar na primeira vez (baixando imagens e instalando dependências).

### 6. Acesse as interfaces

- **Airflow:** <http://localhost:8080>  
  Usuário: `<USER>`  
  Senha: `<SENHA>`
- **Metabase:** <http://localhost:8081> (ou <http://localhost:3000> se não alterou a porta)

### 7. Teste a DAG

No Airflow, ative a DAG `simple_hello_dag` e clique em "Trigger DAG" para rodar manualmente. Acompanhe os logs pela interface.

### 8. Sobre o arquivo Excel

O arquivo de clientes deve estar em `files/dados_empresa_alternativa.xlsx`. Certifique-se de que ele existe antes de rodar a DAG.

---

## Resolução de Problemas Comuns

- **Porta 80 ocupada:**
  - O Windows pode usar a porta 80 pelo processo `System` (HTTP.sys). Não mate esse processo! Apenas altere a porta do nginx para `8081` no `docker-compose.yaml`.

- **Banco `metabase` não existe:**
  - Sempre defina `POSTGRES_DB=metabase` no `.env` para garantir que o banco seja criado.
  - Se mudar variáveis do banco, rode `docker-compose down -v` antes de subir novamente.

- **Loop de containers reiniciando:**
  - Normalmente causado por variáveis de ambiente erradas ou banco não criado. Confira o `.env` e remova volumes antigos.

- **Senhas e usuários:**
  - Use sempre as mesmas credenciais no `.env` e nos serviços que dependem do banco.

---

## Estrutura do Projeto

- `dags/` - DAGs do Airflow (pipelines de dados)
- `files/` - Arquivos de entrada (ex: Excel de clientes)
- `config/` - Configurações do Airflow
- `utils/` - Utilitários Python
- `plugins/` - Plugins customizados do Airflow
- `logs/` - Logs gerados pelo Airflow
- `requirements.txt` - Dependências Python
- `docker-compose.yaml` - Orquestração dos serviços
- `Dockerfile` - Customização da imagem do Airflow

---

## Dicas Finais

- Sempre confira o log do terminal para mensagens de erro.
- Se mudar algo no `.env` ou no banco, remova os volumes antes de subir novamente.
- Não compartilhe seu `.env` publicamente.
- Para dúvidas, consulte a documentação oficial do [Airflow](https://airflow.apache.org/) e [Metabase](https://www.metabase.com/).

---

## Documentação Técnica Completa do Sistema

Esta seção detalha profundamente a arquitetura, os componentes, o fluxo de dados e a lógica de negócio implementada neste projeto de orquestração de dados.

---

### Visão Geral do Projeto

Este projeto implementa um **pipeline de dados completo** (ETL - Extract, Transform, Load) para processar informações de uma empresa de gestão de resíduos que utiliza caçambas para coleta. O sistema é construído com as seguintes tecnologias principais:

- **Apache Airflow**: Orquestrador de workflows que gerencia e agenda a execução das DAGs
- **PostgreSQL**: Dois bancos de dados - um para metadados do Airflow e outro para os dados de negócio
- **Metabase**: Ferramenta de Business Intelligence para visualização e análise dos dados
- **Docker**: Containerização de todos os serviços para facilitar deploy e escalabilidade
- **Nginx**: Proxy reverso para o Metabase
- **Redis**: Message broker para o executor Celery do Airflow

### Arquitetura do Sistema

#### Componentes e suas Responsabilidades

**1. Apache Airflow (Orquestrador Principal)**

O Airflow é dividido em múltiplos containers especializados:

- **airflow-apiserver** (porta 8080): Interface web e API REST para gerenciamento das DAGs
  - Permite visualizar, ativar/desativar e monitorar DAGs
  - Fornece logs detalhados de cada execução
  - Gerencia conexões com bancos de dados externos

- **airflow-scheduler**: Cérebro do Airflow que:
  - Analisa as DAGs e determina quando executá-las baseado nos schedules
  - Enfileira tarefas para execução
  - Monitora a saúde dos workers

- **airflow-worker**: Executa as tarefas propriamente ditas
  - Processa os dados usando Celery Executor
  - Permite paralelização de tarefas
  - Pode escalar horizontalmente para mais workers

- **airflow-dag-processor**: Processa os arquivos DAG
  - Lê os arquivos Python da pasta `dags/`
  - Valida a sintaxe e estrutura das DAGs
  - Atualiza o banco de metadados com informações das DAGs

- **airflow-triggerer**: Gerencia tarefas assíncronas e deferrable operators
  - Eficiente para tarefas que esperam eventos externos
  - Reduz uso de recursos comparado a polling

- **airflow-init**: Container de inicialização que:
  - Cria o banco de dados do Airflow
  - Cria usuário administrador
  - Configura permissões de arquivos
  - Valida recursos do sistema (CPU, RAM, disco)

**2. Bancos de Dados PostgreSQL**

**postgres** (porta interna 5432):

- Banco exclusivo para metadados do Airflow
- Armazena informações sobre DAGs, execuções, logs, conexões
- Usuário: `airflow` / Senha: `airflow` / Database: `airflow`

**data-postgres** (porta 5433):

- Banco de dados de negócio onde ficam os dados processados
- Contém o schema `alternativa` com tabelas dimensionais e fato
- Configurado com `postgresql.conf` e `pg_hba.conf` customizados
- Usuário/senha definidos no arquivo `.env`
- Database: `datadb`

**3. Redis**

- Message broker para o Celery Executor
- Gerencia filas de tarefas do Airflow
- Permite comunicação assíncrona entre scheduler e workers
- Porta interna: 6379

**4. Metabase**

- Ferramenta de BI para análise visual dos dados
- Conecta-se ao `data-postgres` para ler os dados processados
- Seu próprio banco de metadados também fica no `data-postgres`
- Porta: 3000 (acesso direto) ou 8081 (via nginx)

**5. Nginx**

- Proxy reverso que encaminha requisições para o Metabase
- Permite configurações adicionais de segurança e cache
- Configurado via `nginx.conf`
- Porta externa: 8081 → Porta interna Metabase: 3000

---

### Modelo de Dados

O sistema implementa um **Data Warehouse com esquema estrela (Star Schema)** no schema `alternativa`:

#### Tabelas Dimensionais (SCD Tipo 2)

Todas as dimensões implementam **Slowly Changing Dimensions Tipo 2**, que mantém histórico completo de alterações:

**1. dim_cliente** (Dimensão de Clientes)

```sql
- sk_id_cliente: Surrogate Key (chave artificial sequencial)
- id_cliente: ID natural do cliente (vem do Excel)
- nome: Nome do cliente
- tipo_cliente: 'PF' (Pessoa Física) ou 'PJ' (Pessoa Jurídica)
- cidade: Cidade do cliente
- inicio_validade: Timestamp de quando o registro ficou válido
- fim_validade: NULL se ativo, timestamp se histórico
```

**Por que SCD Tipo 2?** Permite rastrear mudanças. Ex: Se o cliente mudou de cidade, o registro antigo recebe `fim_validade` e um novo registro é criado com a cidade nova.

**2. dim_funcionario** (Dimensão de Funcionários)

```sql
- sk_id_funcionario: Surrogate Key
- id_funcionario: ID natural do funcionário
- nome: Nome do funcionário
- cargo: Cargo (ex: Motorista, Operador)
- inicio_validade: Timestamp de criação
- fim_validade: NULL se ativo
```

**3. dim_frota** (Dimensão de Veículos)

```sql
- sk_id_caminhao: Surrogate Key
- id_caminhao: ID natural do caminhão
- placa: Placa do veículo
- tipo_modelo: Modelo do caminhão
- capacidade: Capacidade de carga em kg
- inicio_validade: Timestamp de criação
- fim_validade: NULL se ativo
```

**4. dim_residuo** (Dimensão de Tipos de Resíduo)

```sql
- sk_id_residuo: Surrogate Key
- id_residuo: ID natural do resíduo
- tipo_residuo: Tipo (ex: Orgânico, Reciclável, Perigoso)
- tratamento: Destinação (ex: Aterro, Reciclagem, Incineração)
- inicio_validade: Timestamp de criação
- fim_validade: NULL se ativo
```

#### Tabela Fato

**fato_servico** (Fato de Serviços de Coleta)

```sql
- id_servico: Chave composta (concatenação de ids + data)
- id_cliente: FK para dim_cliente (via surrogate key)
- id_caminhao: FK para dim_frota (via surrogate key)
- id_residuo: FK para dim_residuo (via surrogate key)
- id_motorista: FK para dim_funcionario (via surrogate key)
- data_solicitacao: Data da solicitação do serviço
- tempo_resposta_horas: Tempo até atendimento
- tempo_permanencia_dias: Dias que a caçamba ficou no local
- peso_residuos_kg: Peso total coletado
- km_percorridos: Quilometragem do trajeto
- taxa_ocupacao_percent: Percentual de ocupação da caçamba
```

**Métricas de Negócio:** Esta tabela permite análises como:

- Tempo médio de resposta por região
- Taxa de ocupação por tipo de resíduo
- Eficiência da frota (km por coleta)
- Volume de resíduos por cliente/período

---

### Fluxo de Dados Completo

#### 1. Fonte de Dados

**Arquivo Excel:** `files/dados_empresa_alternativa.xlsx`

Contém 5 abas (sheets):

- **clientes**: Dados cadastrais dos clientes
- **funcionarios**: Informações dos colaboradores
- **frota**: Dados dos veículos
- **residuos**: Tipos de resíduos e destinações
- **coletas**: Registros dos serviços realizados (fato)

#### 2. Processamento pelas DAGs

O sistema possui **5 DAGs especializadas**, cada uma responsável por processar uma entidade:

---

### Documentação Detalhada das DAGs

#### **DAG 1: process_client_data**

**Objetivo:** Processar dados de clientes mantendo histórico de alterações (SCD Tipo 2)

**Configuração:**

```python
dag_id: "process_client_data"
schedule: "@daily"  # Executa diariamente à meia-noite
start_date: datetime(2025, 10, 28)
catchup: False  # Não executa retroativamente
retries: 1  # Tenta novamente 1 vez em caso de falha
retry_delay: timedelta(minutes=5)
```

**Fluxo de Execução:**

1. **Extração (Extract)**
   - Lê a aba 'clientes' do Excel usando pandas
   - Transforma o campo `tipo_cliente`:
     - "Pessoa Física" → "PF"
     - "Pessoa Jurídica" → "PJ"
   - Extrai lista de `id_cliente` para busca no banco

2. **Verificação de Existência (Check)**

   ```python
   # Busca clientes existentes e ativos (fim_validade IS NULL)
   SELECT * FROM alternativa.dim_cliente 
   WHERE id_cliente IN (...) AND fim_validade IS NULL
   ```

3. **Detecção de Mudanças (Change Detection)**

   Para cada cliente existente, compara:
   - `nome_cliente` (do Excel) com `nome` (do banco)
   - `tipo_cliente` (do Excel) com `tipo_cliente` (do banco)
   - `cidade` (do Excel) com `cidade` (do banco)

   **Se houver diferença:**
   - Marca o registro antigo como histórico:

     ```sql
     UPDATE alternativa.dim_cliente 
     SET fim_validade = NOW() 
     WHERE id_cliente = X AND fim_validade IS NULL
     ```

   - Mantém o cliente no DataFrame para inserção como novo registro

   **Se for idêntico:**
   - Remove do DataFrame (sem necessidade de inserção)

4. **Carga (Load)**
   - Insere novos clientes e versões atualizadas:

   ```python
   INSERT INTO alternativa.dim_cliente 
   (id_cliente, nome, tipo_cliente, cidade) 
   VALUES (...)
   # inicio_validade é preenchido automaticamente com NOW()
   # fim_validade é NULL por padrão
   ```

**Por que essa abordagem?**

- Mantém histórico completo: podemos saber que o cliente X estava na cidade Y em determinado período
- Permite análises temporais: "Quantos clientes PJ tínhamos em 2024?"
- Rastreabilidade: Toda mudança é registrada com timestamp

---

#### **DAG 2: process_employee_data**

**Objetivo:** Gerenciar dados de funcionários com versionamento

**Configuração:** Idêntica à DAG de clientes

**Fluxo de Execução:**

1. **Extração**
   - Lê aba 'funcionarios' do Excel
   - Extrai campos: `id_funcionario`, `nome`, `cargo`

2. **Verificação de Mudanças**

   Compara para cada funcionário:
   - `nome`: Se funcionário mudou de nome (casamento, etc)
   - `cargo`: Se houve promoção ou mudança de função

   **Exemplo prático:**

   ```
   Funcionário 101 - João Silva - Motorista
   → Excel agora mostra: João Silva - Supervisor
   
   Ação:
   1. UPDATE registro antigo: fim_validade = NOW()
   2. INSERT novo registro: João Silva - Supervisor
   ```

3. **Carga**

   ```sql
   INSERT INTO alternativa.dim_funcionario 
   (id_funcionario, nome, cargo) 
   VALUES (...)
   ```

**Caso de Uso:** Permite rastrear progressão de carreira e analisar produtividade por cargo ao longo do tempo.

---

#### **DAG 3: process_fleet_data**

**Objetivo:** Manter cadastro atualizado da frota de veículos

**Configuração:** Schedule diário

**Fluxo de Execução:**

1. **Extração**
   - Lê aba 'frota' do Excel
   - Campos: `id_caminhao`, `placa`, `modelo`, `capacidade_carga_kg`

2. **Detecção de Alterações**

   Verifica mudanças em:
   - `placa`: Caso o veículo seja reemplacado
   - `modelo`: Caso haja erro no cadastro ou upgrade
   - `capacidade_carga_kg`: Modificações no veículo

   **Exemplo:**

   ```
   Caminhão 5 - ABC1234 - Mercedes Axor - 15000kg
   → Upgrade: ABC1234 - Mercedes Axor 2024 - 18000kg
   
   Sistema cria novo registro mantendo histórico
   ```

3. **Carga**

   ```sql
   INSERT INTO alternativa.dim_frota 
   (id_caminhao, placa, tipo_modelo, capacidade) 
   VALUES (...)
   ```

**Importância:** Rastrear capacidade é crucial para análise de eficiência e planejamento de rotas.

---

#### **DAG 4: process_waste_data**

**Objetivo:** Catalogar tipos de resíduos e suas destinações

**Configuração:** Execução diária

**Fluxo de Execução:**

1. **Extração**
   - Lê aba 'residuos' do Excel
   - Campos: `id_residuo`, `tipo_residuo`, `destinacao`

2. **Verificação de Mudanças**

   Compara:
   - `tipo_residuo`: Classificação do resíduo
   - `tratamento` (mapeado de `destinacao`): Forma de destinação

   **Caso de Uso Real:**

   ```
   Resíduo 3 - Plástico - Aterro
   → Empresa agora recicla: Plástico - Reciclagem
   
   Histórico permite análises de sustentabilidade ao longo do tempo
   ```

3. **Carga**

   ```sql
   INSERT INTO alternativa.dim_residuo 
   (id_residuo, tipo_residuo, tratamento) 
   VALUES (...)
   ```

**Valor para Negócio:** Compliance ambiental e relatórios de sustentabilidade exigem histórico de destinações.

---

#### **DAG 5: process_service_data** ⭐ (A MAIS COMPLEXA)

**Objetivo:** Processar a tabela fato com todos os serviços de coleta realizados

**Configuração:** Schedule diário

**Por que é complexa?** Precisa fazer lookups em múltiplas dimensões para obter as surrogate keys.

**Fluxo de Execução Detalhado:**

1. **Extração**
   - Lê aba 'coletas' do Excel
   - Campos: `id_cliente`, `id_caminhao`, `id_residuo`, `id_motorista`, `data_solicitacao`, métricas...

2. **Enriquecimento com Surrogate Keys** (Processo Crítico)

   **Problema:** O Excel tem IDs naturais, mas o banco usa surrogate keys (sk_id_*).

   **Solução:** Para cada dimensão:

   ```python
   headers_list = {
       'id_cliente': "dim_cliente",
       'id_caminhao': "dim_frota", 
       'id_residuo': "dim_residuo",
       'id_funcionario': "dim_funcionario"
   }
   ```

   Para cada par (coluna_excel, tabela_dimensão):

   a) **Busca as Surrogate Keys ativas:**

   ```python
   # Função retorna_tabela busca registros ativos
   SELECT * FROM alternativa.{tabela} 
   WHERE {coluna} IN (...) AND fim_validade IS NULL
   ```

   b) **Cria mapeamento ID Natural → Surrogate Key:**

   ```python
   # Exemplo para clientes:
   resultado = [(1, 101), (2, 102), (3, 103)]  # (sk, id_natural)
   mapa_sk = {101: 1, 102: 2, 103: 3}
   ```

   c) **Substitui IDs naturais por SKs no DataFrame:**

   ```python
   df['id_cliente'] = df['id_cliente'].map(mapa_sk)
   ```

   **Tratamento Especial para Motorista:**

   ```python
   # Excel tem 'id_motorista', mas dimensão é 'id_funcionario'
   if k == 'id_funcionario':
       df[k] = df['id_motorista'].map(mapa_sk)
   ```

3. **Geração de ID Composto**

   **Por que ID composto?** Garante unicidade de cada serviço.

   ```python
   # Concatena todos os IDs + data para criar identificador único
   cols = ['id_cliente', 'id_caminhao', 'id_residuo', 
           'id_funcionario', 'data_solicitacao']
   df['id'] = df[cols].astype(str).agg(''.join, axis=1)
   
   # Exemplo: "112132024-10-15" 
   # (cliente 1, caminhão 1, resíduo 2, funcionário 1, data)
   ```

4. **Verificação de Duplicatas**

   ```sql
   SELECT * FROM alternativa.fato_servico 
   WHERE id_servico IN (...)
   ```

   Remove do DataFrame serviços já existentes (evita duplicação).

5. **Carga da Tabela Fato**

   ```python
   INSERT INTO alternativa.fato_servico (
       id_servico, id_cliente, id_caminhao, id_residuo, 
       id_motorista, data_solicitacao, tempo_resposta_horas,
       tempo_permanencia_dias, peso_residuos_kg, 
       km_percorridos, taxa_ocupacao_percent
   ) VALUES (...)
   ```

   **Conversões de Tipo:**
   - IDs: `int()`
   - Métricas numéricas: `float()`
   - Data: mantém formato date

**Ordem de Execução Crítica:**

```
1° → process_client_data
2° → process_employee_data  
3° → process_fleet_data
4° → process_waste_data
5° → process_service_data (depende de todas as anteriores)
```

**Por quê?** A DAG de serviços precisa que as dimensões estejam atualizadas para fazer os lookups corretamente.

---

### Componentes de Suporte

#### PostgreSQL Hook

Todas as DAGs utilizam `PostgresHook`:

```python
from airflow.providers.postgres.hooks.postgres import PostgresHook

hook = PostgresHook(postgres_conn_id='data_db')
```

**O que faz:**

- Gerencia conexão com o banco `data-postgres`
- Fornece métodos para executar queries:
  - `hook.get_records(sql, parameters)`: SELECT queries
  - `hook.run(sql, parameters)`: INSERT/UPDATE queries
- Usa connection pooling para eficiência
- Trata transações automaticamente

**Configuração da Conexão:**

No Airflow UI, deve-se configurar a connection `data_db`:

```
Connection ID: data_db
Connection Type: Postgres
Host: data-postgres
Schema: datadb
Login: (valor do POSTGRES_USER do .env)
Password: (valor do POSTGRES_PASSWORD do .env)
Port: 5432
```

#### Pandas para Manipulação de Dados

Todas as DAGs usam pandas:

```python
import pandas as pd

df = pd.read_excel(
    "/opt/airflow/files/dados_empresa_alternativa.xlsx", 
    sheet_name='clientes'
)
```

**Vantagens:**

- Leitura fácil de Excel com múltiplas abas
- Manipulação de dados em memória (filtros, transformações)
- Integração com NumPy para cálculos
- Métodos convenientes como `.map()`, `.apply()`, `.values`

---

### Containerização e Orquestração Docker

#### Volumes Persistentes

O `docker-compose.yaml` define volumes para persistir dados:

```yaml
volumes:
  postgres-db-volume:  # Dados do Airflow
  data-postgres-volume:  # Dados de negócio
```

**Por que volumes?** Containers são efêmeros. Volumes garantem que dados sobrevivam a `docker-compose down`.

#### Volumes Montados (Bind Mounts)

```yaml
volumes:
  - ./dags:/opt/airflow/dags  # DAGs
  - ./utils:/opt/airflow/utils  # Utilitários
  - ./logs:/opt/airflow/logs  # Logs do Airflow
  - ./config:/opt/airflow/config  # Configurações
  - ./plugins:/opt/airflow/plugins  # Plugins customizados
  - ./files:/opt/airflow/files:ro  # Excel (read-only)
```

**Benefícios:**

- Alterações em DAGs são detectadas automaticamente
- Logs acessíveis no host para debugging
- Configuração pode ser alterada sem rebuild
- `:ro` (read-only) protege arquivo Excel de alterações acidentais

#### Health Checks

Cada serviço tem health check para garantir disponibilidade:

**PostgreSQL:**

```yaml
healthcheck:
  test: ['CMD', 'pg_isready', '-U', 'airflow']
  interval: 10s
  retries: 5
  start_period: 5s
```

**Redis:**

```yaml
healthcheck:
  test: ['CMD', 'redis-cli', 'ping']
  interval: 10s
  timeout: 30s
  retries: 50
  start_period: 30s
```

**Airflow API Server:**

```yaml
healthcheck:
  test: ['CMD', 'curl', '--fail', 'http://localhost:8080/api/v2/version']
  interval: 30s
  timeout: 10s
  retries: 5
```

**Importância:** Dependências (depends_on) esperam health checks passarem antes de iniciar serviços dependentes.

#### Executor Celery

**Por que Celery em vez de Sequential ou Local?**

- **Paralelização:** Múltiplas tarefas rodam simultaneamente
- **Escalabilidade:** Pode-se adicionar mais workers
- **Resiliência:** Se um worker falha, outros continuam
- **Distribuição:** Workers podem rodar em máquinas diferentes

**Componentes:**

- **Broker (Redis):** Fila de tarefas
- **Scheduler:** Envia tarefas para a fila
- **Workers:** Consomem e executam tarefas
- **Result Backend (PostgreSQL):** Armazena resultados

---

### Segurança e Configurações

#### Arquivo .env (Variáveis de Ambiente)

```env
AIRFLOW_IMAGE_NAME=apache/airflow:3.1.0
AIRFLOW_UID=50000  # UID do usuário nos containers
POSTGRES_USER=<VALOR>
POSTGRES_PASSWORD=<VALOR>!
POSTGRES_DB=datadb
_AIRFLOW_WWW_USER_USERNAME=<VALOR>
_AIRFLOW_WWW_USER_PASSWORD=<VALOR>
_PIP_ADDITIONAL_REQUIREMENTS=  # Deixar vazio, usar requirements.txt
```

**Boas Práticas:**

- Nunca versionar o `.env` (adicionar ao `.gitignore`)
- Usar senhas fortes e únicas
- Documentar variáveis necessárias em `.env.example`
- Usar mesmas credenciais em todos os serviços que compartilham banco

#### Configuração PostgreSQL Customizada

**postgresql.conf:**

- Ajustes de performance (shared_buffers, work_mem)
- Configurações de logging
- Otimizações para workload específico

**pg_hba.conf:**

- Define regras de autenticação
- Controla quem pode conectar de onde
- Tipos de autenticação (md5, trust, reject)

---

### Metabase e Visualização

#### Conexão com Dados

Metabase se conecta ao `data-postgres`:

```yaml
environment:
  - MB_DB_TYPE=postgres  # Tipo de banco para metadados do Metabase
  - MB_DB_DBNAME=metabase  # Database para metadados
  - MB_DB_HOST=data-postgres
  - MB_DB_USER=${POSTGRES_USER}
  - MB_DB_PASS=${POSTGRES_PASSWORD}
```

**Dois bancos no mesmo PostgreSQL:**

1. `metabase`: Armazena configurações, dashboards, queries salvas do Metabase
2. `datadb`: Dados de negócio (schema `alternativa`)

#### Nginx como Proxy

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://metabase:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Benefícios:**

- URL limpa (<http://localhost:8081>)
- Possibilidade de adicionar SSL
- Cache de conteúdo estático
- Rate limiting
- Load balancing (múltiplas instâncias Metabase)

---

### Processo de Deploy e Inicialização

#### Sequência de Startup

1. **docker-compose up --build**

2. **Criação de Networks**
   - Docker cria rede interna para comunicação entre containers

3. **Volumes**
   - Cria ou reutiliza volumes persistentes

4. **Bancos de Dados**
   - `postgres` e `data-postgres` iniciam primeiro
   - Health checks aguardam estarem prontos

5. **Redis**
   - Inicia e passa health check

6. **airflow-init**
   - Verifica recursos do sistema
   - Cria diretórios necessários
   - Executa migrations do banco do Airflow
   - Cria usuário administrador
   - Ajusta permissões de arquivos

7. **Serviços Airflow**
   - Aguardam `airflow-init` completar
   - Iniciam em paralelo:
     - API Server
     - Scheduler
     - DAG Processor
     - Worker
     - Triggerer

8. **Metabase**
   - Aguarda `data-postgres` estar saudável
   - Inicializa banco de metadados
   - Na primeira vez, apresenta wizard de configuração

9. **Nginx**
   - Aguarda Metabase
   - Inicia proxy reverso

#### Primeira Execução

**No Airflow (<http://localhost:8080>):**

1. Login com credenciais do `.env`
2. Verificar que DAGs aparecem (pode demorar ~30s)
3. Configurar connection `data_db`:
   - Admin → Connections → Add
   - Preencher dados do `data-postgres`
4. Ativar DAGs (toggle on)
5. Executar na ordem:
   - `process_client_data`
   - `process_employee_data`
   - `process_fleet_data`
   - `process_waste_data`
   - `process_service_data`

**No Metabase (<http://localhost:8081>):**

1. Wizard de configuração inicial
2. Adicionar database:
   - Type: PostgreSQL
   - Host: data-postgres
   - Port: 5432
   - Database: datadb
   - Username: (do .env)
   - Password: (do .env)
3. Metabase analisa schema e sugere questões

---

### Troubleshooting e Debugging

#### Logs do Airflow

**Via UI:**

- Clicar em DAG → Task → View Log
- Logs coloridos com stack traces completos

**Via Docker:**

```bash
docker logs airflow-worker
docker logs airflow-scheduler
```

**Via Arquivos:**

- `logs/` no host contém logs persistidos
- Organizados por dag_id/task_id/execution_date

#### Problemas Comuns

**1. DAG não aparece:**

- Verificar erros de sintaxe Python
- Checar logs do `airflow-dag-processor`:

  ```bash
  docker logs airflow-dag-processor
  ```

- Sintaxe incorreta gera parsing errors

**2. Erro de conexão com banco:**

- Verificar connection `data_db` configurada
- Testar conexão no DBeaver com mesmas credenciais
- Checar se `data-postgres` está rodando:

  ```bash
  docker ps | grep data-postgres
  ```

**3. Excel não encontrado:**

- Verificar que arquivo existe em `files/dados_empresa_alternativa.xlsx`
- Volume montado corretamente (`:ro` impede escrita, mas permite leitura)
- Checar permissões do arquivo

**4. Duplicatas na tabela fato:**

- Não deveria acontecer devido ao check de `id_servico`
- Se ocorrer, verificar lógica de geração do ID composto
- Pode indicar que dimensões não foram processadas primeiro

**5. Surrogate keys NULL na fato:**

- Significa que lookup falhou
- Causas:
  - Dimensões não processadas
  - IDs no Excel não existem nas dimensões
  - Registro da dimensão tem `fim_validade` preenchido (não ativo)

#### Comandos Úteis

**Reiniciar tudo:**

```bash
docker-compose down -v  # Remove volumes (CUIDADO: apaga dados!)
docker-compose up --build
```

**Rebuild apenas Airflow:**

```bash
docker-compose build airflow-apiserver
docker-compose up -d
```

**Ver logs em tempo real:**

```bash
docker-compose logs -f airflow-worker
```

**Executar comando no container:**

```bash
docker exec -it <container_name> bash
```

**Listar DAGs via CLI:**

```bash
docker exec -it airflow-worker airflow dags list
```

---

### Análises Possíveis com os Dados

Com o modelo de dados implementado, é possível responder questões como:

**Operacionais:**

- Qual o tempo médio de resposta por região?
- Quais caminhões têm melhor taxa de ocupação?
- Quantos km em média cada motorista percorre por dia?

**Negócio:**

- Quais clientes geram mais receita (peso × frequência)?
- Qual tipo de resíduo é mais comum por cidade?
- Tendência de volume de coletas ao longo do tempo

**Sustentabilidade:**

- Percentual de resíduos reciclados vs. aterrados
- Evolução da destinação ao longo do tempo (via SCD2)
- Clientes com melhor taxa de reciclagem

**Eficiência:**

- Correlação entre capacidade do caminhão e taxa de ocupação
- Otimização de rotas (análise de km por coleta)
- Tempo de permanência médio por tipo de resíduo

---

### Melhorias Futuras Sugeridas

1. **DAGs:**
   - Implementar dependências entre DAGs (sensores)
   - Adicionar data quality checks
   - Notificações por email/Slack em caso de falha
   - Implementar testes unitários para funções

2. **Dados:**
   - Adicionar dimensão de tempo (dim_tempo)
   - Implementar agregações pré-calculadas (OLAP cubes)
   - Particionamento da tabela fato por data
   - Índices otimizados para queries comuns

3. **Infraestrutura:**
   - Migrar para Kubernetes para produção
   - Implementar CI/CD para DAGs
   - Backup automatizado dos bancos
   - Monitoring com Prometheus + Grafana
   - Adicionar autenticação OAuth no Airflow

4. **Código:**
   - Implementar classes nos arquivos `utils/` (atualmente vazios)
   - Centralizar constantes (nomes de colunas, paths)
   - Adicionar type hints
   - Documentação inline (docstrings)

5. **Segurança:**
   - Secrets management (AWS Secrets Manager, Vault)
   - Criptografia de dados sensíveis
   - Audit logs
   - Row-level security no PostgreSQL

---

### Referências e Documentação Adicional

- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Metabase Documentation](https://www.metabase.com/docs/latest/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [Kimball Dimensional Modeling](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)

---
