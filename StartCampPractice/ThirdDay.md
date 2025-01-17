git 2일차
git : 변경사항만 기록하는 분산 버전 관리 시스템
repository : .git

git init : 로컬 저장소 설정(초기화), 관리할 디렉토리에서 실행
git add -A : 모든 추적되는 파일 add
git add . : 현재 디렉토리의 모든 파일 add
git branch name : name으로 branch 생성
git checkout : branch 변경

git 1일차 review
Working Directory -> Staging Area -> Repository
git config --global -l : 전역 설정 확인
git remote -v : 현재 연결되어있는 저장소 확인
git remote add name url : name이라는 저장소 이름으로 url 연결
git remote remove name : name이라는 저장소 삭제
git status : 현재 상태 확인(Untracked, Modified 확인)
             add, commit마다 확인하기
git add filename : filename을 Staging Area에 올릴 파일들을 선별하는 작업
git commit : Staging Area에 저장(로컬 저장소에 저장)
git push name branchname : name이라는 저장소에 branchname의 branch로 push
git pull name branchname : branchname의 branch데이터로 업데이트
git clone url : url의 repository를 복제
