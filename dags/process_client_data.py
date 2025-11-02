from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd


def check_client_table():
    hook = PostgresHook(postgres_conn_id='data_db')
    df = pd.read_excel("/opt/airflow/files/dados_empresa_alternativa.xlsx", sheet_name='clientes')
    df['tipo_cliente'] = df['tipo_cliente'].apply(lambda x: 'PF' if x == 'Pessoa Física' else 'PJ')
    client_id_list = df['id_cliente'].tolist()
    placeholders = ','.join(['%s'] * len(client_id_list))
    sql = f"SELECT * FROM alternativa.dim_cliente WHERE id_cliente in ({placeholders}) and fim_validade IS NULL"
    existing_clients = hook.get_records(sql, parameters=tuple(client_id_list))
    
    for client in existing_clients:
        id_cliente = client[1]

        filtro = df['id_cliente'] == id_cliente
        if not filtro.any():
            continue

        nome_val = df.loc[filtro, 'nome_cliente'].values[0]
        tipo_val = df.loc[filtro, 'tipo_cliente'].values[0]
        cidade_val = df.loc[filtro, 'cidade'].values[0]

        nome = nome_val == client[2]
        tipo = tipo_val == client[3]
        cidade = cidade_val == client[4]

        if not nome or not tipo or not cidade:
            sql = 'UPDATE alternativa.dim_cliente SET fim_validade = %s WHERE id_cliente = %s and fim_validade IS NULL'
            hook.run(sql, parameters=(datetime.now(), id_cliente))
        else:
            df = df[df['id_cliente'] != id_cliente]
            
    insert_client_data(df)
            
    


def insert_client_data(df):
    hook = PostgresHook(postgres_conn_id='data_db')
    sql = 'INSERT INTO "alternativa"."dim_cliente" (id_cliente, nome, tipo_cliente, cidade) VALUES (%s, %s, %s, %s)'
    for index, row in df.iterrows():
        hook.run(sql, parameters=(int(row['id_cliente']), row['nome_cliente'], row['tipo_cliente'], row['cidade']))



# Definição da DAG
with DAG(
    dag_id="process_client_data",
    description="Processa dados de clientes da planilha e atualiza o banco de dados",
    schedule="@daily",  # roda todo dia
    start_date=datetime(2025, 10, 28),
    catchup=False,  # não executa retroativamente
    default_args={
        "owner": "airflow",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:

    # Tarefa usando PythonOperator
    process_data = PythonOperator(
        task_id="process_data",
        python_callable=check_client_table,
    )
    

    # Se houver mais tarefas, você pode encadear assim:
    process_data