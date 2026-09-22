    def _load_todos(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    loaded_todos = json.load(f)
                    for todo in loaded_todos:
                        if 'deadline' not in todo:
                            todo['deadline'] = None
                    return loaded_todos
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_todos(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"파일 저장 중 오류 발생: {e}")

    def add_todo_with_deadline(self, task, deadline_str):
        deadline = None
        if deadline_str:
            try:
                datetime.strptime(deadline_str, "%Y-%m-%d")
                deadline = deadline_str
            except ValueError:
                print("날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식을 사용하세요. (마감일 없이 추가합니다)")
                deadline = None
        
        self.todos.append({"task": task, "completed": False, "deadline": deadline})
        self._save_todos()
        print(f"'{task}' 항목이 추가되었습니다. (마감일: {deadline if deadline else '없음'})")

    def list_todos(self):
        if not self.todos:
            print("\n현재 할 일 목록이 비어 있습니다.")
            self._current_sorted_todos = []
            return

        self.todos.sort(key=lambda x: x['deadline'] if x['deadline'] else '9999-12-31')
        self._current_sorted_todos = self.todos

        print("\n--- 할 일 목록 ---")
        for index, todo in enumerate(self.todos, start=1):
            status = "[V]" if todo['completed'] else "[ ]"
            deadline_info = f" (마감: {todo['deadline']})" if todo['deadline'] else ""
            print(f"{index}. {status} {todo['task']}{deadline_info}")
        print("------------------")

    def complete_todo(self, index):
        if 0 < index <= len(self._current_sorted_todos):
            target_todo = self._current_sorted_todos[index - 1]
            target_todo['completed'] = True
            self._save_todos()
            print(f"{index}번 항목을 완료로 표시했습니다.")
        else:
            print("잘못된 번호입니다.")

    def delete_todo(self, index):
        if 0 < index <= len(self._current_sorted_todos):
            target_todo = self._current_sorted_todos[index - 1]
            self.todos.remove(target_todo)
            self._save_todos()
            print(f"'{target_todo['task']}' 항목이 삭제되었습니다.")
        else:
            print("잘못된 번호입니다.")

def main():
    manager = TodoManager()
    manager._current_sorted_todos = []

    while True:
        print("\n[ TODO 관리 프로그램 ]")
        print("1. 목록 보기")
        print("2. 할 일 추가")
        print("3. 완료 표시")
        print("4. 삭제")
        print("5. 종료")
        
        choice = input("메뉴를 선택하세요 (1-5): ").strip()

        if choice == '1':
            manager.list_todos()
        elif choice == '2':
            task = input("추가할 할 일을 입력하세요: ").strip()
            if task:
                deadline = input("마감일을 입력하세요 (YYYY-MM-DD, 없으면 엔터): ").strip()
                manager.add_todo_with_deadline(task, deadline)
            else:
                print("내용을 입력해야 합니다.")
        elif choice == '3':
            manager.list_todos()
            if manager.todos:
                try:
                    idx = int(input("완료할 항목의 번호를 입력하세요: "))
                    manager.complete_todo(idx)
                except ValueError:
                    print("숫자를 입력해주세요.")
            else:
                print("목록이 없습니다.")
        elif choice == '4':
            manager.list_todos()
            if manager.todos:
                try:
                    idx = int(input("삭제할 항목의 번호를 입력하세요: "))
                    manager.delete_todo(idx)
                except ValueError:
                    print("숫자를 입력해주세요.")
            else:
                print("목록이 없습니다.")
        elif choice == '5':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 시도해주세요.")

if __name__ == "__main__":
    main()