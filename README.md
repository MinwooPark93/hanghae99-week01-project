# 어서오'쉐어'

"코로나 3년! 집돌이, 집순이들의 방자랑하기.
나와 다른사람들의 방이 어떻게 꾸며졌나 공유하고 자랑해보자!
어서오'쉐어'는 우리들의 방을 꾸미고 자랑하는 방스타그램같은 페이지 입니다 :)"

--------------


## 1. 제작 기간 & 팀원 소개

* 2022년 3월 7일 ~ 2022년 3월 10일
* 4인 1조 팀 프로젝트
>* 박민우: Login page - JSON WEB TOKEN 사용하여 로그인 & 로그아웃 기능 구현, 디자인, main CSS
>* 김일권: Main page - 메인페이지 swiper 라이브러리 이용 슬라이더 기능 구현 ( python loop index 사용 ) & CSS
>>* Jinja2 Template Engine 사용 SSR 구현
>* 천은호: My page - 마이페이지 내가 쓴 글 POST, GET 기능 & Jinja2 Template Engine 사용 SSR 구현
>* 조병윤: Main page_modal - 메인페이지의 POST, GET 서버단과 프론트엔드 Ajax기능 구현

--------------


## 2. 사용 기술 및 Tool

```
Back-end
```
* Python 3
* Flask
* MongoDB
* Jinja2

```
Front-end
```
* Javascript
* JQuery
* Bulma
* Bootstrap

```
deploy
```
* AWS EC2 (Ubuntu 20.04 LTS)

--------------


## 3. 어서오'쉐어' 링크

* <http://codefeed.shop/login>

--------------


## 4. S.A (Starting Assignment)

* 블로그 S.A 링크: <https://codefeed.tistory.com/24>

--------------


## 5. 실행화면 링크

* 시연 영상 링크: <https://www.youtube.com/watch?v=5tzO5esJYwA>

--------------


## 6. 핵심기능

* 회원가입, 로그인 & 로그아웃
>* JWT를 사용, 로그인과 회원가입 기능 구현
>* 아이디 중복확인이 가능하며, 정규식을 사용하여 특수문자와 최대글자수 구현

* 메인페이지 swiper, Image upload, modal 기능 구현
>* Swiper 라이브러리 이용 Slide기능 & Image upload 기능 구현

* 마이페이지
>* Jinja2 Template Engine 사용 SSR(Server Side Rendering) 기능 구현
>* Database 정보 delete 기능 구현

--------------


## 7. Trouble shooting

>* 1. python3 decode(JWT 사용중 hash암호화 작업시)
>>* 이슈 내용 : token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')에 의한 **INTERNAL SERVER ERROR** 발생
>>* 로컬개발환경에서는 .decode('utf-8')을 사용하였을때 sever error 발생    
>>* 해결 방법 :  python3.6 ver 이상부터 사용하지 않는 방식이다. 
>>>* 서버 환경에 있는 python의 version에 따라 .decode('utf-8') 부분을 추가,삭제 해야할지 고민해야하고, 이번 프로젝트 상황에서는 추가를 하여 이슈 해결

>* 2. python으로 mongodb에 images 또는 files를 넣을때 GridFS 라이브러리 사용
>>* 이슈 내용 : mongoDB에 이미지 또는 Files이 저장되지 않는 이슈 발생
>>* 해결 방법 : python으로 mongodb에 images 또는 files를 넣을때 GridFS 라이브러리 사용 16mb가 넘는 사이즈의 데이터를 청크로 나누어 저장하는 방식이 있다는 것을 서칭 후 적용
>>>* 추후 encode 사용하여 이미지 저장기능 구현 공부 필요.

>* 3. Pycharm venv 파일 보이지 않는 현상 발생.
>>* 이슈 내용 : Github에서 Repository 클론한 이후 로컬에서 파일 작업을 하던 중 MongoDB와 연동이 되지 않는 이슈가 발생했고 venv 폴더가 없음을 확인함. 
>>* 해결 방법 : 인터프리터 추가를 (설정 → 인터프리터 추가)경로로 생성하려 하였으나 실패하였고 PyCharm 우측 하단에 인터프리터 설정란에서 추가하여 해결

>* 4. Database에서의 Delete를 원한다면 애초에 포스팅 시, 고유 ID값이 존재해야만 한다.
>>* 이슈 내용 : Delete 구현을 위한 고유 ID 값을 포스팅 시 구현하지 않아 삭제 기능 구현에 어려움을 느낌
>>* 해결 방법 : ID값을 추가하는 방법도 있었으나 현재는 .png 파일명을 활용하여 디렉토리 및 DB에서 삭제 구현

>* 5. CSS 순서에 의해 충돌 현상 발견 다른 종류의 부트스트랩을 사용하며 modal 기능이 겹쳐 사용이 불가했음.
>>* 이슈 내용 : 각자 작업한 내용 취합 후 CSS가 깨지거나 작동이 되지 않는 이슈 발생, 부트스트랩에서 가져온 CSS와 
>>>* CSS 작업물에서 충돌이 발생하여 우선된 CSS만 작동하는 이슈로 확인
>>* 해결 방법 : 직접 작성한 CSS를 제외하고 부트스트랩으로 재 작성하여 프로젝트 내 CSS 충돌 제거

>* 6. Github Push & Merge
>>* 이슈 내용 : Merge 과정에서 xml 등 각자 개발 환경에서의 차이로 Merge 에러 발생
>>* 해결 방법 : 실제로 작업을 하고 필수로 Push해야 하는 작업물만 체크하여 Commit 후 Push

>* 7. Github 관리
>>* 이슈 내용 : Merge 과정에서 실수가 발생하여 작업 내용이 초기화 되는 이슈 발생.
>>* 해결 방법 : Master와 Merge등의 작업을 하지 않고 메인 버전을 mk1,2,3 등으로 여러개 나누어 버전별로 작업한 후 최종 취합 후 Master에 Merge함

>* 8. querySelector()로 Click 구현 시 가장 우선되는 버튼 1개만 작동
>>* 이슈 내용 : 바닐라 자바스크립트로 Modal창을 구현하면서 'querySelector()'함수를 사용하였는데,
>>>* 동일한 Class의 버튼을 여러개 지정해야하는 상황에서 첫 번째 요소만 반환되는 이슈 발생.
>>* 해결 방법 : Modal창을 CSS충돌 이슈로 부트스트랩으로 변경하면서 해당 이슈는 다루지 않았으나
>>>* 'querySelectorAll()'을 활용하면 해결 가능하지 않았을까 생각됨.

>* 9. Get으로 불러올 때 url지정
>>* 이슈 내용 : Get으로 DB 내 데이터를 불러오는 과정에서 url을 착각하여 Get으로 데이터는 불러왔지만 HTML에 적용이 안되는 이슈
>>* 해결 방법 : Console.log로 출력하여 Get 기능은 이상없음을 확인했고 구현하려는 페이지와의 끊어진 접점을 찾던 중 url이 잘못 설정되었음을 확인하여 수정


--------------


## 8. 개인 회고

박민우: <>
김일권: <>
천은호: <>
조병윤: <>
