# ORM

## ORM이란?

- **ORM(Object-Relational Mapping)**은 객체 지향 프로그래밍 언어와 관계형 데이터베이스 간에 데이터를 변환(mapping)해주는 기술이다.
- ORM을 사용하면 SQL을 직접 작성하지 않고도 Python 코드로 데이터베이스 작업을 수행할 수 있다.

## QuerySet API

- **QuerySet API**는 Django ORM에서 데이터를 다루기 위해 제공하는 메서드 집합이다.
- **Query**는 데이터베이스에 데이터를 요청하는 구문이다.
- **QuerySet**은 데이터베이스로부터 전달받은 객체 목록이며, 단일 객체일 경우 해당 모델의 인스턴스로 반환된다.
- QuerySet API는 모델 클래스, Manager, QuerySet 메서드로 구성된다.

### Manager

- **Manager**는 Django 모델과 데이터베이스 사이의 쿼리 동작을 위한 인터페이스이다.
- 기본적으로 각 모델은 `objects`라는 이름의 기본 Manager를 가지며, 이를 통해 데이터베이스에 대한 쿼리 작업(조회, 생성, 수정, 삭제 등)을 수행할 수 있다.
- 필요에 따라 사용자가 직접 커스텀 Manager를 작성할 수 있다.

### 주요 QuerySet API 메서드

- `get()`: 조건에 맞는 단 하나의 객체를 반환한다. 조건을 만족하는 객체가 없거나 여러 개일 경우 각각 `DoesNotExist` 예외와 `MultipleObjectsReturned` 예외가 발생한다.
- `filter()`: 주어진 조건에 맞는 객체들을 포함하는 QuerySet을 반환한다.
- `exclude()`: 주어진 조건에 맞지 않는 객체들을 반환한다.
- `values()`: 각 객체를 딕셔너리 형태로 반환한다. 딕셔너리의 key는 필드명이 된다.
- `all()`: 모델의 모든 객체를 포함하는 QuerySet을 반환한다.
- `update()`: 조건에 맞는 객체들을 한 번에 업데이트한다.
- `delete()`: 조건에 맞는 객체들을 삭제한다.

## 예제: 모델 정의 및 CRUD 구현

### 1. 모델 정의

``` python
# app/models.py
from django.db import models

class Test(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField()
```

### 2. Django Shell 설정 및 데이터 생성

- 편리한 Shell 환경을 위해 아래의 패키지를 설치한다.
  
``` bash
  pip install ipython
  pip install django-extensions
```
  
- **주의:** `django-extensions`는 추가 앱이므로, `INSTALLED_APPS`에 등록해야 하며, 이를 통해 확장된 셸 기능을 사용할 수 있다.
- Shell에서 다음 코드를 입력하여 데이터를 생성한다.

``` shell
방법 1: 인스턴스를 생성한 후 save() 호출
test1 = Test()
test1.name = 'user1'
test1.age = 12
test1.save()

방법 2: 생성자에 값을 전달한 후 save() 호출
test2 = Test(name='user2', age=14)
test2.save()

방법 3: objects.create()를 사용하여 한 번에 생성
Test.objects.create(name='user3', age=16)
```

- 위의 코드들은 서로 다른 방식으로 동작하지만, 최종적으로 데이터베이스에 입력한 값대로 저장된다.

### 3. 데이터 조회

- 생성된 데이터를 조회하는 방법에는 `all()`, `filter()`, `get()` 등이 있다.
- Shell에서 다음과 같이 입력하여 데이터를 조회한다.

```python
# 전체 객체 조회
test1 = Test.objects.all()
print(test1)

# 조건에 맞는 객체 조회 (예: age가 14인 경우)
test2 = Test.objects.filter(age=14)
print(test2)

# get() 사용 시 주의: 조건 없이 호출하면 단일 객체를 반환해야 하므로, 여러 객체가 존재할 경우 예외가 발생한다.
test3 = Test.objects.get()
print(test3)
```

- `Test.objects.all()`은 이전에 생성한 3개의 객체가 포함된 QuerySet을 반환한다.
- `Test.objects.filter(age=14)`는 조건에 맞는 객체(예: age가 14인 객체)를 반환한다.
- `Test.objects.get()`은 조건 없이 호출하면 객체가 하나여야 하므로, 여러 객체가 존재할 경우 `MultipleObjectsReturned` 예외가 발생한다.

### 4. 데이터 수정

- 특정 데이터를 수정할 때는 고유성을 보장하는 PK를 기준으로 조회한 후, 원하는 값을 변경하고 저장한다.
- 예를 들어, `user2`의 `age` 값을 수정하려면 다음과 같이 한다.

``` shell
user = Test.objects.get(pk=2)
user.age = 15
user.save()
```

- 이 과정을 통해 해당 사용자의 나이만 수정된다.

### 5. 데이터 삭제

- 특정 데이터를 삭제할 때는 역시 고유성을 보장하는 PK를 기준으로 조회 후 삭제한다.
- 예를 들어, `user3`를 삭제하려면 다음과 같이 한다.

``` shell
user = Test.objects.get(pk=3)
user.delete()
```

## CRUD란?

- 지금까지 회원 정보 등록(Create), 조회(Read), 수정(Update), 삭제(Delete) 작업을 다루었다.
- 이러한 데이터베이스 조작의 기본 작업을 통칭하여 **CRUD**라고 한다.
