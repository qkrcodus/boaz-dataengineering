### `kafka connect` : 데이터베이스와 같은 외부 시스템과 카프카를 손쉽게 연결하기 위한 프레임워크

그림과 같이 카프카 클러스터를 먼저 구성한 후 카프카 클러스터 양쪽 옆에 배치 할 수 있다.

1. 카프카의 producer 역할 → source connector
2. 카프카의 consumer 역할 → sink connector

![](https://i.imgur.com/JNTSQRU.png)

## Kafka Connect를 이용한 MySQL 테이블의 변경 데이터 스트리밍 및 연동

목표 : mysql table에 데이터를 insert하면 다른 table에 데이터가 그대로 저장되는지 확인하기

Connect: Connector를 동작하게 하는 프로세서(서버)
Connector:  Data Source(DB)의 데이터를 처리하는 소스가 들어있는 jar파일

Connect 을 실행해야 Connector 사용이 가능하다.

### 1. MySQL 설치 및 세팅하기 - 비번 기억해주세요
#### 2. MySQL 서버 시작하기
mysql.server start
#### 3. MySQL 서버 접속하기
mysql -u root -p
#### 4. test라는 이름의 데이터베이스를 생성
CREATE SCHEMA test;
#### 5. test 데이터베이스 안에 users라는 이름의 테이블을 생성
CREATE TABLE test.users ( id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(20) );

// 테이블 잘 만들어졌는지 확인하기 DESCRIBE test.users;

user테이블에 id와 name 두 개의 필드가 만들어진 것을 확인할 수 있다.
![](https://i.imgur.com/xGnm4SI.png)

### 6. `kafka` 설치

새 터미널창을 열고 바탕화면에 `kafka-connect` 디렉토리를 만들고 그 안에 설치해주고 압축을 풀어줍니다.

```bash
curl -o kafka_2.13-3.9.0.tgz [<https://downloads.apache.org/kafka/3.9.0/kafka_2.13-3.9.0.tgz>](<https://downloads.apache.org/kafka/4.0.0/kafka_2.13-4.0.0.tgz>)
```

```bash
tar xvf kafka_2.13-3.9.0.tgz
```

```bash
cd kafka_2.13-3.9.0
```

`kafka_2.13-3.9.0` 디렉토리로 들어온 뒤
vi config/server.properties
![](https://chestnut-crane-417.notion.site/image/attachment%3A9d2f24d3-4e6a-4776-9800-373906995b66%3A811be87a-b44e-452a-a557-8c1cf7c4c253.png?table=block&id=1cf2e060-208a-805f-a08e-f3c7bd38f1b0&spaceId=24fe3dc2-8ecf-4caa-af5e-4956d13428f0&width=1340&userId=&cache=v2)

### 7. 카프카 클러스터 만들기 - 주기퍼 실행

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

### 2181번 포트가 이미 사용중이라는 에러가 뜬다면 ( Address already in use )

프로세스 PID를 확인하고

```sql
sudo lsof -i :2181
```

프로세스를 종료 해준 뒤 다시 주기퍼를 실행해주세요.

```sql
kill -9 [PID]
```

‼️ 주기퍼가 먼저 실행되어야 브로커가 정상적으로 실행됩니다. 주기퍼 실행되는지 확인 후 넘어가주세요

### 8. 카프카 클러스터 만들기 - 브로커 실행

새로운 터미널창을 열고 `kafka_2.13-3.9.0` 디렉토리로 이동

```bash
bin/kafka-server-start.sh config/server.properties
```

‼️ 주기퍼가 먼저 실행되어야 브로커가 정상적으로 실행됩니다. 주기퍼 실행되는지 확인 후 넘어가주세요

![](https://i.imgur.com/v66M5pJ.png)

### 9. Kafka Connect 실행

<aside> 💡

Connect: Connector를 동작하게 하는 프로세서(서버)

Connector:  Data Source(DB)의 데이터를 처리하는 소스가 들어있는 jar파일

Connect 을 실행해야 Connector 사용이 가능하다.

</aside>

새로운 터미널창을 열고 `kafka_2.13-3.9.0` 디렉토리로 이동
```bash
bin/connect-distributed.sh config/connect-distributed.properties
```

### connect 잘 실행 되었는지 확인하기

새로운 터미널창을 열고 `kafka_2.13-3.9.0` 디렉토리로 이동

```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```
위 명령어 결과 총 4개의 토픽이 나오면 성공!

![](https://i.imgur.com/BEJPlxi.png)

### 관계형 데이터베이스(RDBMS)와 Kafka 간의 통신을 위해 JDBC Connector를 설치

### 10-1. Connector 설치 - JDBC Connector

아래 zip 파일을 압축 해제한 파일만 `kafka-connect`디렉토리에 넣기

‼️ 현재까지 구조
![](https://i.imgur.com/lKK61ss.png)

`kafka_2.13-3.9.0` 디렉토리에서

```bash
vi config/connect-distributed.properties
```

`plugin.path` 설정을 바꿔줍니다. ( ‼️ **Kafka Connect가 사용할 커넥터**을 찾는 디렉토리 경로를 알려주기 )

맨 아래 주석을 풀고 아래 처럼 적어준 뒤 저장하고 나와줍니다.

```bash
plugin.path=/Users/yourusername/path/to/confluentic-kafka-connect-jdbc-10.8.2
```

```bash
plugin.path=/Users/parkchaeyeon/Desktop/kafka-connect/confluentinc-kafka-connect-jdbc-10.8.2
```

<aside> 📌

### Kafka JDBC Connector의 JAR 파일에는 기본적으로 MySQL 드라이버가 포함되어 있지 않음 → 사용자가 사용하는 DB에 맞는 JDBC 드라이버를 직접 추가

</aside>

### 10-1. Connector 설치 - mysql Connector
위 파일 압축 해제 후 `mysql-connector-java-버전.jar` 파일을 복사하여 `confluentinc-kafka-connect-jdbc-10.8.2/lib` 아래 붙여넣습니다.

jar파일들 (Connector 들)을 모두 **Kafka Connect 가 인식 할 수 있습니다.**

Connect: Connector를 동작하게 하는 프로세서(서버)
Connector:  Data Source(DB)의 데이터를 처리하는 소스가 들어있는 jar파일

![](https://i.imgur.com/JYT2faD.png)

### 11. 수정 사항이 생겼으니 Kafka Connect 실행하고 있었던 터미널을 종료한뒤 다시 실행해줍니다.

### 12. Connect의 REST API를 통해 Source Connector 생성하기
```bash
curl -X POST -H "Content-Type: application/json" -d '{ "name": "test1-for-source-connect", "config": { "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector", "connection.url": "jdbc:mysql://localhost:3306/{db명}", "connection.user": "root", "connection.password": "{비번}", "mode": "incrementing", "incrementing.column.name": "id", "table.whitelist": "users", "topic.prefix": "example_topic_", "tasks.max": "1" } }' http://localhost:8083/connectors
```
config.table.whitelist : 데이터를 변경을 감지할 table 이름

config.topic.prefix : kafka 토픽에 저장될 이름 형식 지정 위 같은경우 whitelist를 뒤에 붙여 example_topic_users 토픽에 데이터가 들어감

생성한 source connector 가 작동 중인지 확인하기
```bash
curl http://localhost:8083/connectors/test1-for-source-connect/status
```

### 12. test.users table에 데이터를 insert 하기

```sql
INSERT INTO test.users (name) VALUES ('boaz');
```

topic 리스트를 확인

```bash
./bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

`example_topic_users`가 추가됨
![](https://i.imgur.com/V2vo8ek.png)

#### ‼️ DB에 데이터를 삽입함으로써 Source Connector가 DB데이터를 topic에 push한 것

#### 13. Connect의 REST API를 통해 Sink Connector 생성하기

이제 Source Connector를 통해 topic에 넣은 데이터를 Sink하기 위해 Sink Connector를 생성하자
```bash
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{ "name": "test1-for-sink-connect", "config": { "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector", "connection.url": "jdbc:mysql://localhost:3306/test", "connection.user": "root", "connection.password": "1266", "auto.create": "true", "auto.evolve": "true", "delete.enabled": "false", "tasks.max": "1", "topics": "example_topic_users" } }'
```

🍀 "topics": "example_topic_users" → Kafka에서 이 토픽의 데이터를 가져온다는 뜻

🍀 "auto.create": "true" → MySQL에 Kafka topic 이름과 동일한 테이블이 없으면 자동으로 생성함

### 14. 생성후 users table에 데이터를 insert하기

현재 상태다 ( pcy1 은 무시 , boaz 만 있으면 정상 )
![](https://i.imgur.com/jHaJFdM.png)

![](https://i.imgur.com/cR9Z7WW.png)
