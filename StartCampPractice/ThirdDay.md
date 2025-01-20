# git 2일차

## git 1일차 리뷰 + 정리

git : 변경사항만 기록하는 분산 버전 관리 시스템<br>
commit : 하나의 기능에 관련된 코드를 묶는다<br>
repository : .git<br>
## **Working Directory -> Staging Area -> Repository** <br>
---
git init : 로컬 저장소 설정(초기화), 관리할 디렉토리에서 실행 <br>
git add -A : 모든 추적되는 파일 add <br>
git add . : 현재 디렉토리의 모든 파일 add <br>
git branch name : name으로 branch 생성 <br>
git checkout branchname : branchname의 branch로 변경 <br>
git branch -l : branch list 출력 <br>
git config --global -l : 전역 설정 확인 <br>
git remote -v : 현재 연결되어있는 저장소 확인 <br>
git remote add name url : name이라는 저장소 이름으로 url 연결 <br>
git remote remove name : name이라는 저장소 삭제 <br>
git status : 현재 상태 확인(Untracked, Modified 확인) <br>
             add, commit마다 확인하기 <br>
git add filename : filename을 Staging Area에 올릴 파일들을 선별하는 작업 <br>
git commit : Staging Area에 저장(로컬 저장소에 저장) <br>
git push name branchname : name이라는 저장소에 branchname의 branch로 push <br>
git pull name branchname : branchname의 branch데이터로 업데이트 <br>
git clone url : url의 repository를 복제 <br>
git stash : 현재 올라가지 않은 내용이 stash에 보관 <br>
git stash list : 보관되고 있는 내용 리스트 <br>
git stash pop num : num에 해당하는 보관내용 가져오기 <br>


#API

API : 클라이언트와 서버 사이의 인터페이스 역할 <br>
API Key는 이 통신을 더욱 안전하게 만들기 위한 핵심 수단 <br>

