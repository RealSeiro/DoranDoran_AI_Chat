# techContext — 기술 스택과 개발 환경 (계획서 4.2)

## 앱 (`android/`, 강현준)
Kotlin · Jetpack Compose · Android Studio, Gradle · Navigation Compose · Retrofit, OkHttp, Kotlin Coroutines ·
STT: Android SpeechRecognizer · TTS: Android TextToSpeech · 푸시: FCM · 개발 보조: OpenAI Codex

## AI (`server/ai/`, 곽민석)
- Python, LLM API (대규모 학습 없음). LangChain 등 프레임워크는 검토 중
- **모델 선정**: 한국어 벤치마크 KoBALT 결과로 후보 → 기억 추출·기억 기반 응답·불명확 발화 처리를 자체 테스트 → API 제공 여부·비용·응답 속도로 최종 선정
- 지금은 규칙 기반 가짜 AI(`fake.py`)가 연결돼 있음. 진짜 AI는 `ai/llm.py`에 만들고 `python scripts/check_ai.py ai.llm` 통과 후 `ai/__init__.py` import 교체

## 서버 (`server/`, 김도현)
- Python, FastAPI, Pydantic (앱 요청과 AI 출력을 같은 방식으로 검증), SQLAlchemy 2, psycopg 3
- 인증: JWT (앱은 토큰만 보관), 비밀번호 PBKDF2 해시
- 알림·예약 작업: FCM(firebase-admin, 키 없으면 콘솔 출력만), APScheduler (하루 1번 알림, 멈춘 대화 정리, 원문 보관기간 정리)
- DB: PostgreSQL 16 (`server/docker-compose.yml`, 처음 켤 때 `schema.sql` 자동 실행: 테이블 16개 + 퀴즈 30문제)
- 실행 방법: `server/README.md` "처음 실행 (Windows)"
- 설정은 `.env` (`server/.env.example` 복사). `JWT_SECRET`이 32자 미만이거나 예시 값이면 서버가 일부러 안 켜진다.

## 개발·배포 (계획 기준)
Docker, GitHub · **클라우드 서버(HTTPS) 상시 가동** (알림이 제시간에 나가도록) — 아직 안 함

## 주요 설정값 (`server/app/config.py`, `.env`)
| 이름 | 기본 | 뜻 |
|---|---|---|
| `DAILY_INVITE_TIME` | 10:00 | 하루 1번 대화 알림 시각 (한국 시간) |
| `TURN_RETENTION_DAYS` | 30 | 대화 원문 보관 기간 (계획서 4.3: 30일) |
| `MEMORIES_IN_CONTEXT` | 30 | AI에 넘기는 기억 수. **0이면 기억 없이 대화 = 6장 Baseline 실험** |
| `QUIZ_ONLY_VERIFIED` | 0 | 1이면 검수 끝난 퀴즈만 출제 (계획서: 검수한 문제만 출제 → 검수 후 1로) |

## 검증 도구
| 명령 | 하는 일 | DB 필요 |
|---|---|---|
| `python scripts/ai_verify.py` | 바뀐 폴더에 맞는 검사를 모아서 실행 (AI가 끝내기 전에 돌림) | 있으면 더 많이 검사 |
| `cd server && python scripts/check_ai.py [모듈]` | AI 모듈이 `contract.py` 약속을 지키는지 | 아니오 |
| `cd server && python scripts/demo.py` | 사용자 흐름 전체 시연 + 서버 규칙 확인 (43개) | 예 |

## 앱에서 서버 접속
- 에뮬레이터 `http://10.0.2.2:8000`, 실제 폰은 `uvicorn ... --host 0.0.0.0` 후 `http://<PC IP>:8000`
- 모든 요청에 `Authorization: Bearer <토큰>` (어르신 `POST /auth/elder`, 보호자 `POST /auth/login`)
