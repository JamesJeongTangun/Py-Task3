# 메모짱 배포 가이드

## 🚀 배포 개요

이 가이드는 메모짱 Django 애플리케이션을 다양한 환경에 배포하는 방법을 설명합니다.

## 📋 사전 요구사항

### 시스템 요구사항
- Python 3.12 이상
- Git
- 웹서버 (Nginx, Apache 등)
- 데이터베이스 (PostgreSQL 권장, SQLite 개발용)

### 필수 패키지
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install python3-pip python3-venv nginx postgresql postgresql-server
```

## 🐳 Docker를 이용한 배포 (권장)

### 1. Docker 설치
```bash
# Ubuntu
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

### 2. 프로젝트 클론
```bash
git clone https://github.com/JamesJeongTangun/Py-Task3.git
cd Py-Task3
```

### 3. 환경변수 설정
```bash
cp .env.example .env
nano .env
```

`.env` 파일 설정:
```env
SECRET_KEY=your-very-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=memojjang
DB_USER=memojjang_user
DB_PASSWORD=secure-password
DB_HOST=db
DB_PORT=5432
```

### 4. Docker Compose 실행
```bash
docker-compose up -d
```

### 5. 초기 설정
```bash
# 데이터베이스 마이그레이션
docker-compose exec web python manage.py migrate

# 관리자 계정 생성
docker-compose exec web python manage.py createsuperuser

# 정적 파일 수집
docker-compose exec web python manage.py collectstatic --noinput
```

## 🖥️ 전통적인 서버 배포

### 1. 서버 준비
```bash
# 사용자 생성
sudo adduser memojjang
sudo usermod -aG sudo memojjang
su - memojjang

# 프로젝트 디렉토리 생성
mkdir -p /home/memojjang/apps
cd /home/memojjang/apps
```

### 2. 프로젝트 클론 및 설정
```bash
git clone https://github.com/JamesJeongTangun/Py-Task3.git memojjang
cd memojjang

# 가상환경 생성
python3 -m venv .venv
source .venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 3. 데이터베이스 설정 (PostgreSQL)
```bash
# PostgreSQL 설치 및 설정
sudo -u postgres psql

CREATE DATABASE memojjang;
CREATE USER memojjang_user WITH PASSWORD 'secure-password';
GRANT ALL PRIVILEGES ON DATABASE memojjang TO memojjang_user;
\q
```

### 4. 환경변수 설정
```bash
cp .env.example .env
nano .env
```

프로덕션 `.env` 설정:
```env
SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=memojjang
DB_USER=memojjang_user
DB_PASSWORD=secure-password
DB_HOST=localhost
DB_PORT=5432
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

### 5. Django 설정
```bash
# 마이그레이션
python manage.py migrate

# 정적 파일 수집
python manage.py collectstatic --noinput

# 관리자 계정 생성
python manage.py createsuperuser

# 테스트 실행
python manage.py test
```

### 6. Gunicorn 설정
```bash
# Gunicorn 설정 파일 생성
nano gunicorn.conf.py
```

`gunicorn.conf.py` 내용:
```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 5
preload_app = True
user = "memojjang"
group = "memojjang"
tmp_upload_dir = None
errorlog = "/home/memojjang/apps/memojjang/logs/gunicorn.error.log"
accesslog = "/home/memojjang/apps/memojjang/logs/gunicorn.access.log"
loglevel = "info"
```

### 7. 시스템 서비스 설정
```bash
sudo nano /etc/systemd/system/memojjang.service
```

서비스 파일 내용:
```ini
[Unit]
Description=Memojjang Django Application
After=network.target

[Service]
Type=exec
User=memojjang
Group=memojjang
WorkingDirectory=/home/memojjang/apps/memojjang
ExecStart=/home/memojjang/apps/memojjang/.venv/bin/gunicorn \
    --config gunicorn.conf.py \
    memojjang.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

서비스 활성화:
```bash
sudo systemctl daemon-reload
sudo systemctl enable memojjang
sudo systemctl start memojjang
sudo systemctl status memojjang
```

### 8. Nginx 설정
```bash
sudo nano /etc/nginx/sites-available/memojjang
```

Nginx 설정:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # HTTPS로 리다이렉트
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL 인증서 설정 (Let's Encrypt 권장)
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # 정적 파일
    location /static/ {
        alias /home/memojjang/apps/memojjang/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /home/memojjang/apps/memojjang/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # Django 애플리케이션
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # 보안 헤더
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

Nginx 활성화:
```bash
sudo ln -s /etc/nginx/sites-available/memojjang /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔒 SSL 인증서 설정 (Let's Encrypt)

### 1. Certbot 설치
```bash
sudo apt install certbot python3-certbot-nginx
```

### 2. 인증서 발급
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 3. 자동 갱신 설정
```bash
sudo crontab -e

# 다음 줄 추가
0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 모니터링 및 로깅

### 1. 로그 설정
```bash
# 로그 디렉토리 생성
mkdir -p /home/memojjang/apps/memojjang/logs

# 로그 로테이션 설정
sudo nano /etc/logrotate.d/memojjang
```

로그 로테이션 설정:
```
/home/memojjang/apps/memojjang/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 644 memojjang memojjang
    postrotate
        systemctl reload memojjang
    endscript
}
```

### 2. 모니터링 스크립트
```bash
nano monitor.sh
```

```bash
#!/bin/bash
# 메모짱 상태 모니터링

check_service() {
    if systemctl is-active --quiet $1; then
        echo "✅ $1 is running"
    else
        echo "❌ $1 is not running"
        systemctl restart $1
    fi
}

check_service memojjang
check_service nginx
check_service postgresql

# 디스크 사용량 확인
df -h | grep -E "(/$|/home)"

# 메모리 사용량 확인
free -h
```

실행 권한 설정:
```bash
chmod +x monitor.sh
```

## 🔄 업데이트 및 배포

### 1. 무중단 배포 스크립트
```bash
nano deploy.sh
```

```bash
#!/bin/bash
# 메모짱 배포 스크립트

set -e

PROJECT_DIR="/home/memojjang/apps/memojjang"
BACKUP_DIR="/home/memojjang/backups"

echo "🚀 배포 시작..."

# 백업 생성
echo "📦 데이터베이스 백업..."
mkdir -p $BACKUP_DIR
pg_dump memojjang > $BACKUP_DIR/db_backup_$(date +%Y%m%d_%H%M%S).sql

# 코드 업데이트
echo "📥 코드 업데이트..."
cd $PROJECT_DIR
git pull origin main

# 가상환경 활성화
source .venv/bin/activate

# 의존성 업데이트
echo "📦 의존성 업데이트..."
pip install -r requirements.txt

# 데이터베이스 마이그레이션
echo "🗄️ 데이터베이스 마이그레이션..."
python manage.py migrate

# 정적 파일 수집
echo "🎨 정적 파일 수집..."
python manage.py collectstatic --noinput

# 테스트 실행
echo "🧪 테스트 실행..."
python manage.py test

# 서비스 재시작
echo "🔄 서비스 재시작..."
sudo systemctl restart memojjang
sudo systemctl reload nginx

echo "✅ 배포 완료!"
```

실행 권한 설정:
```bash
chmod +x deploy.sh
```

### 2. 자동 배포 (GitHub Actions)
`.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.PRIVATE_KEY }}
        script: |
          cd /home/memojjang/apps/memojjang
          ./deploy.sh
```

## 🛡️ 보안 체크리스트

### Django 설정
- [ ] `DEBUG = False`
- [ ] 강력한 `SECRET_KEY` 설정
- [ ] `ALLOWED_HOSTS` 적절히 설정
- [ ] HTTPS 리다이렉트 활성화
- [ ] 보안 헤더 설정

### 서버 보안
- [ ] 방화벽 설정 (필요한 포트만 열기)
- [ ] SSH 키 기반 인증
- [ ] 불필요한 서비스 비활성화
- [ ] 정기적인 시스템 업데이트

### 데이터베이스 보안
- [ ] 강력한 데이터베이스 비밀번호
- [ ] 데이터베이스 외부 접근 차단
- [ ] 정기적인 백업
- [ ] 백업 파일 암호화

## 🔧 문제 해결

### 일반적인 문제

#### 1. 502 Bad Gateway
```bash
# Gunicorn 상태 확인
sudo systemctl status memojjang

# 로그 확인
tail -f /home/memojjang/apps/memojjang/logs/gunicorn.error.log
```

#### 2. Static 파일 로딩 실패
```bash
# 정적 파일 재수집
cd /home/memojjang/apps/memojjang
source .venv/bin/activate
python manage.py collectstatic --noinput

# Nginx 설정 확인
sudo nginx -t
```

#### 3. 데이터베이스 연결 오류
```bash
# PostgreSQL 상태 확인
sudo systemctl status postgresql

# 데이터베이스 연결 테스트
psql -h localhost -U memojjang_user -d memojjang
```

### 로그 위치
- Django: `/home/memojjang/apps/memojjang/logs/django.log`
- Gunicorn: `/home/memojjang/apps/memojjang/logs/gunicorn.*.log`
- Nginx: `/var/log/nginx/access.log`, `/var/log/nginx/error.log`

## 📞 지원

배포 중 문제가 발생하면:
1. 로그 파일 확인
2. GitHub Issues에 문제 보고
3. 커뮤니티 지원 요청

---

**성공적인 배포를 위해 각 단계를 차근차근 따라해 주세요! 🚀**
