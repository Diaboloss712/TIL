# DataType <br>

## 숫자형 <br>
| 항목 | 파이썬 사용 예 |
| :---- | :----- |
| 정수 | 123, -345, 0 |
| 실수 | 123.45, -43.21, 3.14e15|
| 8진수 | 0o65, 0o12 |
| 16진수 | 0x2A, 0xFF |


### 실수형 예시 <br>
a = 4.24E10  -> 4.24 * 10^10 <br>
a = 4.24e-10 -> 4.24 * 10^-10 <br>

### 8진수, 16진수 <br>
8진수는 숫자가 0o 또는 0O로 시작 <br>
a = 0o177 -> 1*8^2+7*8^1+7 = 127 <br>
16진수는 0x로 시작 <br>
a = 0xABC -> 10*16^2+11*16^1+12 = 2748 <br>

### **연산자 <br>
a = 3, b = 4, a ** 4 = a^b = 81 <br>

## 시퀀스 자료형 <br>

### 문자열 자료형 <br>
문자열은 4가지 방법으로 만들어진다. <br>
1. "Hello" <br>
2. 'Hello' <br>
3. """Hello""" <br>
4. '''Hello''' <br>

### 문자열 내에 큰따옴표나 작은따옴표를 넣고 싶을때의 방법 <br>
1. "Today's lunch is noodle" - 큰따옴표 안에 작은따옴표 <br>
2. '"I love chicken"' - 작은따옴표 안에 큰따옴표 <br>
3. food = 'Python\'s favorite food is pizza' - 역슬래시 다음 문자를 이스케이프 처리 <br>

### 여러줄인 문자열을 변수에 대입 <br>
Life is long enough <br>
You need Programming Skills <br>

    vn='''
    Life is lone enough <br>
    You need Programming skills <br>

### 문자열 곱하기 <br>
``` python
a = "python"
a * 2
'pythonpython'
```

### **문자열 인덱싱** <br>
``` python
a = "Life is too short, You need Python"
a[-1] = 'n'
a[-2] = 'o'
a[-0] = a[0] = 'L'
```

### **문자열 슬라이싱** <br>
``` python
a[0:5] = a[0]+a[1]+a[2]+a[3]+a[4] = 'Life '
```
시작 번호나 끝 번호를 생략시 생략한 방향의 끝까지 출력 <br>
a[19:-7] = a[19:-8] = 'You need' <br>

### 문자열 포매팅 <br>
``` python
number = 815
day = "five"
"I ate %d apples. so I was sick for %s days." % (number, day)
'I ate 815 apples. so I was sick for five days.'
```

### 문자열 포맷 코드 <br>
| 코드 | 설명 |
| :--: | :-- |
|%s | 문자열(String) |
|%c | 문자 1개(Character) |
|%d | 정수(Integer) |
|%f | 부동소수(floating-point) |
|%o | 8진수 |
|%x | 16진수 |
|%% | Literal %(문자 % 자체)

### **f문자열 포매팅** <br>
``` python
text = '이건 어떻게'
num = 15
print(f'내가 다음으로 말하고 싶은 것은 {text} 해야 할지다. {num} 번 생각했다')
```

---
---
***
### 리스트 자료형 <br>
생성 예시 : a = list(), a = [] <br>
데이터 타입 : 모든 자료형 저장 가능 <br>
list 추가 : a.append([5,6]) <br>
리스트 정렬 : sort, 리스트 뒤집기 : reverse <br>
요소 꺼내기 : pop, 특정 값 세기 : count <br>

### 튜플 자료형 - <u>쉼표가 본체</u>  <br>
튜플은 리스트와 다르게 소괄호로 생성, 변수가 아닌 상수 사용 <br>
즉 요솟값을 변경하거나 삭제가 불가능, 그 외에는 동일 <br>
단일 요소 튜플을 만들 때는 반드시 후행 쉼표가 필요 <br>
ex) my_tuple_2 = (1,) -> <u>쉼표</u>가 없으면 기본 자료형이 됨) <br>
tuple은 내부 동작과 안전한 데이터 전달에 사용 <br> 
ex) 다중 할당, 값 교환, 그룹화, 함수 다중 반환 값 등 <br>

### range <br>
range(시작 값, 끝 값, 증가 값) - 정수 시컨스 생성<br>
증가 값이 0이면 에러 <br>
값의 범위 규칙 <br>
1. 음수 증가 시 : 시작 값이 끝값보다 커야 함
2. 양수 증가 시 : 시작 값이 끝 값보다 작아야 함

---
---
---
## 비시퀀스 자료형 <br>

### **딕셔너리 자료형** <br>
<u>Key</u>, <u>Value</u> 쌍을 가진 형태 <br>

```
dic = { 'name' : 'dia', 'num' : '10', 'study' = 'python'}
```

추가 방법 <br>
ex) dic[key값] = value값 <br>

### 딕셔너리 관련 함수 <br>
keys : 딕셔너리의 Key만을 모아 dict_keys 객체를 리턴 <br>
values : keys와 유사하게 dict_values 객체를 리턴 <br>
items : Key, Value 쌍을 튜플로 묶은 값을 리턴 <br>
in : Key가 존재하는지 확인(True, False) <br>

### set - 순서와 중복이 없는 변경 가능한 자료형 <br>
수학에서의 집합과 동일한 연산 처리 기능, 중괄호로 표기
my_set_1 = {1,2,3} -> 1,2,3 <br>
my_set_2 = {1,1,1} -> 1 <br>

### None - 파이썬에서 '값이 없음'을 표현하는 자료형<br> 

### Boolean - 참과 거짓을 표현하는 자료형<br> 
bool_1 = True, bool_2 = False - 대문자 유의<br> 
비교 / 논리 연산의 평가 결과로 사용, 조건 / 반복문과 함께 사용<br>

### Collection - 여러 개의 항목 또는 요소를 담는 자료 구조<br> 
| 컬렉션 | 변경 가능 여부 | 순서 여부 |
| :--: | :--: | :--: |
| str | X | O |
| list | O | O |
| tuple | X | O |
| dict | O | X |
| set | O | X |