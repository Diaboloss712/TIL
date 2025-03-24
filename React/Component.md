# Component
마크업, CSS, Javascript를 앱의 재사용 가능한 UI 요소인 컴포넌트로 결합할 수 있다.
태그는 HTML과 동일하게 사용한다.


## 컴포넌트 정의
함수를 정의할 때 대문자로 사용하여야 컴포넌트로 인식된다.
컴포넌트는 다른 컴포넌트 안에 중첩할 수 있지만, 다른 컴포넌트 안에서 정의를 중첩할 수는 없다.


## Root 컴포넌트
1. 컴포넌트를 추가할 JS 파일을 생성
2. 새로 만든 파일에서 함수 컴포넌트를 export (export default function ...)
3. 컴포넌트를 사용할 파일에서 import


파일 하나에는 하나의 default export가 가능하다.
하지만 named export는 여러번 가능하다. (export function ...)
import {function} from '.FileName.js';


## JSX 규칙
1. 하나의 루트 엘리멘트로 반환
    - 한 컴포넌트에서 여러 엘리먼트를 반환하려면, 하나의 부모 태그로 감싸야한다.
2. 모든 태그는 닫아주기
    - 태그를 명시적으로 닫아야한다.
3. 대부분 camelCase로 (react는 소문자 시작)
    - JSX에서 작성된 어트리뷰트는 JavaScript 객체의 키가 된다.


## 중괄호
1. JSX 태그 안의 문자에서만 사용 가능
2. = 바로 뒤의 어트리뷰트를 읽는다
    ex) src={avatar}, src="{avatar}"
    앞의 src는 avatar 변수를 읽지만, "{avatar}" 문자열을 전달한다


## 이중중괄호
JSX에서 객체를 전달하려면 중괄호 쌍으로 객체를 감싸야 한다.

``` JavaScript
  {
    backgroundColor: 'black',
    color: 'pink'
  }
```

## Props 전달
React 컴포넌트는 Props를 이용해 서로 통신한다.
Props는 객체, 배열, 함수를 포함한 모든 JavaScript 값을 전달할 수 있다.
하지만 Props는 불변이어야 하기 때문에 동적 반응을 원한다면 State를 설정해야 한다.

구조 분해 할당
: 배열이나 객체의 속성을 해체하여 그 값을 개별 변수에 담을 수 있게 하는 JavaScript 표현식

``` JavaScript
function Avatar({ person, size }) {
  // ...
}

function Avatar(props) {
  let person = props.person;
  let size = props.size;
  // ...
}
```
