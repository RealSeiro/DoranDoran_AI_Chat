# techContext — 기술 스택과 개발 환경

## 서버 (`server/`)
- Python, FastAPI, SQLAlchemy 2, psycopg 3, PyJWT, APScheduler 3, python-dotenv (`server/requirements.txt`)
- PostgreSQL 16 (`server/docker-compose.yml`, 처음 켤 때 `schema.sql` 자동 실행: 테이블 16개 + 퀴즈 30문제)
- 푸시: firebase-admin (키 파일이 없으면 콘솔 출력만)
- 실행 방법은 `server/README.md` "처음 실행 (Windows)"
- 설정은 `.env` (`server/.env.example` 복사). `JWT_SECRET`이 32자 미만이거나 예시 값이면 서버가 일부러 안 켜진다.

## 주요 설정값 (`server/app/config.py`, `.env`)
| 이름 | 기본 | 뜻 |
|---|---|---|
| `DAILY_INVITE_TIME` | 10:00 | 하루 1번 대화 알림 시각 (한국 시간) |
| `TURN_RETENTION_DAYS` | 30 | 대화 원문 보관 기간 (팀 확정 필요) |
| `MEMORIES_IN_CONTEXT` | 30 | AI에 넘기는 기억 수. 0이면 기억 없이 대화 (Baseline 실험용) |
| `QUIZ_ONLY_VERIFIED` | 0 | 1이면 검수 끝난 퀴즈만 출제 |

## 검증 도구
| 명령 | 하는 일 | DB 필요 |
|---|---|---|
| `python scripts/ai_verify.py` | 바뀐 폴더에 맞는 검사를 모아서 실행 (AI가 끝내기 전에 돌림) | 있으면 더 많이 검사 |
| `cd server && python scripts/check_ai.py [모듈]` | AI 모듈이 `contract.py` 약속을 지키는지 | 아니오 |
| `cd server && python scripts/demo.py` | 사용자 흐름 전체 시연 + 서버 규칙 확인 (43개) | 예 |

## 앱에서 서버 접속
- 에뮬레이터 `http://10.0.2.2:8000`, 실제 폰은 `uvicorn ... --host 0.0.0.0` 후 `http://<PC IP>:8000`
- 모든 요청에 `Authorization: Bearer <토큰>` (어르신 `POST /auth/elder`, 보호자 `POST /auth/login`)
