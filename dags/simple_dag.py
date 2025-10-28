from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

# Função que será executada pela DAG
def hello_world():
    print("Hello, I'm Alive. Airflow 3.1.0!")
    df = pd.read_excel("/opt/airflow/files/dados_empresa_alternativa.xlsx")
    print(df.head())

# Definição da DAG
with DAG(
    dag_id="simple_hello_dag",
    description="Uma DAG simples de exemplo",
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
    task_hello = PythonOperator(
        task_id="print_hello",
        python_callable=hello_world,
    )

    # Se houver mais tarefas, você pode encadear assim:
    # task_hello >> outra_tarefa