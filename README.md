# 오픈빌더를 이용한 카카오톡 챗봇 만들기



카카오의 오픈빌더를 이용한 카카오톡 챗봇 개발 예제입니다. 스킬 서버는 Python Flask를 이용하여 구현되었습니다. 본 예제에서는 서울대학교 식당 정보를 제공하는 챗봇을 만듭니다. 데이터는 서울대학교 식단 정보 제공 홈페이지 (http://mini.snu.ac.kr)에서 가져옵니다.



### 파일 설명

- api: flask 서버 폴더
  - api.py: flask로 구현한 스킬서버 예제
  - pyjosa.py: 한글조사 처리를 위한 라이브러리
    https://github.com/myevan/pyjosa
- starter_code: 스킬서버 구현을 위한 flask 템플릿
- test_code: 서울대학교 식당 메뉴 안내 홈페이지 크롤링을 위한 테스트 코드
- tutorial_slides: 오픈빌더 튜토리얼 

