# Django 튜토리얼: 설치부터 Templates까지지

## 장고 설치 과정

1. 파이썬 가상환경 설치
    - python -m venv venv
2. 장고 설치
    - django-admin startproject pjt_name
3. 서버 실행
    - python manage.py runserver
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

---

## Django의 MTV 아키텍처

Django의 MVT패턴은 MVC 패턴과 개념적으로 유사하다.
MVC = Model-View-Controller
1. Model : 데이터와 비즈니스 로직을 관리한다.
2. View : 레이아웃과 화면을 처리한다.
3. Controller : 모델과 뷰로 명령을 전달한다.

MTV = Model-Templates-View
- Model: 데이터 구조를 정의하고 DB를 관리한다.
- Template: HTML 파일 등 사용자 인터페이스의 구조와 레이아웃을 정의한다.
- View: HTTP 요청 수신 및 반환하는 요청 처리 함수. Model을 통해 데이터에 접근하고, Template에게 응답의 서식 설정 맡긴다.

---

## Template System

1. Variable
    - render 함수의 세번째 인자로 딕셔너리 데이터를 사용한다.
    - 딕셔너리 key에 해당하는 문자열이 template에서 사용 가능한 변수명이 된다.
    - dot('.')를 사용하여 변수 속성에 접근할 수 있다.
2. Filters
    - 표시할 변수를 수정할 때 사용 (변수 + '|' + 필터)
    - chained이 가능하며 일부 필터는 인자를 받기도 한다.
    - 약 60개의 built-in template filters를 제공한다.
    - {{variable|filter}}
    - {{name|truncatewords:30}}
3. Tags
    - 반복 또는 논리를 수행하여 제어 흐름을 만든다.
    - 일부 태그는 시작과 종료 태그가 필요하다.
    - 약 24개의 built-in template tags를 제공한다.
    - {% tag %}
    - {% if %} {% endif %}
4. Comments
    - DTL에서의 주석

---

## Form의 역할

``` html
<form action="/receiver" method="GET">
    <input type="text" name="query" id="message">
    <input type="submit" value="submit">
</form>
```

주소/test에서 위 코드로 구성된 페이지가 있다고 가정해보자.

input에 test라는 글자를 넣고 submit 버튼을 누른다면

query=test라는 params가 생성될 것이다.

위의 params가 생성되는 이유는 form의 method가 GET이기 때문이다.

GET, POST 등의 method가 있는데, GET의 경우 입력값을 그대로 params에 넣어버리고 action의 위치로 보낸다. (따라서 보안이 필요한 정보는 GET을 쓰면 안된다.)

따라서 주소 /receiver?query=test 로 이동될 것이다.


URL에서 해당 파라미터를 사용하려고 params를 넣었으니 이제 사용하는 방법을 알아보자.

이 값은 Query String Parameters라고 하는데, 입력 데이터를 key=value쌍으로 보낸 것이다.

params에 있는 값은 request에 그대로 담겨있으니 사용하는 프레임워크에 따라 request에서 추출하면 된다.

django를 기준으로는 request.GET.get('받을 값의 name')를 통하여 필요한 값을 얻을 수 있다.

이 test 값을 목적지의 페이지에 넘겨주면 된다.

``` python
def receive(request):
    query = request.GET.get('query')
    context = {
        'text': query,
    }
    return render(request, 'receiver.html', context)
```

---

## Django URLs

기본적으로 프로젝트를 만들면 urls.py가 있다.

하지만 app을 만들때마다 주소의 범위는 넓어질텐데 이것을 어떻게 처리할까?

다음의 예시를 통해 살펴보자.

``` python
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
```

만약에 홈페이지에서 항목마다 게시판이 있다면, 또한 다양한 기능이 있다면 상당히 복잡할 것이다.

하지만 공통점을 보면 단순화 시킬 수 있다.

먼저 게시판의 세부 게시물인 board/1을 봤을 때,

모든 세부 게시물은 board/num의 형태로 될 것이다.

따라서 위의 경우 다음과 같이 작성할 수 있다.

``` python
urlpatterns = [
    path('app1/board/<int:num>/', views.detail),
]
```

이제 변수를 통해 들어오는 것은 위의 형태로 범위를 줄일 수 있다.

이것을 Variable Routing이라고 한다.

다음으로 앱에 무관계하게 모든 url이 적혀있는데, 이것을 앱에 따라 나눌 수 있다.

프로젝트의 urls.py를 다음과 같이 바꿔보자.

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
from .import views

urlpatterns = [
    path('board/', views.board),
    path('board/<int:num>/', views.detail),
    path('board/write/', views.write),
]
```

``` python
# app2/urls.py
from django.urls import path
from .import views

urlpatterns = [
    path('board/', views.board),
    path('board/<int:num>/', views.detail),
    path('board/write/', views.write),
]
```

여기서 include()는 일치하는 부분까지 잘라내고, 나머지는 include된 URL로 전달한다.

이것을 App URL mapping이라고 한다.

---

## Naming URL patterns

url 태그는 주어진 URL 패턴의 이름과 일치하는 절대 경로 주소를 반환한다.

URL에 이름을 지정하면 URL의 주소를 일일이 따라가면서 고칠 필요가 없다.

이름을 지정하기 위해 path 함수의 name 키워드 인자를 사용한다.

이름을 지정했을 때 어떠한 변화가 발생하는지 코드를 통해 따라가보자.

``` python
# app2/urls.py
from django.urls import path
from .import views

urlpatterns = [
    path('board/', views.board, name='board'),
    path('board/<int:num>/', views.detail, name='detail_board'),
    path('board/write/', views.write, name='write'),
]
```

``` html
<!-- app2/board.html -->

{% block content %}
    <a href="/board/write">글쓰기</a>
    <a href="/board/1">1번 게시물</a>
{% endblock content %}

---------------------------

<!-- app2/board.html -->

{% block content %}
    <a href="{% url 'write' %}">글쓰기</a>
    <a href="{% url 'detail_board' %}">1번 게시물</a>
{% endblock content %}
```

위의 코드를 보면 이제 일일이 주소를 입력하지 않아도 되는 것을 확인할 수 있다.

하지만 여전히 문제점이 하나 남아있는데,

서로 다른 app에서 같은 기능의 코드가 있으면 중복되는 이름을 가질 수 있다.

이 문제는 app에 이름을 붙이는 것으로 해결할 수 있다.

``` python
# app2/urls.py
from django.urls import path
from .import views

app_name = 'review'
urlpatterns = [
    path('board/', views.board, name='board'),
    path('board/<int:num>/', views.detail, name='detail_board'),
    path('board/write/', views.write, name='write'),
]
```

이제 url 태그의 양식에 맞추면 url은 다음과 같아진다.

``` html
<!-- app2/board.html -->

{% block content %}
    <a href="{% url 'review:write' %}">글쓰기</a>
    <a href="{% url 'review:detail_board' num=1 %}">1번 게시물</a>
{% endblock content %}
```