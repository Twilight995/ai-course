```markdown
# Todo App Specification

## 1. 개요
사용자가 간단하게 할 일을 기록하고 관리할 수 있는 웹 애플리케이션입니다. 최소한의 기능만을 갖춘 단순하고 직관적인 할 일 관리 도구를 목표로 합니다.

## 2. 기술
- **Language**: Python 3.x
- **Framework**: Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3 (Pure CSS)

## 3. 파일 구성
- `app.py`: Flask 애플리케이션 메인 로직 및 라우트 정의
- `database.db`: SQLite 데이터베이스 파일
- `models.py`: SQLAlchemy 등을 이용한 데이터 모델 정의 (또는 app.py 내 정의)
- `static/style.css`: 애플리케이션 스타일 시트
- `templates/index.html`: 메인 화면 템플릿
- `test_app.py`: Flask `test_client`를 이용한 기능 테스트 코드

## 4. 동작 규칙

| 라우트 | 메서드 | 입력 | 결과 |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | 없음 | 전체 할 일 목록 페이지 렌더링 |
| `/add` | `POST` | `title` (string) | 새로운 할 일 추가 및 `/`로 리다이렉트 |
| `/toggle/<int:todo_id>` | `POST` | `todo_id` | 할 일의 완료 상태 반전 및 `/`로 리다이렉트 |
| `/delete/<int:todo_id>` | `POST` | `todo_id` | 할 일 삭제 및 `/`로 리다이렉트 |

## 5. 화면
- **메인 화면**:
    - 상단에 할 일을 입력할 수 있는 입력창(Input)과 추가 버튼(Button) 위치.
    - 중앙에 할 일 목록이 리스트 형태로 나열됨.
    - 각 항목은 [완료 체크박스] [할 일 제목] [삭제 버튼]으로 구성.
    - 완료된 항목은 시각적으로 구분되도록 스타일(예: 취소선 또는 흐릿한 색상) 적용.

## 6. 테스트

| 요청 | 기대하는 결과 |
| :--- | :--- |
| `GET /` | 200 OK 및 메인 페이지 HTML 응답 |
| `POST /add` (제목: "공부하기") | 302 Redirect 및 데이터베이스에 "공부하기" 저장 확인 |
| `POST /add` (제목: "") | 400 Bad Request 또는 빈 값 저장 방지 (에러 메시지) |
| `POST /add` (제목: 매우 긴 문자열) | 400 Bad Request 또는 글자 수 제한 적용 |
| `POST /add` (제목: 특수문자 포함) | 200 OK 및 특수문자가 포함된 제목 정상 저장 |
| `POST /toggle/1` (ID 존재) | 302 Redirect 및 해당 ID의 완료 여부 변경 확인 |
| `POST /toggle/999` (ID 없음) | 404 Not Found 에러 발생 |
| `POST /delete/1` (ID 존재) | 302 Redirect 및 해당 ID 데이터 삭제 확인 |
| `POST /delete/999` (ID 없음) | 404 Not Found 에러 발생 |
| `GET /add` (잘못된 메서드) | 405 Method Not Allowed |
| `POST /toggle/abc` (ID 타입 오류) | 404 Not Found 또는 400 Bad Request |

## 7. 완료 전 점검
- [ ] 모든 할 일이 리스트에 올바르게 표시되는가?
- [ ] 할 일을 추가했을 때 즉시 목록에 나타나는가?
- [ ] 완료 체크박스를 누르면 상태가 변경되고 시각적으로 반영되는가?
- [ ] 삭제 버튼을 누르면 목록에서 제거되는가?
- [ ] 데이터베이스에 생성 시각이 자동으로 기록되는가?
- [ ] 순수한 CSS만으로 레이아웃이 깨지지 않고 작동하는가?

## 8. 하지 않는 것
- 사용자 로그인 및 회원가입 기능
- 기존 할 일 내용 수정(Edit) 기능
- 외부 CSS 프레임워크(Bootstrap, Tailwind 등) 사용
- 자바스크립트 프레임워크(React, Vue 등) 사용
```