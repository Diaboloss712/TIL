Git 연습

Working Directory : 코드를 작성하는 곳
Staging : 로컬에서 버전관리가 되고 있는 상태
Repository : 서버 단위에서 관리가 되고 있는 상태

Untracked, Modified = Working Directory
git add : Working Directory -> Straging Area
New file, Modified = Staging Area
git commit : Staging Area -> Repository

git init : 현재 폴더에서 버전관리 시작
주의사항 : 디렉토리 내부 하단에서 git init 금지
           사용시 상위 git에서는 하위 git 추적 불가
git status : 현재 파일들의 버전 관리 상태(추적되고 있는지)
git add filename : filename에 해당하는 파일을 Staging
git commit : 분산 저장소에 관리시작
git log : 커밋한 로그 확인 
git config --global -l : git global 설정 확인

단, git commit 하기 전에 아래와 같이  이메일과 유저이름 설정이 필요
git config --global user.email "이메일주소"
git config --global user.name "유저이름"

git config --global alias.st 'status' : alias는 별명, status를 st로 줄임

git , : 모든 파일 추가
폴더채로 관리가 가능, "folder"라고 할때 git add folder/
git add -A : 작성한 모든 코드에 작동


gitignore : git 추적을 받지 않게하는 설정 파일(env파일, Secret Key)
git remote nickname url : nickname에 url을 저장
git remote -v : 현재 담겨있는 주소 목록 보여주기 
git remote remove nickname : nickname에 해당하는 연결 삭제
git push nickname branchname : nickname에 해당하는 branchname으로 push
git pull nickname branchname : nickname에 해당하는 branchname으로 pull
git clone url : url주소의 repository를 다운로드
