from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd


def check_waste_table():
    hook = PostgresHook(postgres_conn_id='data_db')
    df = pd.read_excel("/opt/airflow/files/dados_empresa_alternativa.xlsx", sheet_name='residuos')
    waste_id_list = df['id_residuo'].tolist()
    placeholders = ','.join(['%s'] * len(waste_id_list))
    sql = f"SELECT * FROM alternativa.dim_residuo WHERE id_residuo in ({placeholders}) and fim_validade IS NULL"
    existing_wastes = hook.get_records(sql, parameters=tuple(waste_id_list))

    for waste in existing_wastes:
        id_residuo = waste[1]

        filtro = df['id_residuo'] == id_residuo
        if not filtro.any():
            continue
        
        tipo_residuo_val = df.loc[filtro, 'tipo_residuo'].values[0]
        tratamento_val = df.loc[filtro, 'destinacao'].values[0]

        tipo_residuo = tipo_residuo_val == waste[2]
        tratamento = tratamento_val == waste[3]

        if not tipo_residuo or not tratamento:
            sql = 'UPDATE alternativa.dim_residuo SET fim_validade = %s WHERE id_residuo = %s and fim_validade IS NULL'
            hook.run(sql, parameters=(datetime.now(), id_residuo))
        else:
            df = df[df['id_residuo'] != id_residuo]
            
    insert_client_data(df)
            
    


def insert_client_data(df):
    hook = PostgresHook(postgres_conn_id='data_db')
    sql = 'INSERT INTO "alternativa"."dim_residuo" (id_residuo, tipo_residuo, tratamento) VALUES (%s, %s, %s)'
    for index, row in df.iterrows():
        hook.run(sql, parameters=(int(row['id_residuo']), row['tipo_residuo'], row['destinacao']))



# Definição da DAG
with DAG(
    dag_id="process_waste_data",
    description="Processa dados de resíduos da planilha e atualiza o banco de dados",
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
        python_callable=check_waste_table,
    )
    

    # Se houver mais tarefas, você pode encadear assim:
    process_data