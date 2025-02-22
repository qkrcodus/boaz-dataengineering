#### 출처 : 보아즈 23기 김건형님 강의자료 , 미쿸엔지니어
를 토대로 이해한 내용을 정리했습니다.

### Apache Airflow
프론트엔드의 요청으로 백엔드 서버에 이벤트들이 하나씩 생성된다. 
각 이벤트들을 모이고 real time 또는 batch로 처리된다. 

이벤트들은 데이터 파이프라인에 따라 ETL 과정을 거치고 
1. database 에 저장되거나
2. tenserflow, pytorch 와 같은 머신러닝 도구를 사용해 모델을 저장하거나
3. 빅데이터 시각화 도구에게 전달된다.

![](https://i.imgur.com/jhVZqn4.png)

즉, 데이터 파이프라인은 ( workflow ) ETL 과정을 거치고 이 파이프라인의 개수는 아주 많다.

따라서, 수많은 데이터 파이프라인( workflow )들을 한 번에 관리해주는 orchestrator : Apache Airflow 를 사용한다. 

- 하나의 workflow 는 DAG 이다. / 하나의 workflow 를 공유하는 이벤트들은 같은 데이터 파이프라인을 타고 이동한다. 
- 선후행 관계가 있는 Task들을 연결한게 DAG 이다. 
- DAG는 순환되지 않는다.
- Cron 기반 스케줄링 된다. ( Task 의 실행 시간과 주기를 정해준다.)
---
### Airflow Operator
task 들은 operator 로 정의된다. 실습에선 python 함수 실행하는 pythonOperator 사용

---
### Airflow XCom
DAG 는 순차적인 task로 구성된다.
DAG 내 task 사이 데이터를 전달하기 위해 사용되는게 Airflow XCom. 데이터는 DAG 내서만 공유.
- xcom_push : 데이터 송신
- xcom_pull : 데이터 수신
---
#### DAG 예시와 설명
e , t, l 에 해당한 함수를 extract_data , transform_data,load_data 로 정의하고 task가 돌 때 함수가 호출되게 한다.
테스크 순서도 정의해준다.
![](https://i.imgur.com/R9Vekma.png)

![](https://i.imgur.com/IG5gS40.png)
### 실습
---
- Docker Compose 파일 다운로드
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.3/docker-compose.yaml'

- 디렉토리 구조 생성
mkdir -p ./dags ./logs ./plugins ./config

- 환경 설정
echo -e "AIRFLOW_UID=$(id -u)" > .env && \
sed -i '' 's/AIRFLOW__CORE__LOAD_EXAMPLES: '\''true'\''/AIRFLOW__CORE__LOAD_EXAMPLES: '\''false'\''/' docker-compose.yaml

- 초기화 및 실행
docker compose up airflow-init
docker compose up -d

---
- dags 디렉토리 내부에 파이썬 코드를 넣어준다.
---
실행시키면 3개의 task 가 success 되고, 3을 클릭하면 각 task 에 대한 log 를 볼 수 있다.
![](https://i.imgur.com/JAkusvY.png)
graph

![](https://i.imgur.com/QWMcd5x.png)

---
즉, 요약하자면 무수히 많은 데이터 파이프라인을 종합적으로 관리하기 위해 Apache Airflow를 사용한다.
데이터 파이프라인의 workflow 는 단방향의 DAG 구조로 되어있다. 
사용자는 airflow 를 사용하기 위해 
1. 작업 실행하는 단위인 operator
2. 작업 순서인 DAG과 이를 이루는 task
3. task 실행 방식인 executor 를 설정한다.

부가적으로 task가 실행되는 주기를 cron, task 들끼리 데이터를 주고받는 과정을 xcom 으로 정의해둔다.

---
### 과제
로컬에 간단한 api를 띄워 1분마다 요청을 보내는 DAG 작성
요청 주소: [`http://host.docker.internal:8000/`](http://host.docker.internal:8000/) (docker 내부에서 localhost를 지정하는 형식)