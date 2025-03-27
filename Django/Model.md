# Model의 개요

## model 클래스 작성

model 클래스는 app의 내부의 models.py에 작성한다.

``` python
# app/models.py
from django.db import models

class Test(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField()

```

위의 코드를 한줄씩 설명한다면 다음과 같다.

models는 django에서 지원해주는 모듈로 DB를 관리할 때 다양한 메서드를 가지고 있다.

name은 models의 CharField를 가진다.

여기서 models의 뒤에 붙어있는 Field는 필드 클래스로 DB에 저장될 데이터의 속성을 지정해준다.

또한 Field에는 다양한 제약 조건을 걸 수 있다. (유효성 검사, 기본값, 빈 값, null값 등)

이제 위에서 작성한 model 클래스가 DB의 테이블로 전환되기 위해 migration 작업이 필요하다.

- python manage.py makemigrations : DB에 저장하기 전 필드 값들과 해당 속성들에 대한 정보를 담은
000n_inital.py를 생성해준다.

- python manage.py migrate : 생성되었던 파일을 기준으로 db에 저장해준다.

위의 과정에서 추가적으로 필드를 생성해야 한다면 모델 클래스를 재작성하여 위의 과정을 반복하면 된다.

단, 기존 테이블이 존재하기 때문에 필드의 기본 값을 설정해야 하는데 2가지의 방법으로 나뉜다.

1. Provide a ... : 하나의 default 값을 존재하는 모든 행에 넣는다. default value를 설정하지 않으면 기본 값이 설정된다.
2. Quit and manually define a default value in models.py : 진행을 중단하고 models.py에 기본 값 관련 설정을 하여 해결한다.

---

## 관리자 페이지

Automatic admin interface : Django가 기본으로 제공하는 인터페이스다.

이 인터페이스의 장점은 기본적인 생성과 수정, 삭제를 관리자 페이지에서 해볼 수 있다.(db가 동작하는지 확인 가능)

1. admin 계정 생성
    - python manage.py createsuperuser
2. admin.site.register
    - app/admin.py에서 해당 app의 model 클래스를 import하고 등록해주어야한다.

``` python
# app/admin.py

from django.contrib import admin
from .models import Test


admin.site.register(Test)
```

---

### 번외 - DB 초기화

DB를 초기화하려면 DB인 db.sqlite3과 migrations의 n_str.py를 삭제하면 된다.

단, migrations의 __init__.py와 폴더는 삭제하면 안된다.

- migrations 폴더 삭제
    - 필드를 추가하기 위해 model 클래스를 재작성하고 1번을 통하여 진행하면 다음 번호의 파일이 생성되는 것을 볼 수 있다.
    - 이렇게 생성되면 어떠한 변화가 있었는지 history를 알 수 있지만, 폴더를 삭제하면 history가 날아가는 것과 마찬가지다.
    - 이외에도 db에 정보가 저장되기 때문에 충돌이 발생한다.

- init.py 삭제
    - init.py는 해당 폴더를 패키지로 취급하기 위한 파일이다. 삭제 시 인식이 안되기 때문에 문제가 발생한다.
    - 실수로 삭제되었다면 해당 파일을 다시 생성해주면 정상적으로 동작한다.