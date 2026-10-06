import unittest
import os
from app import app, db, Todo

class TodoTestCase(unittest.TestCase):
    def setUp(self):
        # 테스트용 DB 설정
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_todo.db'
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # 테스트 후 DB 삭제
        with app.app_context():
            db.session.remove()
            db.drop_all()
        if os.path.exists('test_todo.db'):
            os.remove('test_todo.db')

    def test_get_index(self):
        """GET / - 200 OK 및 메인 페이지 HTML 응답"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('할 일 목록'.encode('utf-8'), response.data)

    def test_post_add_success(self):
        """POST /add (제목: \"공부하기\") - 302 Redirect 및 데이터베이스에 \"공부하기\" 저장 확인"""
        response = self.client.post('/add', data={'title': '공부하기'}, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        
        with app.app_context():
            todo = Todo.query.filter_by(title='공부하기').first()
            self.assertIsNotNone(todo)

    def test_post_add_empty(self):
        """POST /add (제목: \"\") - 400 Bad Request"""
        response = self.client.post('/add', data={'title': ''})
        self.assertEqual(response.status_code, 400)

    def test_post_toggle_success(self):
        """POST /toggle/1 (ID 존재) - 302 Redirect 및 해당 ID의 완료 여부 변경 확인"""
        # 먼저 테스트용 데이터 하나 생성
        with app.app_context():
            todo = Todo(title="테스트용")
            db.session.add(todo)
            db.session.commit()
            todo_id = todo.id

        # 완료 상태로 변경 시도
        response = self.client.post(f'/toggle/{todo_id}', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        
        with app.app_context():
            todo = Todo.query.get(todo_id)
            self.assertTrue(todo.completed)

        # 다시 해제 시도
        response = self.client.post(f'/toggle/{todo_id}', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        
        with app.app_context():
            todo = Todo.query.get(todo_id)
            self.assertFalse(todo.completed)

    def test_post_toggle_not_found(self):
        """POST /toggle/999 (ID 없음) - 404 Not Found 에러 발생"""
        response = self.client.post('/toggle/999', follow_redirects=False)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()