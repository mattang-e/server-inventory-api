# server-inventory-api
FastAPI와 PostgreSQL을 이용한 서버 인벤토리 관리 REST API입니다.
Docker Compose를 사용하여 API와 PostgreSQL을 컨테이너 환경에서 실행합니다.

Tech Stack
* Python 3.13
* FastAPI / Uvicorn
* PostgreSQL 17
* psycopg
* Docker / Docker Compose

Python 패키지 버전은 requirements.txt에서 관리합니다.

Architecture

Client
  │ HTTP :8000
  ▼
FastAPI
  │ psycopg
  ▼
PostgreSQL :5432
  │
  ▼
Docker Volume

FastAPI와 PostgreSQL은 Docker Compose의 동일한 네트워크에서 통신하며, DB 접속 정보는 환경변수로 관리합니다.

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/servers` | 전체 서버 조회 |
| GET | `/servers/{server_id}` | 특정 서버 조회 |
| POST | `/servers` | 서버 등록 |
| PUT | `/servers/{server_id}` | 서버 정보 수정 |
| DELETE | `/servers/{server_id}` | 서버 삭제 |

Run
docker compose up -d --build

컨테이너 확인:
docker compose ps

API문서:
http://localhost:8000/docs

로그 확인:
docker compose logs -f api

종료:
docker compose down
