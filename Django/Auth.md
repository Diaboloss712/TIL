# Auth

이번에는 로그인과 로그아웃을 구현할 것인데, 구현하기에 앞서 각종 사이트에서의 로그인을 생각해보자.

쇼핑몰이나 인터넷 서점, 채용 사이트 등 거의 모든 사이트에 로그인 기능이 있고,

로그인을 했을 때 시간제한이 있을 수도 있지만 로그인 상태가 유지가 된다.

그러면 어떻게 로그인 상태가 유지가 되는지 알아보자.


## Cookie

첫번째로 Cookie에 대해 설명하겠다.

작성일인 25년 4월 2일 기준으로 대부분의 외국 사이트에 처음 접속하면 Cookie에 대한 설정을 안내해준다.

이 Cookie가 뭐길래 허용할지 설정을 해야하는걸까?

Cookie는 서버가 클라이언트에게 주는 명찰과 같다.

클라이언트가 서버에 요청했을 때 서버가 클라이언트에게 표식을 심어둔다면 판별하기 매우 쉬울 것이다.

한번 심어뒀다면 다음에 클라이언트가 다시 오면 서버는 해당 클라이언트를 구분할 수 있고, 로그인을 통과시켜주는 것도 가능할 것이다.

<br>

하지만 만약에 이 표식이 탈취당하면 어떻게 될까?

내가 어디에 갔다왔는지에 대한 정보가 고스란히 넘어갈 수도 있고,

로그인의 정보가 담겨있었다면 보안이 위험해질 수도 있다.

그렇기에 서버에서 Session을 같이 사용함으로써 안정성을 더할 수 있다.


## Session

Session은 서버에서 명찰을 들고 있는것과 같다.

클라이언트가 서버에 요청하여 Cookie를 받아가면, 서버는 해당 정보를 저장한다.

그리고 클라이언트가 다시 서버에 요청하게 되면, Cookie와 Session 둘 다 검증하여 판별한다.

Session의 경우 서버가 계속 가지고 있었기 때문에, 위조되거나 탈취당할 위험이 거의 없다.

Cookie에 만료 시간을 추가하거나 Session에 타임아웃 설정을 해준다면 위험성은 더욱 낮아지게 된다.

이렇게 Cookie와 Session을 병행하여 사용함으로써 안정성을 챙기면서 상태를 유지한다.


## Authentication Form

Django에서는 AuthenticationForm을 통하여 Cookie와 Session을 둘 다 관리한다.

사용자가 AuthenticationForm으로 로그인을 성공하면 사용자는 SessionId가 담긴 쿠키를, 서버는 세션 정보를 저장하게 된다.

시작하기에 앞서 accounts라는 app을 만들어서 CustomUser를 만들것이다.

(Django에서 accounts라는 이름을 쓰는 것과 User를 따로 만드는 것을 권장하고 있다.)

1. 먼저 accounts라는 이름의 app을 생성한다.

``` bash
    python manage.py startapp accounts
```

2. 생성한 app을 settings.py를 통하여 등록하고, 기본 User 모델을 등록한다.

``` python
# settings.py
INSTALLED_APPS = [
    'accounts',
    ...
]

AUTH_USER_MODEL = 'accounts.CustomUser'
```

3. accounts에서 urls.py를 만들고 할당한다.

``` python
# accounts/urls.py
from django.urls import path, include
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
```

4. models.py에서 User를 상속받는다.

- django.contrib.auth.models에서 AbstractUser를 상속받으면 기본적인 값들은 그대로 상속받는다.
- 필자는 Custom인것을 명확하게 하기 위해 몇몇 필드를 따로 추가해주었다.
- models.py가 완성되면 admin.py에서 관리자 등록도 설정해두자.

``` python
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    age = models.IntegerField(blank=True)
    main_address = models.CharField(maxlength=100, blank=True)
    mini_address = models.CharField(maxlength=50, blank=True)
    condition = models.CharField(maxlength=20, blank=True)
    condition_degree = models.IntegerField(blank=True)  # 입력은 enum으로
```

``` python
# accounts/admin.py
from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)
```

5. view의 login에서 Form을 AuthenticationForm으로 바꿔준다.

``` python
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('hospital:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)
```