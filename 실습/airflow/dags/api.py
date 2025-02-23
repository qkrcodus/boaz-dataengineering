from fastapi import FastAPI
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime, timedelta

app = FastAPI()

@app.get("/")
async def root():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"요청을 받았습니다! {current_time}")
    return {
        "message": "요청을 받았습니다!",
        "timestamp": current_time
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    dag_id='1_minute_request_dag',
    default_args=default_args,
    description='Send an HTTP request every minute',
    schedule_interval='* * * * *',  # cron 식으로 1분
    catchup=False
)

http_get_task = SimpleHttpOperator(
    task_id='1_minute_request_task',
    method='GET',
    http_conn_id='api_http_connection',
    endpoint='', 
    headers={"Content-Type": "application/json"},
    dag=dag
)
