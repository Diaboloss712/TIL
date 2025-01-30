# Java-Basic <br>

1. String str1 = "Hello";
2. String str2 = new String("Hello");

1번의 경우 문자열 풀의 주소를 가져옴
2번의 경우 Heap 메모리에 저장해서 새로운 주소에 값을 저장

Text Block: multi line 가능
``` Java
String str = """"
내 이름은 %s.
나이는 %d살이고, 사는 곳은 %s.
""".formatted("hong gil dong", 20, "율도국");

포멧 문자 형식: %[flags][width][.precision]conversion

참조형과 객체형
참조형
- 모두 소문자로 시작
- 비객체 타입으로 null 불가
- 변수의 선언과 동시에 메모리 생성
- 모든 값 타입은 메모리 스택에 저장
- 저장공간에 실제 자료 값을 가짐

객체형
- 자료가 저장된 공간의 주소를 저장
- 메모리의 힙에 실제 값을 저장, 그 참조값을 갖는 변수는 스택에 저장
