# Form

웹에서 입력값은 단순할수도 있지만 매우 복잡할수도 있다.

현재까지의 예시에서는 값이 몇 종류 없었지만 만약 값이 수십에서 수백개라고 가정해보자.

예시의 방법으로 한다고 가정하면 입력받는 데이터의 개수만큼 코드가 늘어날 것이다.

Form에서는 그런 복잡한 데이터와 유효성 검사를 처리할 수 있는 방법을 제시해준다.


## Form class 정의

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
    return render(request, 'test/new.html', context)
```

``` html
<!-- test/new.html -->
<form action="{% url 'test:create' %}" method="POST">
    {% csrf token %}
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
        article = form.save()
        return redirect('test:end')
    context = {
        'form': form,
    }
    return render(request, 'test/new.html', context)
```

두번째 코드는 ModelForm을 사용하여 Model과 연결된 Form을 자동으로 생성해준다.

그렇기에 필드를 지정하지 않았어도 TestForm이 가지고 있는 필드를 그대로 받는다.


## Meta class

Meta class는 ModelForm의 정보를 작성하는 곳으로 모델의 필드를 그대로 가져오는데,

fields와 exclude를 통하여 필드를 지정할 수 있다.


### Widget

Widget은 input 요소의 속성 및 출력 부분을 변경한다.

forms.py에서 적용시키고 싶은 필드 내부에 다음과 같이 작성하면 된다.

'widget=forms.PasswordInput()'

https://docs.djangoproject.com/en/5.1/ref/forms/widgets/#numberinput 에서 widget의 종류를 확인할 수 있다.