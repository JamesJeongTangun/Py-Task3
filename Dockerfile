# Python 3.12 공식 이미지 사용
FROM python:3.12-slim

# 환경변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=memojjang.settings

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 정적 파일 디렉토리 생성
RUN mkdir -p staticfiles logs

# 정적 파일 수집
RUN python manage.py collectstatic --noinput

# 데이터베이스 마이그레이션
RUN python manage.py migrate

# 포트 노출
EXPOSE 8000

# 서버 실행 명령
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
