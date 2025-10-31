# Eixo04 - Orquestração de Dados com Airflow, Docker, PostgreSQL e Metabase - Alocação de Caçambas Alternativa

Este projeto é uma stack completa para orquestração de pipelines de dados utilizando Apache Airflow, bancos PostgreSQL, Metabase (BI) e Docker. O objetivo é facilitar a ingestão, atualização e visualização de dados de clientes a partir de arquivos Excel, com automação e rastreabilidade.

---

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
