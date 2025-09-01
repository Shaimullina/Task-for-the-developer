class TestTask:
    def test_task_created(self, test_task, db):
        """Проверяем, что задача из фикстуры реально существует"""
        task = db.query(type(test_task)).filter_by(id=test_task.id).first()
        assert task is not None
        assert task.title == "Test Task"
        assert task.owner_id == test_task.owner_id

    def test_task_belongs_to_user(self, test_user, test_task):
        """Задача привязана к конкретному пользователю"""
        assert test_task.owner_id == test_user.id
        assert test_task.owner.email == test_user.email
