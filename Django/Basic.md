# Django 튜토리얼: 설치부터 Templates까지

## 1. 장고 설치 과정

1. 파이썬 가상환경 설치  
   - 명령어: 
     python -m venv venv

2. 장고 프로젝트 생성  
   - 명령어: 
     django-admin startproject pjt_name

3. 서버 실행  
   - 명령어: 
     python manage.py runserver

4. git 설정 (git init, gitignore 생성)

5. 앱 생성  
   - 명령어: 
     python manage.py startapp articles

6. 앱 연결  
   - settings.py 파일의 INSTALLED_APPS에 'articles' 추가

7. Templates 폴더 생성 (View 역할)  
   - articles 앱 내부 또는 별도 위치에 templates 폴더를 생성  
   - 이 폴더는 MVC 관점에서 View, 즉 사용자에게 보여지는 페이지들을 모아놓은 곳이다.  
   - 템플릿 파일을 생성한 후, URL과 연결하면 해당 페이지가 반환된다.

8. URL과 View 연결  
   - URL 패턴을 정의하여 템플릿을 반환하는 View와 연결

9. 필요한 패키지 목록 기록  
   - 명령어: 
     pip freeze > requirements.txt  
   - 주의: 설치 파일이 추가될 때마다 수동으로 갱신해야 한다.


url -> view -> templates 순서로 요청이 처리된다.

---

## 2. Django의 MTV 아키텍처

Django의 아키텍처는 MVC 패턴과 유사한데, Django에서는 이를 MTV (Model-Templates-View) 패턴이라고 부른다.

- Model  
  - 데이터 구조를 정의하고 데이터베이스를 관리한다.
- Template  
  - HTML 파일 등 사용자 인터페이스의 구조와 레이아웃을 정의한다.
- View  
  - HTTP 요청을 받아 처리한 후, 적절한 응답을 반환한다.  
  - 데이터는 Model을 통해 가져오고, Template에 전달하여 최종 응답을 생성한다.

---

## 3. Template System

Django 템플릿 시스템은 웹 페이지의 동적 생성에 필요한 여러 기능을 제공한다.

### 3.1. Variable
- render 함수의 세 번째 인자로 전달된 딕셔너리의 key가 템플릿에서 사용 가능한 변수명이 된다.
- 변수는 {{ variable }}와 같이 표시하며, .을 사용해 변수의 속성에 접근할 수 있다.

### 3.2. Filters
- 변수의 출력을 수정할 때 사용한다.
- 구문:  
  {{ variable | filter }}
- 여러 필터를 체인 형태로 사용할 수 있으며, 일부 필터는 인자를 받기도 한다.
- 예시:  
  {{ name | truncatewords:30 }}
- Django는 약 60개의 내장(built-in) 템플릿 필터를 제공한다.

### 3.3. Tags
- 조건문, 반복문 등 제어 흐름을 구성하는 데 사용된다.
- 구문:  
  {% tag %} ... {% endtag %}
- 예시:  
  {% if condition %}
      <!-- 내용 -->
  {% endif %}
- Django는 약 24개의 내장 템플릿 태그를 제공한다.

### 3.4. Comments
- 템플릿 내에서 주석을 작성할 수 있다.
- 구문:  
  {# 이 부분은 주석 처리됩니다. #}

---

## 4. Form의 역할

HTML Form은 사용자가 데이터를 입력하고 서버로 전송할 수 있게 해준다.

```
<!-- /test.html -->
<form action="/receiver" method="GET">
    <input type="text" name="query" id="message">
    <input type="submit" value="submit">
</form>
```

- 위 코드는 /test 페이지에 있다고 가정한다.
- 사용자가 입력창에 test라는 텍스트를 입력하고 submit 버튼을 누르면, query=test라는 Query String Parameter가 생성되어 서버에 전송된다.
- GET 방식은 입력값을 URL 파라미터에 그대로 노출시키므로, 보안이 필요한 데이터 전송에는 적합하지 않다.
- 최종 URL 예시: /receiver?query=test

### 서버에서 파라미터 추출 (Django 예시)

``` python
def receive(request):
    query = request.GET.get('query')
    context = {
        'text': query,
    }
    return render(request, 'receiver.html', context)
```

- 위 코드에서 request.GET.get('query')를 통해 URL 파라미터로 전달된 값을 추출한다.
- 추출된 값을 템플릿에 전달하여 화면에 표시할 수 있다.

---

## 5. Django URLs

Django 프로젝트를 생성하면 기본적으로 urls.py 파일이 생성된다. 앱을 추가할수록 URL 패턴이 늘어나는데, 이를 효율적으로 관리하는 방법을 알아보자.

### 5.1. 개별 URL 작성의 문제

예를 들어, 다음과 같이 여러 URL 패턴을 작성하면 관리가 복잡해진다.

urlpatterns = [
    path('app1/board/', views.board),
    path('app2/board/', views.board),
    path('app1/board/write/', views.write),
    path('app2/board/write/', views.write),
    path('app1/board/1/', views.detail),
    path('app2/board/1/', views.detail),
    path('app1/board/2/', views.detail),
    path('app2/board/2/', views.detail),
]

### 5.2. Variable Routing

- URL 내의 변수를 사용하여 공통된 패턴을 하나로 처리할 수 있다.
- 예시:

```
urlpatterns = [
    path('app1/board/<int:num>/', views.detail),
]
```

- 이 방식은 Variable Routing이라 하며, URL 경로의 변수에 따라 동적으로 처리가 가능하다.

### 5.3. App URL Mapping

- 프로젝트의 urls.py에서 각 앱별 URL 패턴을 분리하여 관리할 수 있다.
- 예시:

``` python
# pjt/urls.py
from django.urls import path, include

urlpatterns = [
    path('app1/', include('app1.urls')),
    path('app2/', include('app2.urls')),
]
```

``` python
# app1/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.board),
    path('board/<int:num>/', views.detail),
    path('board/write/', views.write),
]
```

``` python
# app2/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.board),
    path('board/<int:num>/', views.detail),
    path('board/write/', views.write),
]
```

- include() 함수는 URL의 공통 부분을 잘라내고, 나머지 부분을 각 앱의 URL 패턴으로 전달한다.
- 이를 App URL Mapping이라고 한다.

---

## 6. Naming URL Patterns

URL 패턴에 이름을 부여하면, 템플릿에서 URL을 직접 입력하지 않고도 해당 이름을 통해 URL을 참조할 수 있다.
이름을 지정하면 URL이 변경되더라도 템플릿의 수정을 최소화할 수 있다.

### 6.1. 이름 지정 방법

```
# app2/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.board, name='board'),
    path('board/<int:num>/', views.detail, name='detail_board'),
    path('board/write/', views.write, name='write'),
]
```

### 6.2. 템플릿에서 URL 이름 사용

```
<!-- app2/board.html -->
{% block content %}
    <a href="{% url 'write' %}">글쓰기</a>
    <a href="{% url 'detail_board' %}">1번 게시물</a>
{% endblock content %}
```

- 위와 같이 URL 이름을 사용하면, 주소를 직접 입력할 필요 없이 해당 이름에 맞는 URL로 자동 연결된다.

### 6.3. 앱별 이름 설정 (Namespace)

- 여러 앱에서 같은 이름을 사용할 경우 이름이 중복될 수 있다.
- 이를 해결하기 위해 각 앱에 이름공간(namespace)을 지정할 수 있다.

```
# app2/urls.py
from django.urls import path
from . import views

app_name = 'review'
urlpatterns = [
    path('board/', views.board, name='board'),
    path('board/<int:num>/', views.detail, name='detail_board'),
    path('board/write/', views.write, name='write'),
]
```

```
<!-- app2/board.html -->
{% block content %}
    <a href="{% url 'review:write' %}">글쓰기</a>
    <a href="{% url 'review:detail_board' num=1 %}">1번 게시물</a>
{% endblock content %}
```
---