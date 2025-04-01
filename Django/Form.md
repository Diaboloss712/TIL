# Form

웹에서 입력값은 단순할수도 있지만 매우 복잡할수도 있다.

현재까지의 예시에서는 값이 몇 종류 없었지만 만약 값이 수십에서 수백개라고 가정해보자.

예시의 방법으로 한다고 가정하면 입력받는 데이터의 개수만큼 코드가 늘어날 것이다.

Form에서는 그런 복잡한 데이터와 유효성 검사를 처리할 수 있는 방법을 제시해준다.

---

## Form class

Form에는 두 가지의 종류가 있다.

``` python
# test/forms.py
from django import forms


class TestForm(forms.Form):
    name = forms.CharField(max_length=10)
    age = forms.IntegerField()

# test/views.py

from .forms import TestForm


def new(request):
    form = TestForm()
    context = {
        'form': form,
    }
    return render(request, 'test/register.html', context)
```

``` html
<!-- test/register.html -->
<form action="{% url 'test:register' %}" method="POST">
    {% csrf_token %}
    {{ form }}
    <input type="submit">
</form>
```

첫번째는 위의 같이 필드 타입을 직접 정의한다.

forms.py는 form들을 모아두는 역할을 한다.

views.py에서는 form 인스턴스를 새로 생성하여 context에 담아 내보낸다.

new.html에서는 csrf 토큰 검사와 {{ form }}이 있는데,

{{ form }}은 위에서 만든 name과 age를 입력받는다.

이 방식은 필드 타입을 직접 정의하기에 입력값을 DB에 저장하지 않을 때 사용한다.

``` python
# test/forms.py
from django import forms
from .models import Test


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'

# test/views.py

from .forms import TestForm

def create(request):
    form = TestForm(request.POST)
    if form.is_valid():
        member = form.save()
        return redirect('test:end')
    context = {
        'form': form,
    }
    return render(request, 'test/register.html', context)
```

두번째 코드는 ModelForm을 사용하여 Model과 연결된 Form을 자동으로 생성해준다.

그렇기에 위의 예시에서 필드를 지정하지 않았어도 Meta에서 model과 fields를 통하여 TestForm이 가지고 있는 필드 전부를 그대로 받는다.


### Meta class

Meta class는 ModelForm의 정보를 작성하는 곳으로 모델의 필드를 그대로 가져오는데,

fields와 exclude를 통하여 필드를 지정할 수 있다.


### Widget

Widget은 input 요소의 속성 및 출력 부분을 변경한다.

forms.py에서 적용시키고 싶은 필드 내부에 다음과 같이 작성하면 된다.

'widget=forms.PasswordInput()'

[widget 종류](https://docs.djangoproject.com/en/5.1/ref/forms/widgets/#numberinput)

에서 widget의 종류를 확인할 수 있다.

---

## form으로 변경 후의 GET, POST 처리

회원을 등록한다고 가정해보자.

view 함수에는 두가지 로직이 필요한데,

GET으로 돌아가는 로직과 POST로 돌아가는 로직이 필요하다.

POST로 들어온다면 회원을 등록하고 페이지를 리턴해야하고,

GET으로 들어온다면 회원의 정보를 적을 페이지를 넘겨주어야한다.

``` python
def register_member_get(request):
    form = TestForm()
    context= {
        'form': form,
    }
    return render(request, 'members/register.html', context)


def register_member_post(request):
    form = TestForm(request.POST)
    if form.is_valid():
        member = form.save()
        return redirect('member:detail', member.pk)
    context= {
        'form': form,
    }
    return render(request, 'members/register.html', context)
```

위의 두 메서드에서 같은 부분을 모아서 하나로 처리하면 다음의 코드와 같아진다.

``` python
def register_member(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            member = form.save()
            return redirect('member:detail', member.pk)
    else:
        form = TestForm()
    context = {
        'form': form,
    }
    return render(request, 'members/register.html', context)
```

is_valid()는 유효성검사를 하는 메서드이다.

modelForm으로 생성했다면 해당 필드를 생성할 때 제약이 그대로 걸려있다.

예시로 name이 forms.CharField(max_length=10)라면

10글자 이상이거나 Char가 아닌 다른 값이 들어오면 유효성 검사를 통과하지 못한다.

context는 form이 유효성 검사를 통과하지 못했을 때 해당 form을 그대로 담아서 다시 반환하고,

GET에서 비어있는 form일때도 그 상태로 반환하면 된다.

그럼 생성이 아닌 정보를 수정하는 코드도 같은지 살펴보자.

``` python
def update_member(request, pk):
    member = Test.objects.get(pk=pk)
    if request.method == 'POST':
        form = TestForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member:detail', member.pk)
    else:
        form = TestForm(instance=member)
    context = {
        'form': form,
    }
    return render(request, 'members/update.html', context)
```

위의 코드를 살펴보면 TestForm(instance=member)라는 코드가 추가되었다.

form에 instance를 명시해줌으로써 기존에 존재했던 member로 변경하여 수정하는 코드로 바뀌게 된다.

---

### 번외 Form rendering options

``` html
<!-- test/new.html -->

<h1>Test</h1>
<form action="{% url 'test:create' %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
</form>
```

context에 form을 담았기 때문에 {{form}} 으로도 출력이 되지만

위에서 작성한 것처럼 {{ form.as_p }} 로도 가능하다.

form.as 에는 as_table, as_p, as_ul이 있고, 이를 적용하면 태그 안의 데이터로 만들어진다.

<br>

[필드 그룹 종류](https://docs.djangoproject.com/en/5.1/ref/forms/api/#django.forms.BoundField.as_field_group)

의 Default rendering에서 확인할 수 있다.