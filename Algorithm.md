APS 기본 학습
- 입출력을 제외한 내장함수 사용하지 않기.
- 기본적인 내장함수의 동작원리 이해

정렬 알고리즘 비교
| 알고리즘 | 평균 수행시간 | 최악 수행시간 | 알고리즘 기법 | <center>비고</center> |
| :---: | :---: | :---: | :---: | :--- |
|버블 정렬 | O(n^2) | O(n^2) | 비교와 교환 | 코딩이 가장 손쉽다 |
|카운팅 정렬 | O(n+k) | O(n+k) | 비교환 방식 | n이 비교적 작을때만 가능하다 |
|선택 정렬 | O(n^2) | O(n^2) | 비교와 교환 | 교환의 횟수가 버블, 삽입 정렬보다 적다 |
|퀵 정렬 | O(n log n) | O(n^2) | 분할 정복 | 최악으로는 O(n^2)이지만, <br> 평균적으로는 가장 빠르다 |
|삽입 정렬 | O(n^2) | O(n^2) | 비교와 교환 | n의 개수가 작을 때 효과적이다. |
|합병 정렬 | O(n log n) | O(n^2) | 분할 정복 | 연결리스트의 경우 가장 효율적인 방식 |

안정성 : 동일한 키가 있을 때, "상대적 순서 보존"

적응성 : 초기 정렬 상태 => 실행 시간이 바뀌나

제자리 정렬 : 외부 메모리를 사용하는지

카운팅 정렬 O(n+k)
- 항목들의 순서를 결정하기 위해 집합에 각 항목이 몇 개씩 있는지 세는 작업
- 선형 시간에 정렬하는 효율적인 알고리즘

제한 사항
- 정수나 정수로 표현할 수 있는 자료에 대해서만 적용 가능
- 공간 할당을 위해 집합 내의 가장 큰 정수를 알고 있어야함

```
Data = [0, 4, 1, 3, 1, 2, 4, 1]
Counts = [1, 3, 1, 1, 1]
Pos_Counts = [1, 4, 5, 6, 8]

Count[0] = 1
Temp[Counts[]] = Data[Counts]
for num in Data:
    Temp[num-1] = num
    Counts[num] = Counts[num]-1

# Counts 구현
# Counts = [0] * len(set(Data))
# for i in Data:
#    Counts[i] += 1
```

순열 Permutation
- 서로 다른 것들 중 몇 개를 뽑아서 한 줄로 나열하는 것
- 서로 다른 n개 중 r개를 택하는 순열은 아래와 같이 표현한다.
``` nPr ```
- 그리고 nPr은 다음과 같은 식이 성립한다.
``` nPr = n * (n-1) * (n-2) * ... * (n-r+1) ```
- nPn = n!이라고 표기하며 Factorial이라 부른다.
``` n! = n * (n-1) * (n-2) * ... * 2 * 1 ```

탐욕 알고리즘

탐욕 알고리즘은 최적해를 구하는 데 사용되는 근시안적인 방법

여러 경우 중 하나를 결정해야 할 때마다 그 순간에 최적이라고 생각되는 것을 선택해 나가는 방식으로 진행하여 최종적인 해답에 도달한다.

각 선택의 시점에서 이루어지는 결정은 지역적으로 최적이지만, 그 선택들을 계속 수집하여 최종적인 해답을 만들었다고 하여, 그것이 최적이라는 보장은 없다.


탐욕 알고리즘의 동작 과정

1. 해 선택 : 현재 상태에서 부분 문제의 최적 해를 구한 뒤,

    이를 부분해 집합에 추가한다.

2. 실행 가능성 검사 : 새로운 부분해 집합이 실행 가능한지를 확인한다.

    곧, 문제의 제약 조건을 위반하지 않는지를 검사한다.

3. 해 검사 : 새로운 부분해 집합이 문제의 해가 되는지를 확인한다.

    아직 전체 문제의 해가 완성되지 않았다면 1)의 해 선택부터 다시 시작한다.


2차원 배열

- 1차원 List를 묶어놓은 List
- 2차원 이상의 다차원 List는 차원에 따라 Index를 선언
- 2차원 List의 선언 : 세로길이(행의 개수), 가로길이(열의 개수)를 필요로 함
- Python 에서는 데이터 초기화를 통해 변수선언과 초기화가 가능함

```
1. 2차원 배열 빈칸으로 구분되어 있을때 받는법
N = int(input)
arr = [list(map(int, input().split())) for _ in range(N)]

2. 빈칸이 없을때 받는법
N = int(input)
arr = [list(map(int, input())) for _ in range(N)]
```

비트 연산자
```
arr = [3,6,7,1,5,4]

n = len(arr)
# 부분 집합의 개수만큼
# 원수의 수만큼 비트를 비교하고
# i의 j번 비트가 1인경우
# j번 원소 출력
for i in range(1<<n):
    for j in range(n):
        if i & (1<<j):
            print(arr[j], end=", ")
```
---
---

Python에서의 문자열 처리
- char 타입 없음
- 텍스트 데이터의 취급방법이 통일되어 있음

- 문자열 기호
    ', ", ''', """
    + 연결(Concatenation)
        - 문자열 + 문자열 : 이어 붙이는 역할
    * 반복
        - 문자열 * 수 : 수만큼 문자열이 반복


Brute Force
- 본문 문자열을 처음부터 끝까지 차례대로 순회하면서 패턴 내의 문자들을 일일이 비교하는 방식으로 동작

---
---
KMP

보이어 무어 알고리즘
- 오른쪽에서 왼쪽으로 비교
- 패턴에 오른쪽 끝에 있는 문자가 불일치 하고 이 문자가 패턴 내에 존재하지 않는 경우, 이동 거리는 무려 패턴의 길이만큼이 된다.
- 최악의 경우 수행시간 : O(mn)

```
t = 'TTATATTATATATTTA'
p = 'TTA'


def search(p, t):
    N = len(t)
    M = len(p)
    for i in range(N-M+1):
        for j in range(M):
            if t[i+j] != p[j]:
                break
        else:               # break에 걸리지 않고 for가 끝난경우 실행
            return i        # 패턴이 처음 나타난 인덱스 리턴
    return -1

print(search(p, t))

---
---

Stack : 물건을 쌓아 올리듯 자료를 쌓아 올린 형태의 자료구조
- 후입선출

``` python
class Stack:
    top = -1

    def __init__(self, size=100):
        self.size = size
        self.top = -1
        self.items = [None] * size

    def push(self, item):
        self.top += 1
        self.items[self.top] = item

    def pop(self):
        item = self.items[self.top]
        self.items[self.top] = None
        self.top -= 1
        return item

    def peek(self):
        item = self.items[self.top]
        return item

    def is_empty(self):
        return self.top == -1

```

---
---

DP : 최적화 문제를 해결하는 알고리즘

``` python
def fibo2(n):
    f = [0] * (n+1)
    f[0] = 0
    f[1] = 1
    for i in range(2, n+1):
        f[i] = f[i-1] + f[i-2]
    return f[n]
```

DFS : 비선형구조를 가장 깊은곳부터 탐색하는 방법
- 가장 마지막에서 다른 길로 탐색을 하는 과정을 반복하기 때문에 스택을 사용
- 한바퀴를 순회하는 구조의 경우 방문한 곳을 표기하기 위한 visited 사용 필요

``` python

def dfs(v, N):
    visited = [0] * (N+1)
    stack = []

    while True:
        if visited[v] == 0:
            visited[v] = 1
            print(v)
        for w in adj_list[v]:
            if visited[w] == 0:
                stack.append(v)
                v = w
                break
        else:
            if stack:
                v = stack.pop()
            else:
                break


V, E = map(int, input().split())
graph = list(map(int, input().split()))
adj_list = [[] for _ in range(V+1)]

for i in range(E):
    v, w = graph[i*2], graph[i*2+1]

    adj_list[v].append(w)
    adj_list[w].append(v)


후위 표기법 변환과정
1. 피연산자면 append
2. ')'면 '('가 올 때까지 스택에서 pop
3. 연산자일 때
- 스택이 비어있을 경우 무조건 push
- 스택의 peek보다 우선순위가 높으면 push
- 스택의 peek보다 우선순위가 낮으면 스택의 peek가 우선순위가 더 낮아질 때까지 pop을 진행한 후에 push
4. 스택이 비어있지 않다면 전부 pop


백트래킹
해당 방향의 검색 결과가 의미없을 경우 되돌아가서 최적화하는 기법


순열
```
def backtrack(a, k, n):
    c = [0] * MAXCANDIDATES

    if k == n:
        for i in range(0, k):
            print(a[i], end=" ")
        print()
    else:
        ncandidates = construct_candidates(a, k, n, c)
        for i in range(ncandidates):
            a[k] = c[i]
            backtrack(a, k + 1, n)

def construct_candidates(a, k, n, c):
    in_perm = [False] * (NMAX + 1)

    for i in range(k):
        in_perm[a[i]] = True

    ncandidates = 0
    for i in range(1, NMAX + 1):
        if in_perm[i] == False:
            c[ncandidates] = i
            ncandidates += 1
    return ncandidates

MAXCANDIDATES = 3
NMAX = 3
a = [0]*NMAX
backtrack(a, 0, 3)
```

아래는 내가 생각한 코드

```
def backtrack(arr, visited, depth, new_arr)
    if depth == N:
        for i in range(depth):
            print(arr[i], end=" ")
        print()
    else:
        for i in range(len(arr)):
            if not visited[i]:
                new_arr[depth] = arr[i]
                visited[i] = 1
                backtrack(arr, visited, depth, new_arr)
                visited[i] = 0
            else:
                continue


---
---

Queue
|연산|기능|
|:---:|:---|
|enQueue(item)|큐의 뒤쪽에 원소를 삽입하는 연산|
|deQueue()|큐의 앞쪽에서 원소를 삭제하고 반환하는 연산|
|createQueue()|공백 상태의 큐를 생성하는 연산|
|isEmpty()|큐가 공백상태인지를 확인하는 연산|
|isFull()|큐가 포화상태인지를 확인하는 연산|
|Qpeek()|큐의 앞쪽(front)에서 원소를 삭제 없이 반환하는 연산|


선형큐
```
class Queue:
    front = -1
    rear = -1

    def __init__(self):
        self.size = 100
        self.items = [None]*self.size
        self.rear = -1
        self.front = -1

    def enqueue(self, data):
        self.rear += 1
        self.items[self.rear] = data

    def dequeue(self):
        self.front += 1
        data = self.items[self.front]
        self.items[self.front] = 0
        return data

    def is_empty(self):
        return self.rear == self.front

    def peek(self):
        return self.items[self.front+1]
```
문제점 : 점점 뒤로 가기 때문에 앞에 있는 빈 공간을 활용할 수가 없다.


원형 큐
```
class CircularQueue:
    front = -1
    rear = -1

    def __init__(self):
        self.size = 100
        self.items = [None]*self.size
        self.rear = -1
        self.front = -1

    def enqueue(self, data):
        self.rear = (self.rear + 1) % self.size
        self.items[self.rear] = data

    def dequeue(self):
        if self.is_empty():
            print('Queue가 empty라 불가능')
        self.front = (self.front + 1) % self.size
        data = self.items[self.front]
        self.items[self.front] = 0
        return data

    def is_empty(self):
        return self.rear == self.front

    def peek(self):
        return self.items[self.front+1]

    def is_full(self):
        return (self.rear + 1) % self.size == self.front
```

deque(덱)
- 양쪽 끝에서 빠르게 추가와 삭제를 할 수 있는 리스트류 컨테이너
연산
- append(x) : 오른쪽에 x 추가
- popleft() : 왼쪽에서 요소를 제거하고 반환. 요소가 없으면 IndexError


Priority Queue
우선순위대로 나가는 큐

버퍼
- 데이터를 한 곳에서 다른 한 곳으로 전송하는 동안 일시적으로 그 데이터를 보관하는 메모리의 영역
- 버퍼링 : 버퍼를 활용하는 방식 또는 버퍼를 채우는 동작을 의미한다.

버퍼의 자료 구조
- 버퍼는 일반적으로 입출력 및 네트워크와 관련된 기능에서 이용된다.
- 순서대로 입력/출력/전달되어야 하므로 FIFO 방식의 자료구조인 큐가 활용된다.


---
---

BFS