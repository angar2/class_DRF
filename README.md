# drf 학습

>### <1일차>

## 과제
### 1 .args, kwargs를 사용하는 예제 코드 짜보기
: push 내용 확인

<br>

### 2. mutable과 immutable은 어떤 특성이 있고, 어떤 자료형이 어디에 해당하는지 서술하기
: Python에서는 객체의 종류를 두 가지로 구분할 수 있다.

- mutable: 객체의 상태 변경 가능
- immutable: 객체 상태 변경 불가능

immutable은 값이 존재하는 메모리 주소를 참조한다.
값이 같다면 같은 주소를 참조하는데, 
값이 바뀔 경우 실제 메모리의 값을 바뀌는 것이 아니라 참조를 바꾸는 형식이다.
해당하는 자료형은 int, float, tuple, str, bool 등이 있다.

mutable은 각각의 객체가 개별적인 주소를 참조한다.
그렇기에 값 조작의 편의성이 있으며 해당하는 자료형은 list, set, dictionary 등이 있다.

<br>

### 3. DB Field에서 사용되는 Key 종류와 특징 서술하기
:

#### <key 종류> ####

#### Primary Key(기본키)
- ```null```을 허용하지 않음
- unique(유일성) 성질을 지님

#### Candidate Key(후보키)
- 기본키가 될 수 있는 키

#### Alternate Key(대체키)
- 후보키가 둘 이상일 때 기본키를 제외한 나머지 키

#### Foreing Key(외래키)
- 참조되는 릴레이션 기본키와 대응됨
- ```null```을 허용함
- 여러개의 외래키가 존재할 수 있음

<br>

### 4. django에서 queryset과 object는 어떻게 다른지 서술하기
:
#### QuerySet
QuerySet은 데이터베이스에서 전달받은 객체들의 list이다. 
각 객체들은 DB에서 하나의 record(row)에 해당한다.
Python으로 작성한 코드가 SQL로 mapping되어 QuerySet이라는 자료 형태로 값이 넘어온다.
ORM 코드가 객체를 불러오지만 실제 DB에 쿼리가 이루어지는 것은 아니다.
QuerySet의 lazy한 특성으로 인해 실제 데이터를 가져오기 위해서는 iterate시켜야한다.


#### Object
DB는 column(field)와 row(record)에 데이터가 저장된다.
Django에서 필드에 해당하는 부분은 모델의 각 클래스 안에서 지정해준 속성들이다.
레코드에 해당하는 부분은 각 속성에 부여되는 값들이다.
테이블의 레코드마다 dictionary가 저장되는 것이다.
QuerySet안에 있는 객체에 접근할 때에는 value에 접근하는지 dictionary의 요소에 접근하는지에 따라 접근방식이 달라진다.
