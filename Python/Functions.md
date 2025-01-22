# Functions <br>

## 개요 <br>
함수를 사용하는 이유 : **재사용성, 가독성, 유지보수성 향상** <br>

### 함수 구조 <br>
``` python
def make_sum(param1, param2):
    """이것은 두 수를 받아
    두 수의 합을 반환하는 함수입니다.
    >>> make_sum(1,2)_
    3
    """
    return param1 + param2
 ```
**Docstring** : 따옴표 3개로 시작하는 <u>함수에 대한 설명서</u> <br>
함수 정의는 def 키워드로 시작 <br>
def 키워드 이후 함수 이름 작성 <br>
함수 body : 콜론 다음에 들여쓰기 된 코드 블럭 <br>
함수 반환 값 : return 키워드 이후에 반환할 값을 명시, return문이 없다면 <u>None</u>이 반환 <br>

### 매개변수와 인자 <br>
매개변수(parameter) : 함수를 정의할 때, 함수가 받을 값을 나타내는 변수 <br>
인자(argument) : 함수를 호출할 때, 실제로 전달되는 값 <br>

### 다양한 인자 종류 <br>
1. 위치 인자(Positional Arguments) <br>
함수 호출 시 인자의 위치에 따라 전달되는 인자 <br>
위치인자는 함수 호출 시 반드시 값을 전달해야 함 <br>

2. 기본 인자 값(Default Argument Values) <br>
함수 정의에서 매개변수에 기본 값을 할당하는 것 <br>
함수 호출 시 인자를 전달하지 않으면, 기본값이 매개변수에 할당됨 <br>

3. 키워드 인자(Keyword Arguments)  <br>
함수 호출 시 인자의 이름과 함께 값을 전달하는 인자 <br>
매개변수와 인자를 일치시키지 않고, 특정 매개변수에 값을 할당할 수 있음 <br>
인자의 순서는 중요하지 않으며, 인자의 이름을 명시하여 전달 <br>
단, 호출 시 키워드 인자는 위치 인자 뒤에 위치해야 함 <br>

4. 임의의 인자 목록(Arbitrary Argument Lists)  <br>
정해지지 않은 개수의 인자를 처리하는 인자 <br>
함수 정의 시 매개변수 앞에 '\*'를 붙여 사용 <br>
여러 개의 인자를 tuple로 처리 <br>

5. 임의의 키워드 인자 목록(Arbitrary Keyword Argument Lists) <br>
정해지지 않은 개수의 키워드 인자를 처리하는 인자 <br>
함수 정의 시 매개변수 앞에 '\*\*'를 붙여 사용 <br>
여러 개의 인자를 dictionary로 묶어 처리 <br>

### 함수 인자 권장 작성순서 <br>
위치 -> 기본 -> 가변 -> 가변 키워드 <br>
호출 시 인자를 전달하는 과정에서 혼란을 줄일 수 있도록 함 <br>
단, 모든 상황에 적용되는 절대적인 규치근 아니며, 상황에 따라 유연하게 조정될 수 있음 <br>

---
---
---

### 재귀 함수 <br>
특정 알고리즘 식을 표현할 때 변수의 사용이 줄어들며, <u>코드의 가독성</u>이 높아짐 <br>
수학적 문제 해결, 코드 간결, 문제의 자연스러운 표현 <br>

### 내장 함수 <br>
파이썬이 기본적으로 제공하는 함수 <br>
map(function, iterable) : 순회 가능한 데이터구조의 모든 요소에 함수를 적용하고, 결과를 map object로 반환 <br>
``` python
list(map(int, input().split()))  # 입력된 값을 공백 단위로 분리한 후, 각각에 int 적용
```
zip(\*iterables) : 임의의 iterable을 모아 튜플을 원소로 하는 zip object를 반환 <br>
활용 : 여러 개의 리스트를 동시에 조회할 때(각각의 i번째 데이터 묶음) <br>
**예외** : pair가 맞지 않으면 저장되지 않는다(pair가 된 부분만 반환) <br>

### 함수와 Scope
Python의 범위(scope) : 함수는 코드 내부에 local scope를 생성하며, 그 외의 공간인 global scope로 구분 <br>
범위와 변수 관계
- global scope : 코드 어디에서든 참조할 수 있는 공간 <br>
- local scope : 함수가 만든 scope (함수 내부에서만 참조 가능) <br>
- global variable : global scope에 정의된 변수 <br>
- local variable : local scope에 정의된 변수 <br>

Scope 예시 <br>
``` python
def_func():
    num = 20
    print('local', num)  # 20

func()

print('global', num)  # NameError
```
변수 수명주기(lifecycle) <br>
변수의 수명 주기는 변수가 선언되는 위치와 scope에 따라 결정됨 <br>
1. built-in scope <br>
    파이썬이 실행된 이후부터 영원히 유지 <br>
2. global scope <br>
    모듈이 호출된 시점 이후 혹은 인터프리터가 끝날 때까지 유지 <br>
3. local scope <br>
    함수가 호출될 때 생성되고, 함수가 종료될 때까지 유지 <br>

이름 검색 규칙(Name Resolution) <br>
파이썬에서 사용되는 이름들은 특정한 이름공간에 저장되어 있음 <br>
아래와 같은 순서로 이름을 찾아 나가며, LEGB Rule이라고 부름 <br>
1. Local scope : 지역 범위(현재 작업 중인 범위) <br>
2. Enclose scope : 지역 범위 한 단계 위 범위 <br>
3. Global scope : 최상단에 위치한 범위 <br>
4. Built-in scope : 모든 것을 담고 있는 범위(정의하지 않고 사용할 수 있는 모든 것) <br>
함수 내에서는 바깥 Scope의 변수에 접근 가능하나 수정은 할 수 없음 <br>

LEGB Rule 예시 <br>

``` python
print(sum)  # <built-in function sum>
print(sum(range(3)))  # 3

sum = 5

print(sum)  # 5
print(sum(range(3)))  # TypeError
```
sum이라는 이름을 global scope에서 사용하게 되면서 built-in scope에 있던 내장함수 sum을 사용하지 못하게 됨 <br>
sum을 참조 시 LEGB Rule에 따라 global에서 먼저 찾기 때문 <br>

'global' 키워드 <br>
변수의 scope를 전역 범위로 지정하기 위해 사용 <br>
일반적으로 함수 내에서 전역 변수를 수정하려는 경우에 사용 <br>
global 키워드 사용 전 참조 불가 <br>
매개변수에는 global 키워드 사용 불가 <br>

---
---
---

## 함수 스타일 가이드 <br>
### 함수 이름 작성 규칙 <br>
기본 규칙 <br>
- 소문자와 언더스코어 사용 <br>
- 동사로 시작하여 함수의 동작 설명 <br>
- 약어 사용 지망 <br>

함수 이름 구성 요소 <br>
- 동사 + 명사 <br>
- 동사 + 형용사 + 명사 <br>
- get/set 접두사 <br>

**단일 책임 원칙** <br>
: <u>하나의 함수는 하나의 책임만 가져야 한다.</u> - 여러 개의 기능이 필요할 때는 단일 함수들을 실행시키는 함수를 만들어서 사용

---
---
---

## Packing & UnPacking <br>
### Packing <br>
여러 개의 값을 하나의 변수에 묶어서 담는 것 <br>
'\*'을 활용한 패킹 (변수 할당 시) <br>
'\*'을 사용하면 "나머지 모든 값"을 묶어서 할당 가능 <br>

``` python
numbers = [1, 2, 3, 4, 5]
a, *b, c = numbers

print(a)  # 1
print(b)  # [2, 3, 4]
print(c)  # 5
```

### Unpacking <br>
튜플이나 리스트 등의 객체의 요소들을 개별 변수에 할당 <br>
'\*'을 활용한 언패킹 (함수 인자 전달) <br>
- 시퀀스(리스트, 튜플 등)를 함수에 전달할 때, 각 요소를 풀어서 개별 인자로 넘겨줄 수 있음 <br>

패킹 연산자 정리 <br>
'\*' <br>
- 패킹 연산자로 사용될 때, 여러 개의 인자를 하나의 리스트나 튜플로 묶음 <br>
- 언패킹 연산자로 사용될 때, 시퀀스나 반복 가능한 객체를 각각의 요소 언패킹하여 함수의 인자로 전달 <br>

'\*\*' <br>
- 언패킹 연산자로 사용될 때, 딕셔너리의 키-값 쌍을 개별 키워드 인자로 전달 <br>

## Lambda 표현식  <br>
람다 표현식 구조  <br>


``` python
lambda 매개변수: 표현식
```

함수를 1회성으로 사용할 때, 함수를 매개변수로 전달할 때 활용 <br>