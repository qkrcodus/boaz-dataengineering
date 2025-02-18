#### 출처 : 보아즈 23기 김용현님 강의자료 , 데브원영
를 토대로 이해한 내용을 정리했습니다.

### Kafka란?
분산 스트리밍 플랫폼으로, 대량의 데이터를 처리하고 실시간으로 전송하는 데 사용된다.

cf ) 지난 시간에 배운 하둡은 배치로 동작하기에 실시간 처리에 적합하지 않다. 대용량 데이터를 한꺼번에 처리함으로 컴퓨팅 리소스는 효율적으로 사용한다.
실시간 처리를 원하면 Apache Kafka !

---
### Kafka의 구조
프로듀서 - 카프카 클러스터 - 컨슈머

![](https://i.imgur.com/3IsfxWH.png)
![](https://i.imgur.com/9ICYJpS.png)

![](https://i.imgur.com/pcDmwjC.png)

---
### Partiton
broker 내 데이터가 저장되는 물리적 단위
![](https://i.imgur.com/svNGjGZ.png)
- 메시지를 쓸 땐? 가장 끝에
- 메시지 읽을 땐? 앞 -> 뒤 방향으로
- 파티션에 저장된 메시지는 순서랑 위치를 나타내는 offset 갖고 있다.
- 파티션은 여러 broker 에 걸쳐 수평적으로 나누어져 저장된다. ( 복제되어 저장된다는 뜻이다. )

---
#### Partition Replication
- 파티션 리더 - 모든 쓰기 작업은 리더를 통해 이루어진다.
- 파티션 팔로워 - 쓰기 작업이 불가능하다.
- 리더 장애시 ISR( 리더 파티션과 팔로워 파티션이 모두 싱크된 것)되어 있다면, 팔로워 중 하나가 리더로 선출된다.
![](https://i.imgur.com/NyMfaAE.png)
---
### Topic
여러 파티션을 하나로 묶는 논리적 개념
![](https://i.imgur.com/nZzkyki.png)

![](https://i.imgur.com/thZNc8p.png)
- 하나의 토픽에 대해 여러 프로듀서가 발행 가능하고 여러 컨슈머가 구독할 수 있다.
- 디렉토리랑 비슷하다.

---
### Broker
데이터를 받고 보내는 서버다. broker 들이 모여 kafka cluster 를 구성한다.
![](https://i.imgur.com/6Tg7wkC.png)
- 토픽 내 파티션 데이터 복제 , 브로커 관리
- 한 브로커 안에 여러 토픽이 있을 수도 있다.

---
### Producer
데이터를 발행하는 클라이언트 = 데이터를 카프카 토픽에 쓴다.
ex ) 엄청난 양의 클릭 로드를 실시간으로 카프카에게 전달할 때 프로듀서를 사용한다.

![](https://i.imgur.com/igjjClz.png)
- 토픽에 전송할 메시지를 생성
- 특정 토픽으로 데이터를 publish
- 전송 실패하면 재시도

카프카 클라이언트 버전과 브로저 버전 꼭 확인하자
![](https://i.imgur.com/hITMODm.png)
#### 프로듀서를 위한 설정
![](https://i.imgur.com/a51y09D.png)부트스트랩 서버 설정이 localhost의 카프카 를 바라보게 설정
key( 파티션의 위치를 알려주는 ) 와 value 를 시리얼라이저를 통해 직렬화해준다.

![](https://i.imgur.com/O34dL6S.png)
카프카 프로듀서 인스턴스를 만들어 주고
record 객체를 만들어 click -log 토픽에 login value메시지를 보낸다.

#### 키가 없을 때 메시지는 파티션에 어떻게 저장될까?
round robin 방식으로 파티션에 차곡차곡 쌓인다
 
![](https://i.imgur.com/bgURKpe.png)

#### 키가 존재할 때 메시지는 파티션에 어떻게 저장될까?
key -> 파티션과 1:1 매핑되나 파티션 추가하게 되면 일관성 보장되지 않는다
![](https://i.imgur.com/x9zoevD.png)
![](https://i.imgur.com/8eoTE5z.png)

---
#### Consumer
데이터를 컨슈머가 가져가도 데이터는 사라지지 않는다
polling : 토픽내부의 파티션에서 데이터를 가져온다. 
![](https://i.imgur.com/dXPzIvr.png)
- partition 으로부터 데이터 polling
- 파티션에 있는 데이터 번호인 offset을 commit 한다
- consumer group 통해 병렬 처리

#### 컨슈머를 위한 설정
![](https://i.imgur.com/EPvDbwa.png)

부트스트랩 서버에 브로커를 연결한다.
컨슈머 그룹을 group id 로 묶고 직렬화 설정을 해준다.
consumer 인스턴스를 만들고, 어느 토픽에서 데이터를 가져올지 subscribe 구독 설정을 해준다.

파티션에 들어간 데이터는 offset 은 컨슈머가 어디까지 데이터를 읽었는지 확인하는 용도로 쓰인다.
( 컨슈머는 읽은 offset을 consumer_offset 에 저장한다 )
![](https://i.imgur.com/wYbKlcf.png)

컨슈머 개수는 파티션 개수보다 적거나 같아야 한다.
![](https://i.imgur.com/SUONUYR.png)

백업을 위해 하둡에 데이터를 저장하는 컨슈머 그룹을 만들어도, 컨슈머들끼린 consumer offset 을 공유하지 않기에 어디까지 데이터를 폴링해왔는지 알지 못한다.
![](https://i.imgur.com/FRBuXtV.png)

---
### Kafka의 장점과 단점
장점
1. 높은 처리량 : 메시지를 배치처리하므로 네트워크 통신 비용을 줄여 단위 시간 내 더 많은 양의 데이터를 전송할 수 있다.
2. 고가용성 : 브로커를 클러스터링 하므로 일부 브로커가 장애가 나도 상관없다.
3. 높은 확장성 : 손쉽게 스케일 아웃 가능하다.

단점
1. 높은 학습 곡선
2. 클러스터 관리, 토픽 구성, 파티션 관리 등 복잡한 설정과 유지 관리가 필요하다.

