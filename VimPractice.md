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

num+x : 커서 위치에서 num개의 글자 제거

x,d : 삭제, p로 붙여넣기

G : 맨 아래 이동

gg : 맨 위 이동

Ctrl+b : Page Up

Ctrl+f : Page Down

;set number : 라인번호 표기

라인번호 + Shift + g : 해당 라인으로 이동

q(key) : 해당되는 key 값으로 녹화

@(key) : 해당되는 key 실행

@@ : 최근 매크로 실행

m(key) : 북마크 지정

`(key) : 해당 key로 이동

`` : 이전 라인으로 이동

ctrl-q : 비주얼 블록모드

행간 이동 : O, $

행에서 공백을 제외한 맨 앞 문자로 이동 : ^

행에서 해당 문자로 이동 : f + 문자

행에서 해당 문자 앞으로 이동 : t + 문자

한 줄씩 아래로 스크롤 : Ctrl + e

한 줄씩 위로 스크롤 : Ctrl + y

반 페이지 아래로 스크롤 : Ctrl + d

반 페이지 위로 스크롤 : Ctrl + u

페이지 맨 위로 이동 : gg

여러 줄 동일한 문자열 넣기

반복되는 문자열을 삽입하는 위치에서 ctrl+v

shift+i 후 원하는 문자열 입력

검색 : /{word}

- 다음 검색 : n

- 이전 검색 : shift + n

문자열 바꾸기 : (시작줄),(끝줄)s/찾을패턴/바꿀문자열/옵션
