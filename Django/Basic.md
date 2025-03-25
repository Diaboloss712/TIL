# 장고 설치 과정

1. 파이썬 가상환경 설치
    - python -m venv venv
2. 장고 설치
    - django-admin startproject pjt_name
3. 서버 실행
    - python manage.py run server
4. git 설정
5. 앱 생성
    - python manage.py startapp articles
6. setting.py에 앱 연결
    - INSTALLED APPS에 'articles' 추가
7. articles에 templates 생성
    - templates는 MVC로 가정하면 View, 즉 사용자에게 보이는 페이지를 모은 곳
    - templates에서 페이지 파일을 만들고 urls에서 연결하면 해당 페이지를 반환
8. urls에서 페이지와 주소 연결
9. 필요한 설치 리스트 기록
    - pip freeze > requirements.txt
    - 자동 갱신이 안 되기 때문에 설치파일을 추가할 때마다 해줘야한다.

url -> view -> templates


## Template System

1. Variable
    - render 함수의 세번째 인자로 딕셔너리 데이터를 사용
    - 딕셔너리 key에 해당하는 문자열이 template에서 사용 가능한 변수명이 됨
    - dot('.')를 사용하여 변수 속성에 접근할 수 있음
2. Filters
    - 표시할 변수를 수정할 때 사용 (변수 + '|' + 필터)
    - chained이 가능하며 일부 필터는 인자를 받기도 함
    - 약 60개의 built-in template filters를 제공
    - {{variable|filter}}
    - {{name|truncatewords:30}}
3. Tags
    - 반복 또는 논리를 수행하여 제어 흐름을 만듦
    - 일부 태그는 시작과 종료 태그가 필요
    - 약 24개의 built-in template tags를 제공
    - {% tag %}
    - {% if %} {% endif %}
4. Comments
    - DTL에서의 주석


