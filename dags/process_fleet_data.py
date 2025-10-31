from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd


def check_fleet_table():
    hook = PostgresHook(postgres_conn_id='data_db')
    df = pd.read_excel("/opt/airflow/files/dados_empresa_alternativa.xlsx", sheet_name='frota')
    fleet_id_list = df['id_caminhao'].tolist()
    placeholders = ','.join(['%s'] * len(fleet_id_list))
    sql = f"SELECT * FROM alternativa.dim_frota WHERE id_caminhao in ({placeholders}) and fim_validade IS NULL"
    existing_fleets = hook.get_records(sql, parameters=tuple(fleet_id_list))

    for fleet in existing_fleets:

        id_fleet = fleet[1]

        filtro = df['id_caminhao'] == id_fleet
        if not filtro.any():
            continue
        
        placa_val = df.loc[filtro, 'placa'].values[0]
        modelo_val = df.loc[filtro, 'modelo'].values[0]
        capacidade_carga_val = df.loc[filtro, 'capacidade_carga_kg'].values[0]

        placa = placa_val == fleet[2]
        modelo = modelo_val == fleet[3]
        capacidade_carga = capacidade_carga_val == fleet[4]

        if not placa or not modelo or not capacidade_carga:
            sql = 'UPDATE alternativa.dim_frota SET fim_validade = %s WHERE id_frota = %s and fim_validade IS NULL'
            hook.run(sql, parameters=(datetime.now(), id_fleet))
        else:
            df = df[df['id_caminhao'] != id_fleet]
            
    insert_client_data(df)
            
    


def insert_client_data(df):
    hook = PostgresHook(postgres_conn_id='data_db')
    sql = 'INSERT INTO "alternativa"."dim_frota" (id_caminhao, placa, tipo_modelo, capacidade) VALUES (%s, %s, %s, %s)'
    for index, row in df.iterrows():
        hook.run(sql, parameters=(int(row['id_caminhao']), row['placa'], row['modelo'], row['capacidade_carga_kg']))



# Definição da DAG
with DAG(
    dag_id="process_fleet_data",
    description="Processa dados de frota da planilha e atualiza o banco de dados",
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
        python_callable=check_fleet_table,
    )
    

    # Se houver mais tarefas, você pode encadear assim:
    process_data