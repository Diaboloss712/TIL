# Operation - 연산자 <br> 

## 비교 연산자 <br> 

### == 비교 연산자 <br>
값이 같은지를 비교, 동등성 <br>

### is 비교 연산자 <br> 
객체 자체가 같은지를 비교, 식별성 <br> 
같은 메모리 주소를 가리켜야 통과됨 <br>
print(1 is True) # False <br>
print(2 is 2.0) # False <br>

is 대신 ==를 사용해야 하는 이유 <br> 
일반적으로 객체보다는 값을 비교하는 경우가 많음 <br> 
is 연산자를 이용하면 의도치 않은 결과가 나옴 <br> 

is 연산자는 언제 사용하는가? <br> 
None을 비교를 비교 할 때 <br>
- "같은 주소에 있는가?"라는 질문을 답해야 할 때 <br>
싱클턴 객체를 비교 할 때 <br> 
싱클턴 객체 : 프로그램 전체에서 오직 1개만 존재하도록 만들어진 특별한 객체 <br> 

==와 is 정리 <br>

### 논리 연산자 <br> 
|기호|연산자|내용|
|:--:|:--:|:--:|
| and | 논리곱 | 두 연산자가 True -> True |
| or | 논리합 | 하나라도 True -> True |
| not | 논리부정 | 단일 피연산자를 부정 |

### 단축평가 - 논리 연산에서 두번째 연산까지 하지 않고 결과 도출 <br> 
True일때 뒤의 값을 반환한다. <br>
ex) print(('a' and 'b') in 'aeiou') # False <br>
ex) print(('b' and 'a') in 'aeiou') # True <br>
'b' and 'a' -> 'a'(뒤의 값), 'a' in 'aeiou' -> True <br>

### 시퀀스형 연산자 <br>

### Trailing Comma <br> 
컬렉션의 마지막 요소 뒤에 붙는 쉼표 <br>
일반적으로 작성은 '선택사항' <br>
단, 하나의 요소로 구성된 튜플을 만들 때는 필수(튜플은 쉼표가 본체) <br>

### Trailing Comma 기본 규칙 <br>
각 요소를 별도의 줄에 작성 <br>
마지막 요소 뒤에 trailing comma 추가 <br>
닫는 괄호는 새로운 줄에 배치 <br>

