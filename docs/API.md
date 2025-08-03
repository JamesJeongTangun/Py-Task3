# 메모짱 API 문서

## 개요
메모짱은 Django 기반의 개인 메모 관리 웹 애플리케이션입니다.

## 인증
모든 API 엔드포인트는 Django 세션 기반 인증을 사용합니다.

### 로그인 필요
- 모든 메모 관련 API는 로그인이 필요합니다
- 비인증 요청시 로그인 페이지로 리다이렉트됩니다

## API 엔드포인트

### 1. 메모 목록 조회
```
GET /memos/
```

**설명**: 현재 사용자의 메모 목록을 조회합니다.

**매개변수**:
- `search` (선택): 검색 키워드
- `page` (선택): 페이지 번호

**응답**:
- 200: 성공
- 302: 로그인 필요

**예시**:
```
GET /memos/?search=Django&page=2
```

### 2. 메모 상세 조회
```
GET /memos/{id}/
```

**설명**: 특정 메모의 상세 정보를 조회합니다.

**매개변수**:
- `id`: 메모 ID (경로 매개변수)

**응답**:
- 200: 성공
- 404: 메모를 찾을 수 없음
- 302: 로그인 필요

### 3. 메모 생성
```
POST /memos/create/
```

**설명**: 새로운 메모를 생성합니다.

**요청 데이터**:
```json
{
    "title": "메모 제목",
    "content": "메모 내용",
    "priority": "normal|low|high|urgent",
    "is_pinned": false
}
```

**응답**:
- 302: 생성 성공 (메모 상세 페이지로 리다이렉트)
- 400: 유효하지 않은 데이터
- 302: 로그인 필요

### 4. 메모 수정
```
POST /memos/{id}/edit/
```

**설명**: 기존 메모를 수정합니다.

**매개변수**:
- `id`: 메모 ID (경로 매개변수)

**요청 데이터**:
```json
{
    "title": "수정된 제목",
    "content": "수정된 내용",
    "priority": "high",
    "is_pinned": true
}
```

**응답**:
- 302: 수정 성공
- 400: 유효하지 않은 데이터
- 404: 메모를 찾을 수 없음
- 302: 로그인 필요

### 5. 메모 삭제
```
POST /memos/{id}/delete/
```

**설명**: 메모를 삭제합니다.

**매개변수**:
- `id`: 메모 ID (경로 매개변수)

**응답**:
- 302: 삭제 성공
- 404: 메모를 찾을 수 없음
- 302: 로그인 필요

### 6. AJAX 검색 API
```
GET /memos/search/ajax/
```

**설명**: 실시간 메모 검색을 위한 AJAX API입니다.

**매개변수**:
- `q`: 검색 키워드 (필수)

**응답**:
```json
{
    "results": [
        {
            "id": 1,
            "title": "메모 제목",
            "content": "메모 내용 미리보기...",
            "created_at": "2025-08-03 12:00",
            "updated_at": "2025-08-03 15:30",
            "url": "/memos/1/"
        }
    ],
    "count": 1,
    "query": "검색어"
}
```

**상태 코드**:
- 200: 성공
- 302: 로그인 필요

### 7. 메모 통계
```
GET /memos/stats/
```

**설명**: 사용자의 메모 작성 통계를 조회합니다.

**응답**:
- 200: 성공 (HTML 페이지)
- 302: 로그인 필요

**포함 데이터**:
- 총 메모 수
- 총 단어 수
- 최근 7일 메모 수
- 월별 통계 (차트)
- 사용자 등급

## 데이터 모델

### Memo 모델
```python
{
    "id": integer,
    "title": string (최대 200자),
    "content": text,
    "priority": "low|normal|high|urgent",
    "is_pinned": boolean,
    "author": User,
    "created_at": datetime,
    "updated_at": datetime
}
```

**우선순위 옵션**:
- `low`: 낮음
- `normal`: 보통 (기본값)
- `high`: 높음  
- `urgent`: 긴급

## 오류 코드

### HTTP 상태 코드
- `200`: 요청 성공
- `302`: 리다이렉트 (보통 로그인 필요 또는 성공 후 이동)
- `400`: 잘못된 요청 (폼 유효성 검사 실패)
- `403`: 권한 없음
- `404`: 리소스를 찾을 수 없음
- `500`: 서버 내부 오류

### 일반적인 오류 응답
HTML 폼 기반 애플리케이션이므로 대부분의 오류는 페이지에 메시지로 표시됩니다.

## 사용 예시

### 1. 기본 워크플로우
```javascript
// 1. 로그인 후 메모 목록 조회
GET /memos/

// 2. 새 메모 작성
POST /memos/create/
Content-Type: application/x-www-form-urlencoded

title=새 메모&content=메모 내용&priority=normal&is_pinned=false

// 3. 실시간 검색
GET /memos/search/ajax/?q=검색어

// 4. 메모 수정
POST /memos/1/edit/
Content-Type: application/x-www-form-urlencoded

title=수정된 메모&content=수정된 내용&priority=high&is_pinned=true
```

### 2. JavaScript 예시 (AJAX 검색)
```javascript
// 실시간 검색 구현
function searchMemos(query) {
    fetch(`/memos/search/ajax/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            console.log(`${data.count}개 결과 찾음`);
            displaySearchResults(data.results);
        })
        .catch(error => {
            console.error('검색 오류:', error);
        });
}
```

## 보안 고려사항

### CSRF 보호
- 모든 POST 요청에는 CSRF 토큰이 필요합니다
- Django의 `{% csrf_token %}` 템플릿 태그를 사용하세요

### 권한 제어
- 사용자는 자신의 메모만 조회/수정/삭제할 수 있습니다
- 다른 사용자의 메모에 대한 접근은 차단됩니다

### 입력 검증
- 모든 사용자 입력은 Django 폼을 통해 검증됩니다
- XSS 공격을 방지하기 위해 HTML 이스케이프 처리됩니다

## 성능 최적화

### 페이지네이션
- 메모 목록은 페이지당 12개씩 표시됩니다
- 대량의 메모도 효율적으로 처리 가능합니다

### 검색 최적화
- AJAX 검색은 최대 10개 결과만 반환합니다
- 실시간 검색시 500ms 디바운스 적용

### 캐싱
- 정적 파일은 브라우저 캐싱을 활용합니다
- 개발 환경에서는 캐싱을 비활성화합니다

## 개발 환경 설정

### 요구사항
- Python 3.12+
- Django 5.2+
- 기타 패키지는 `requirements.txt` 참조

### 로컬 실행
```bash
# 가상환경 활성화
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\Activate.ps1  # Windows

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
python manage.py migrate

# 개발 서버 실행
python manage.py runserver
```

### 테스트 실행
```bash
# 전체 테스트
python manage.py test

# 특정 앱 테스트
python manage.py test apps.memos

# 성능 테스트
python performance_test.py
```
