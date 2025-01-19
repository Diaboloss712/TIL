# Python의 자료형 <br>
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
'''
a = "python"
a * 2
'pythonpython'
'''

### 문자열 인덱싱 <br>
'''
a = "Life is too short, You need Python"
a[-1] = 'n'
a[-2] = 'o'
a[-0] = a[0] = 'L'
'''

### 문자열 슬라이싱 <br>
'''
a[0:5] = a[0]+a[1]+a[2]+a[3]+a[4] = 'Life '
'''
시작 번호나 끝 번호를 생략시 생략한 방향의 끝까지 출력 <br>
a[19:-7] = a[19:-8] = 'You need' <br>

### 문자열 포매팅 <br>
'''
number = 815
day = "five"
"I ate %d apples. so I was sick for %s days." % (number, day)
'I ate 815 apples. so I was sick for five days.'
'''

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
'''
text = '이건 어떻게'
num = 15
f'내가 다음으로 말하고 싶은 것은 {text} 해야 할지다. {num} 번 생각했다'
'''

### 리스트 자료형 <br>
생성 예시 : a = list(), a = [] <br>
list 추가 : a.append([5,6]) <br>
리스트 정렬 : sort, 리스트 뒤집기 : reverse <br>
요소 꺼내기 : pop, 특정 값 세기 : count <br>

### 튜플 자료형 <br>
튜플은 리스트와 다르게 소괄호로 생성, 변수가 아닌 상수 사용 <br>
즉 요솟값을 변경하거나 삭제가 불가능, 그 외에는 동일 <br>

### 딕셔너리 자료형 <br>
Key, Value 쌍을 가진 형태 <br>

'''
dic = { 'name' : 'dia', 'num' : '10', 'study' = 'python'}
'''

### 딕셔너리 관련 함수 <br>
keys : 딕셔너리의 Key만을 모아 dict_keys 객체를 리턴 <br>
values : keys와 유사하게 dict_values 객체를 리턴 <br>
items : Key, Value 쌍을 튜플로 묶은 값을 리턴 <br>
in : Key가 존재하는지 확인(True, False) <br>
