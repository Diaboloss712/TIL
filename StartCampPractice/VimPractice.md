# VIM 사용법 <br>
## 이동<br>
hjkl 왼위아우 <br>

줄 삭제 : dd <br>
줄 단위 이동 : cc <br>
Undo : u
Redo : Ctrl-R
o : 새 줄 생성 및 삽입모드
O : 새 줄 생성을 바로 윗줄에서
ZZ : 파일 쓰기
qq : 변경된 모든것 버리기
cw : 현재 커서 위치부터 단어끝까지 잘라내기
r : 글자 단위로 변경
v : 비주얼 모드, 드래그
CTRL-V : 테이블에서 블록 단위로 행동 가능
x,d : 삭제, p로 붙여넣기
G : 맨 아래 이동
gg : 맨 위 이동
Ctrl+b : Page Up
Ctrl+f : Page Down
;set number : 라인번호 표기
라인번호 + Shift + g : 해당 라인으로 이동
testestest is gold











testtest## 숫자형 <br>
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

```
a = "python"
a * 2
'pythonpython'
```

### 문자열 인덱싱 <br>
```
a = "Life is too short, You need Python"
a[-1] = 'n'
a[-2] = 'o'
a[-0] = a[0] = 'L'
```

### 문자열 슬라이싱 <br>
```
a[0:5] = a[0]+a[1]+a[2]+a[3]+a[4] = 'Life '
```
시작 번호나 끝 번호를 생략시 생략한 방향의 끝까지 출력 <br>
a[19:-7] = a[19:-8] = 'You need' <br>

### 문자열 포매팅 <br>
```
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

### f문자열 포매팅 <br>
```

### 리스트 자료형 <br>
생성 예시 : a = list(), a = [] <br>
list 추가 : a.append([5,6]) <br>
리스트 정렬 : sort, 리스트 뒤집기 : reverse <br>

### 튜플 자료형 <br> 튜플은 리스트와 다르게 소괄호로 생성, 변수가 아닌 상수 사용 <br>
### 튜플 자료형 <br> 튜플은 리스트와 다르게 소괄호로 생성, 변수가 아닌 상수 사용 <br>

요소 꺼내기 : pop, lk특정 값 세기 : count <br>


### 딕셔너리 자료형 <br>
Key, Value 쌍을 가진 형태 <br>

```
dic = { 'name' : 'dia', 'num' : '10', 'study' = 'python'}
```

### 딕셔너리 관련 함수 <br>
keys : 딕셔너리의 Key만을 모아 dict_keys 객체를 리턴 <br>
