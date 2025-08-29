# 🚀 PDF 병합기 웹 버전 배포 가이드

이 가이드는 PDF 병합기 웹 버전을 Streamlit Cloud에 배포하는 방법을 설명합니다.

## 📋 사전 준비

1. **GitHub 계정**: GitHub 계정이 필요합니다
2. **Streamlit Cloud 계정**: [share.streamlit.io](https://share.streamlit.io)에서 가입

## 🔧 배포 단계

### 1단계: GitHub 저장소 생성

1. GitHub에서 새 저장소 생성
2. 저장소 이름: `pdf-merger-web` (또는 원하는 이름)
3. Public 또는 Private 선택

### 2단계: 로컬 저장소 설정

```bash
# 1. 프로젝트 디렉토리로 이동
cd pdf_merger_web

# 2. Git 초기화
git init

# 3. 파일 추가
git add .

# 4. 첫 번째 커밋
git commit -m "Initial commit: PDF Merger Web Version"

# 5. GitHub 원격 저장소 추가 (YOUR_USERNAME을 실제 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/pdf-merger-web.git

# 6. 메인 브랜치로 설정
git branch -M main

# 7. GitHub에 푸시
git push -u origin main
```

### 3단계: Streamlit Cloud 배포

1. **Streamlit Cloud 접속**: [share.streamlit.io](https://share.streamlit.io)
2. **GitHub 로그인**: GitHub 계정으로 로그인
3. **새 앱 생성**: "New app" 버튼 클릭
4. **저장소 선택**: 방금 생성한 GitHub 저장소 선택
5. **파일 경로 설정**: `streamlit_app.py` 입력
6. **배포**: "Deploy!" 버튼 클릭

## ⚙️ 설정 옵션

### Streamlit Cloud 설정

배포 후 앱 설정에서 다음을 확인하세요:

- **Python 버전**: 3.9 이상 권장
- **메모리**: 기본 설정으로 충분
- **디스크**: 기본 설정으로 충분

### 환경 변수 (필요시)

현재는 특별한 환경 변수가 필요하지 않습니다.

## 🔍 배포 확인

배포가 완료되면:

1. **앱 URL 확인**: Streamlit Cloud에서 제공하는 URL 확인
2. **기능 테스트**:
   - PDF 파일 업로드 테스트
   - 병합 기능 테스트
   - 다운로드 기능 테스트

## 🛠️ 문제 해결

### 일반적인 문제들

1. **의존성 오류**

   - `requirements.txt` 파일이 올바른지 확인
   - Python 버전 호환성 확인
2. **파일 업로드 오류**

   - 파일 크기 제한 확인 (200MB)
   - 파일 형식 확인 (PDF만 지원)
3. **병합 오류**

   - PDF 파일 손상 여부 확인
   - 파일 권한 확인

### 로그 확인

Streamlit Cloud에서 앱 로그를 확인하여 오류를 진단할 수 있습니다.

## 📈 성능 최적화

1. **파일 크기 제한**: 200MB로 설정하여 성능 보장
2. **임시 파일 정리**: 자동으로 임시 파일 삭제
3. **메모리 효율성**: 스트리밍 방식으로 파일 처리

## 🔄 업데이트

코드를 수정한 후:

```bash
# 1. 변경사항 커밋
git add .
git commit -m "Update: [변경 내용 설명]"

# 2. GitHub에 푸시
git push origin main
```

Streamlit Cloud는 자동으로 변경사항을 감지하고 재배포합니다.

## 📞 지원

문제가 발생하면:

1. GitHub Issues에서 버그 리포트
2. Streamlit Cloud 로그 확인
3. 이 문서의 문제 해결 섹션 참조

---

**배포 완료 후 앱 URL을 README.md에 업데이트하는 것을 잊지 마세요!**
