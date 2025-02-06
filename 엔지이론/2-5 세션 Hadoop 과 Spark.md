#### 출처 : 보아즈 23기 이지윤님 강의자료
를 토대로 이해한 내용을 정리했습니다.

[ 지난 주 복습 ]
##### docker 로 컨테이너 하나씩 생성할때 
![](https://i.imgur.com/Xd5ZWxK.png)
- docker build : dockerfile 이나 docker-compose.yml을 이용하여 이미지를 생성
- docker pull : registry에서 이미지를 풀 받아서 로컬 도커 데몬에 저장
- docker run : 지정된 이미지를 실행하여 컨테이너를 만듦

##### docker compose 로 한 번에 여러 컨테이너를 실행할 때
- docker-compose.yml 에 image 지시어를 사용해서 외부에서 제공되는 이미지를 지정한다. ( docker pull 과정 )
- docker-compose up 은 이미지를 빌드하고 서비스를 실행해준다. ( docker pull & docker run 과정 )
---
#### Hadoop 핵심 구성 요소 ( HDFS, YARN, MapReduce)
##### 1. HDFS (Hadoop Distributed File System)
대규모 데이터를 분산 저장하는 파일 시스템
###### 마스터-슬레이브 구조
- NameNode (마스터): 메타데이터 관리 (파일명, 블록 위치, 권한 등)
- DataNode (슬레이브): 실제 데이터 블록 저장 및 클라이언트 요청 처리

![](https://i.imgur.com/Cv8KsNG.png)

##### 2. YARN (Yet Another Resource Negotiator)
클러스터 내 자원(메모리, CPU 등) 관리 및 작업 스케줄링
###### 구조
- ResourceManager (마스터): 전체 클러스터 자원 관리 및 스케줄링
-Scheduler( 우선 순위 관리 ) , ApplicationManager ( Client의 작업 요청을 검토 )
- NodeManager (슬레이브): 클러스터의 각 노드에서 자원(CPU, 메모리 등) 관리 및 작업 실행 환경(Container) 관리
- ApplicationMaster: 각 애플리케이션의 자원 요청 및 작업 관리 담당
###### 작동 방식
![](https://i.imgur.com/69pUe30.png)
- client -> resource manager 작업 제출
- resource manager 의 application manager 요청 수락
- node manager 에 application master 컨테이너 생성 요청
- application master 는 resource manager scheduler 에 자원 요청하고 확인 후 할당
- node manager 는 컨테이너 생성하고 작업 실행
- application master 는 모니터링 하며  resource manager에 작업 완료 보고
##### 3. MapReduce (데이터 처리 프레임워크)
대규모 데이터를 <Key, Value> 쌍으로 병렬로 처리

- **Mapper**: 입력 텍스트 파일을 읽고 각 단어를 키(key)로, 숫자 1을 값(value)으로 매핑합니다. 예를 들어, 문장 "hello world hello"가 입력되면, Mapper의 출력은 다음과 같습니다:
    
    - (hello, 1)
    - (world, 1)
    - (hello, 1)
- **Reducer**: Mapper의 출력을 받아 동일한 키를 가진 데이터의 값을 합산합니다. 위의 예에서 Reducer는 다음과 같은 결과를 생성합니다:
    
    - (hello, 2)
    - (world, 1)
#### Hadoop 에코시스템
- Hadoop Core
HDFS, MapReduce, YARN ( 저장, 처리, 관리 담당 )
- Hadoop 에코시스템
 Hadoop Core 위에서 동작하는 다양한 도구들 그 중 spark ( 실시간 처리 )를 더 살펴볼거다

#### Hadoop의 특징, 한계
- 특징
수천대 서버로 확장 가능, replica 를 둬서 데이터 손실 최소화, 대규모 데이터 처리 가능, 오픈소스라 수정 가능
- 한계
배치 처리 방식이라 실시간 분석 어려움 -> spark 로 보완가능
초기 설정 관리 복잡, 클러스터 유지에 많은 하드웨어 자원 필요

---
#### 실습
##### 1. 도커 설치 후 도커 켜주자.
도커는 애플리케이션을 가상화 기술을 사용하는  컨테이너라는 격리된 환경에서 실행하기 위한 플랫폼이다. 
도켜를 켜서 컨테이너를 생성하고 관리하는 상태로 만들자.

##### 2. hadoop-spark-cluster 디렉토리를 만들고 그 안에 docker-compose.yml 파일을 작성하자.
![](https://i.imgur.com/ZJpD7mh.png)

다중 컨테이너를 생성하고 관리할 때 필요한 설정들을 담은 docker-compose.yml 
( 주석 참고! )

- 정의된 컨테이너들 : NameNode, DataNode (HDFS), ResourceManager, NodeManager (YARN), Spark Master, Spark Worker (spark) 

![](https://i.imgur.com/LcSwmhA.png)

![](https://i.imgur.com/gQFAPr5.png)

![](https://i.imgur.com/IYaw4ND.png)

ports 라고 된 부분은 도커 호스트 ( 내 로컬 ) 포트와 컨테이너 포트를 연결해줬단 뜻이다.

![](https://i.imgur.com/GbjjB95.png)


![](https://i.imgur.com/H5sLMxH.png)

![](https://i.imgur.com/hGTyCc7.png)

![](https://i.imgur.com/xL3DTE5.png)
![](https://i.imgur.com/z0DFAKF.png)

[ nano 에디터 사용할 땐, control +0 , enter , control + X 로 저장하고 에디터를 나간다. ]

---
#### Hadoop MapReduce로 Word Count 실습
Hadoop 핵심 구성 요소 ( HDFS - 저장 , YARN - 자원 관리 , MapReduce - 처리) MapReduce 를 사용해보자.
##### NameNode 컨테이너에 접속
docker exec -it namenode bash
##### 샘플데이터 저장하고 하둡 HDFS에 업로드
echo -e "Hello Hadoop and Spark\nBig Data Big Value\nHello World" > sample.txt
hdfs dfs -mkdir -p /user/test
hdfs dfs -put sample.txt /user/test

-p /user/test 로 상위 디렉토리까지 생성후 여기에 sample.txt 를 업로드한다.
##### WordCount MapReduce 실행
hadoop jar /opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar wordcount /user/test/sample.txt /user/test/output_mr

##### 결과 데이터 출력하기
hdfs dfs -cat /user/test/output_mr/part-r-00000
![](https://i.imgur.com/coGrypb.png)

root@9cd03c948b8d:/# 는 현재 컨테이너에 들어와있다는 뜻  => control + d 로 나오기

---
#### 과제 1 head -n 20 ( 첫 20 줄) 을 map reduce 방식으로
1. hadoop-spark-cluster 폴더에 moby_dict.txt 저장한 뒤, 컨테이너에 파일을 복사한다.
nano moby_dict.txt 
복붙하고 control +0 , enter , control + X 로 저장하고 에디터를 나간다. 

2. 현재 디렉토리에 있는 moby_dict.txt 를 namenode 컨테이너 아래 moby_dict.txt 이름으로 복사한다. 
docker cp ./moby_dict.txt namenode:/moby_dict.txt

3. 첫 20 줄만 뽑아서 새로운 txt 파일을 만든다.
head -n 20 moby_dict.txt > first20_moby_dict.txt

4. 로컬에서 Docker 컨테이너로 파일을 복사한다.
docker cp ./first20_moby_dict.txt namenode:/first20_moby_dict.txt

5. `namenode` 컨테이너에 접속한다.
docker exec -it namenode bash

이전에 
hdfs dfs -mkdir -p /user/test 
hdfs dfs -put sample.txt /user/test 로 디렉토리를 만들어 뒀기에

6. 컨테이너 내부에서 HDFS 명령을 사용하여 파일을 HDFS에 업로드한다.
hdfs dfs -put /first20_moby_dict.txt /user/test 
![](https://i.imgur.com/wop2CSF.png)

7. 하둡에 내장된 wordcount 로 출력파일을 만들자.
hadoop jar /opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar wordcount /user/test/first20_moby_dict.txt /user/test/first20_moby_dict_count

8. 출력파일 목록 확인하자.
hdfs dfs -ls /user/test/first20_moby_dict_count

![](https://i.imgur.com/Tt7Vc21.png)


9. 결과 데이터 확인하자.
hdfs dfs -cat /user/test/first20_moby_dict_count/part-r-00000

![](https://i.imgur.com/KuF2DDF.png)

![](https://i.imgur.com/Wu2wjtz.png)