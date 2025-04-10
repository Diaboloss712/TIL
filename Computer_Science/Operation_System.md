# 운영체제

## 운영체제의 역할

자원 할당 및 관리, 프로세스 및 스레드를 관리하는 기능이 있다.

자원은 한정되어있기에 CPU나 메모리, 스레드 등의 자원을 분배하는 역할을 한다.

프로그램을 메모리에 적재하고 삭제를 하는데, 메모리 용량에 한계가 있기에 가상 메모리를 통해 관리한다.

보조기억장치를 효율적으로 관리하기 위해 파일 시스템을 활용한다.


## 커널


## 프로세스 및 스레드 관리
PCB
타이머 인터럽트

## 프로세스
프로세스의 상태
블로킹 입출력과 논블로킹 입출력
- pending 하고 다음 명령어 수행

## 스레드
프로세스에서 스택을 독자적으로 가짐 (독자적인 함수)
데이터 수정시 문제 발생 가능
공유 메모리
파이프

## 동기화와 교착 상태
레이스 컨디션
임계 구역?
뮤텍스 락
세마포(카운팅 세마포)
교착 상태의 발생 조건과 회피, 회복

## CPU 스케줄링

CPU 스케줄링이란? : CPU의 사용을 배분하는 방법이다.

실행의 문맥이 있는 모든 것은 CPU 스케줄링의 대상이다.

운영체제는 프로세스별 우선순위를 판단하여 PCB에 명시하고, 우선순위가 높은 프로세스에게 우선적으로 자원을 할당한다.


### 운영체제의 우선순위 할당 기준

CPU 활용률은 전체 CPU 가동 시간 중 작업을 처리하는 시간의 비율로 입출력이 많은 프로세스들이 주로 할당받는다.

프로세스가 CPU를 이용하는 것을 CPU 버스트, 입출력장치를 기다리는 작업을 입출력 버스트라고 한다.

입출력 작업이 많은 프로세스는 입출력 집중 프로세스, CPU 집중이 많은 프로세스는 CPU 집중 프로세스라고 부르는데,

입출력 집중 프로세스는 대기 시간이 많기 때문에 우선순위를 높게 두어 빨리 실행시켜두고 CPU 집중 프로세스를 처리한다.


### 스케줄링 큐

자원이 필요한 프로세스들에게 대기표를 뽑아주는 방식

준비 큐 : CPU를 이용하려는 PCB들을 위한 대기표

대기 큐 : 대기 상태에 접어든 PCB들을 위한 대기표

입출력 작업을 수행하면 대기 큐에서 대기 상태로 완료 인터럽트를 기다리게 된다.

준비 상태인 PCB는 준비 큐의 마지막에 삽입되어 CPU 대기순번을 기다린다.

하지만 대기표를 뽑아도 우선순위가 존재하여 우선순위를 우선하여 뽑는다. (VIP)

실행된 프로세스가 상담 시간을 모두 소모하면 상태에 따라 준비 큐 또는 대기 큐로 이동한다.

대기 큐에서 작업이 완료되면 PCB를 준비 상태로 변경한 후 큐에서 제거한다.

(대기 큐가 끝나고 준비 큐로 가는 이유 : 프로세스 종료, 입출력 처리 후의 연산 등 CPU가 필요)


### CPU 스케줄링 알고리즘

1. 선입 선처리 알고리즘
   - 준비 큐에 삽입한 순서대로 CPU를 할당하는 스케줄링 방식
   - 때때로 대기 시간이 길어질 수 있고, 호위 효과가 발생할 수 있다.
2. 최단 작업 우선 스케줄링
   - 준비 큐에 있는 프로세스 중 시간의 길이가 가장 짧은 프로세스부터 처리하는 방식
   - 기본적으로 비선점형 스케줄링이다.
3. 라운드 로빈 스케줄링
   - 선업 선처리 스케줄링에 타임 슬라이스라는 개념을 더했다.
   - 타임 슬라이스 : CPU를 사용할 수 있는 시간이 정해진 것을 말한다.
   - 선점형 스케줄링이며, 완료되지 않으면 맨 뒤로 돌아간다.
4. 최소 잔여 시간 우선 스케줄링
   - 최단 작업 우선 스케줄링과 라운드 로빈 스케줄링을 합친 방식
   - 가장 짧은것부터 정해진 시간을 할당한다.
5. 우선순위 스케줄링
   - 프로세스에 우선순위를 부여하고, 가장 높은 우선순위를 가진 프로세스부터 실행하는 방식
   - 우선순위가 낮으면 계속해서 연기되는 아사 현상이 발생
   - 오랫동안 대기할 수록 우선순위를 높이는 에이징을 적용하면 해결 가능하다.
6. 다단계 큐 스케줄링
   - 우선순위 스케줄링의 발전된 형태로, 여러 개의 준비 큐를 사용한다.
   - 우선순위가 높은 준비 큐부터 처리한다. 그렇기에 아사 현상이 발생할 수 있다.
7. 다단계 피드백 큐 스케줄링
   - 프로세스들이 큐 사이를 이동할 수 있다.
   - 새로 진입하는 프로세스는 가장 높은 우선순위 큐에 삽입되고, 타임 슬라이스 동안 실행된다.
   - 처리가 끝나지 않으면 다음 우선순위 큐에 삽입되어 실행되는게 반복된다.
   - 점차적으로 우선순위가 낮아지기에 오래 기다리는 프로세스들은 자동적으로 우선순위가 높아진다.


## 리눅스 CPU 스케줄링

리눅스 운영체제에는 스케줄링 정책이 다음과 같다.
|스케줄링 정책| 적용 상황|
|---|---|
|SCHED_FIFO|
<table>
  <tr>
    <th>제목1</th>
    <th colspan="2">제목2</th>
  </tr>
  <tr>
    <td rowspan="2">내용1</td>
    <td>내용2</td>
    <td>내용3</td>
  </tr>
  <tr>
    <td colspan="2">내용4 (셀 병합)</td>
  </tr>
</table>