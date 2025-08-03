# 메모짱 (Memojjang) 📝

Django 기반의 현대적이고 사용자 친화적인 메모장 웹 애플리케이션입니다.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 주요 기능

### 📋 메모 관리
- **CRUD 작업**: 메모 생성, 읽기, 수정, 삭제
- **실시간 검색**: AJAX 기반 즉시 검색 기능
- **우선순위 시스템**: 낮음/보통/높음/긴급 우선순위 설정
- **고정 기능**: 중요한 메모를 상단에 고정
- **반응형 디자인**: 모든 기기에서 완벽한 사용 경험

### 📊 통계 대시보드
- **시각적 통계**: Chart.js를 활용한 인터랙티브 차트
- **월별 분석**: 메모 작성 패턴 분석
- **카테고리별 분포**: 우선순위별 메모 분포 확인

### 👤 사용자 관리
- **회원가입/로그인**: Django 내장 인증 시스템
- **프로필 관리**: 개인 메모 공간 제공
- **보안**: 각 사용자의 메모는 완전히 분리됨

### 🎨 현대적 UI/UX
- **Bootstrap 5**: 세련된 디자인과 반응형 레이아웃
- **Smooth Animations**: CSS 애니메이션과 전환 효과
- **다크 모드 지원**: 눈의 피로를 줄이는 다크 테마
- **직관적 인터페이스**: 사용하기 쉬운 인터페이스 디자인

## 🏗️ 기술 스택

### Backend
- **Django 5.2.4**: 강력한 웹 프레임워크
- **Python 3.12+**: 최신 파이썬 버전
- **SQLite/PostgreSQL**: 유연한 데이터베이스 지원

### Frontend
- **Django Templates**: 서버 사이드 렌더링
- **Bootstrap 5**: 반응형 CSS 프레임워크
- **Chart.js**: 데이터 시각화
- **Vanilla JavaScript**: 현대적 ES6+ 문법

### DevOps & Deployment
- **Docker**: 컨테이너화된 배포
- **Nginx**: 웹서버 및 리버스 프록시
- **Gunicorn**: WSGI 서버
- **PostgreSQL**: 프로덕션 데이터베이스

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/JamesJeongTangun/Py-Task3.git
cd Py-Task3
```

### 2. 가상환경 설정
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정
```bash
cp .env.example .env
# .env 파일을 편집하여 필요한 설정을 입력하세요
```

### 5. 데이터베이스 설정
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. 개발 서버 실행
```bash
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000`으로 접속하세요!

## 🐳 Docker로 실행하기

### 개발 환경
```bash
docker-compose up --build
```

### 프로덕션 환경
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📁 프로젝트 구조

```
Py-Task3/
├── .github/
│   ├── workflows/          # GitHub Actions CI/CD
│   └── copilot-instructions.md
├── apps/
│   ├── memos/              # 메모 앱
│   │   ├── models.py       # 메모 데이터 모델
│   │   ├── views.py        # 뷰 로직
│   │   ├── forms.py        # 폼 처리
│   │   ├── admin.py        # 관리자 인터페이스
│   │   └── tests.py        # 단위 테스트
│   └── users/              # 사용자 앱
│       ├── models.py       # 사용자 모델
│       ├── views.py        # 인증 뷰
│       └── forms.py        # 사용자 폼
├── docs/
│   ├── API.md              # API 문서
│   ├── USER_MANUAL.md      # 사용자 매뉴얼
│   └── DEPLOYMENT.md       # 배포 가이드
├── memojjang/
│   ├── settings.py         # Django 설정
│   ├── urls.py             # URL 라우팅
│   └── wsgi.py             # WSGI 설정
├── static/                 # 정적 파일
│   ├── css/                # 스타일시트
│   ├── js/                 # JavaScript
│   └── images/             # 이미지
├── templates/              # Django 템플릿
│   ├── base.html           # 기본 템플릿
│   ├── memos/              # 메모 템플릿
│   └── users/              # 사용자 템플릿
├── docker-compose.yml      # Docker 개발 설정
├── docker-compose.prod.yml # Docker 프로덕션 설정
├── Dockerfile              # Docker 이미지 정의
├── requirements.txt        # Python 의존성
├── manage.py               # Django 관리 스크립트
└── README.md               # 프로젝트 문서
```

## 🧪 테스트

### 전체 테스트 실행
```bash
python manage.py test
```

### 특정 앱 테스트
```bash
python manage.py test apps.memos
python manage.py test apps.users
```

### 커버리지 측정
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage html
```

### 통합 테스트
```bash
python manage.py test apps.memos.test_integration
```

### 성능 테스트
```bash
python performance_test.py
```

## 📖 문서

- [API 문서](docs/API.md) - API 엔드포인트와 사용법
- [사용자 매뉴얼](docs/USER_MANUAL.md) - 애플리케이션 사용 가이드
- [배포 가이드](docs/DEPLOYMENT.md) - 프로덕션 배포 방법

## 🤝 기여하기

1. 이 저장소를 포크하세요
2. 새로운 기능 브랜치를 생성하세요 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋하세요 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시하세요 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성하세요

### 개발 가이드라인

- 코드 스타일: PEP 8 준수
- 테스트: 새로운 기능에는 반드시 테스트 작성
- 문서화: 중요한 기능은 문서 업데이트
- 보안: 보안 취약점 검토 및 개선

## 🔧 개발 도구

### 코드 품질
```bash
# Flake8 린터
flake8 .

# Black 포매터
black .

# isort 임포트 정렬
isort .
```

### 데이터베이스 관리
```bash
# 새로운 마이그레이션 생성
python manage.py makemigrations

# 마이그레이션 적용
python manage.py migrate

# 더미 데이터 생성
python manage.py loaddata fixtures/sample_data.json
```

### 관리자 인터페이스
관리자 인터페이스는 `/admin/`에서 접근할 수 있으며, 다음 기능을 제공합니다:
- 메모 관리 (대량 작업 지원)
- 사용자 관리
- 시스템 통계
- 데이터 내보내기

## 🔒 보안

### 보안 기능
- CSRF 보호
- XSS 방지
- SQL 인젝션 방지
- 보안 헤더 설정
- HTTPS 강제 사용

### 보안 체크리스트
- [ ] 환경변수로 민감한 정보 관리
- [ ] 강력한 SECRET_KEY 사용
- [ ] HTTPS 설정
- [ ] 정기적인 의존성 업데이트

## 📊 성능

### 최적화 기능
- 데이터베이스 쿼리 최적화
- 정적 파일 캐싱
- Gzip 압축
- 이미지 최적화

### 성능 모니터링
```bash
# Django Debug Toolbar 사용
pip install django-debug-toolbar

# 느린 쿼리 분석
python manage.py shell
>>> from django.db import connection
>>> print(connection.queries)
```

## 🌍 국제화 지원

현재 한국어로 제공되며, 다국어 지원 확장 예정입니다.

## 📈 로드맵

### v1.1 (예정)
- [ ] 태그 시스템
- [ ] 메모 공유 기능
- [ ] 파일 첨부 지원
- [ ] 모바일 앱

### v1.2 (예정)
- [ ] 실시간 협업
- [ ] AI 기반 메모 추천
- [ ] API 확장
- [ ] 플러그인 시스템

## ❓ FAQ

### Q: 데이터베이스를 PostgreSQL로 변경하려면?
A: `.env` 파일에서 데이터베이스 설정을 변경하고 `psycopg2-binary`를 설치하세요.

### Q: 프로덕션 배포 시 주의사항은?
A: [배포 가이드](docs/DEPLOYMENT.md)를 참조하세요.

### Q: API만 사용하고 싶어요
A: [API 문서](docs/API.md)를 참조하여 REST API를 활용하세요.

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 👏 감사의 말

- Django 커뮤니티
- Bootstrap 팀
- Chart.js 개발자들
- 모든 기여자들

## 📧 연락처

- **이슈 리포트**: [GitHub Issues](https://github.com/JamesJeongTangun/Py-Task3/issues)
- **기능 요청**: [GitHub Discussions](https://github.com/JamesJeongTangun/Py-Task3/discussions)

---

⭐ 이 프로젝트가 도움이 되었다면 스타를 눌러주세요!
