# 정적 파일

사용자가 파일이나 이미지 등의 자원을 요청한다면 서버는 해당하는 자원을 제공해야한다.

정적 파일은 이에 해당하는 자원들 중 상황에 따라 바뀌는 것이 아닌 고정된 자원을 의미한다.

---

## static files 경로

static files는 해당 파일을 직접 내보내는 것이 아닌 해당 파일의 주소를 내보내기 때문에 경로를 알아야한다.

경로는 settings.py에서 조정할 수 있으며, html 단에서는 built-in tag가 아니기에 load tag를 통해 먼저 import 해야 한다.

``` html
<!-- test/register.html -->
{% load static %}
<img src="{% static 'test/logo.png' %}" alt="img">

<h1>Test</h1>
<form action="{% url 'test:create' %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
</form>
```

다음은 settings.py에서 static files를 설정할 때 사용하는 값들이다.
- STATIC_ROOT
- STATIC_URL
- STATICFILES_DIRS

기본적으로 settings.py에 STATIC_URL이 있는데, 위의 값들 중 ROOT는 기초 경로를 설정해준다.

STATICFILES_DIRS는 기본 경로 외의 추가 경로를 지정할 때 사용된다.

STATIC_URL은 해당하는 주소를 static 파일들의 경로로 지정한다.

---

## media files

media files도 먼저 살펴본 static files과 유사하다.

둘의 차이점은 static files는 서버에서 기본적으로 가지고 있던 파일들이고,

media files는 클라이언트에서 파일을 업로드하여 생긴 파일들이다.

media files은 urls.py와 html에서 추가적인 처리가 필요하다.

``` python
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

먼저 urls.py을 살펴보면 urlpatterns 뒤에 코드가 추가되었다.

경로를 체크하기 위해 settings의 파일에서 정보가 필요하다.

그리고 media files도 static files와 유사하게 settings.py에 다음의 값들을 처리해야한다.

- MEDIA_ROOT
- MEDIA_URL

``` html
<!-- test/register.html -->

 <h1>Test</h1>
<form action="{% url 'test:create' %}" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
</form>
```

enctype을 지정해주게 되는데, enctype은 encoding type으로 

데이터를 전송하기 전에 multipart로 지정함으로써 multipart/form-data의 형식으로 데이터가 전송된다.

만약 타입을 전송하지 않는다면

application/x-www-form-urlencoded type으로 전송되고,

이 타입에서는 데이터가 구분되지 않게 되기 때문에

에러가 발생하게 된다.

---

### 번외 models에서 media 경로 설정

``` python
# register/models.py
from django.db import models

class Test(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    #1 image = models.ImageField(blank=True, upload_to='images/')
    #2
    def test_image_path(instance, filename):
        return f'images/{instance.name}/{filename}'
    image = models.ImageField(blank=True, upload_to=test_image_path)
```

model에서 위와 같이 설정하는 방법도 있다.

첫번째 방법은 models.ImageField의 upload_to를 이용하여 경로를 지정하는 방법이다.

두번째 방법은 instance와 filename을 받아 해당 유저의 폴더를 생성하고 파일이름을 만드는 메서드로 구현할 수 있다.

instance는 모델 인스턴스가 생성되는 시점에 pk를 제외한 값들을 가지고 있다.

filename의 경우는 file에 해당하는 name을 filename으로 받아서 입력해주기 때문에 문제가 발생하지 않는다.