from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd


def check_employee_table():
    hook = PostgresHook(postgres_conn_id='data_db')
    df = pd.read_excel("/opt/airflow/files/dados_empresa_alternativa.xlsx", sheet_name='funcionarios')
    employee_list = df['id_funcionario'].tolist()
    placeholders = ','.join(['%s'] * len(employee_list))
    sql = f"SELECT * FROM alternativa.dim_funcionario WHERE id_funcionario in ({placeholders}) and fim_validade IS NULL"
    existing_employees = hook.get_records(sql, parameters=tuple(employee_list))

    for employee in existing_employees:
        id_funcionario = employee[1]

        filtro = df['id_funcionario'] == id_funcionario
        if not filtro.any():
            continue

        tipo_funcionario_val = df.loc[filtro, 'nome'].values[0]
        cargo_val = df.loc[filtro, 'cargo'].values[0]

        tipo_funcionario = tipo_funcionario_val == employee[2]
        cargo = cargo_val == employee[3]

        if not tipo_funcionario or not cargo:
            sql = 'UPDATE alternativa.dim_funcionario SET fim_validade = %s WHERE id_funcionario = %s and fim_validade IS NULL'
            hook.run(sql, parameters=(datetime.now(), id_funcionario))
        else:
            df = df[df['id_funcionario'] != id_funcionario]

    insert_client_data(df)
            
    


def insert_client_data(df):
    hook = PostgresHook(postgres_conn_id='data_db')
    sql = 'INSERT INTO "alternativa"."dim_funcionario" (id_funcionario, nome, cargo) VALUES (%s, %s, %s)'
    for index, row in df.iterrows():
        hook.run(sql, parameters=(int(row['id_funcionario']), row['nome'], row['cargo']))



# Definição da DAG
with DAG(
    dag_id="process_employee_data",
    description="Processa dados de funcionários da planilha e atualiza o banco de dados",
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
        python_callable=check_employee_table,
    )
    

    # Se houver mais tarefas, você pode encadear assim:
    process_data