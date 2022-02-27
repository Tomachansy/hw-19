from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_data):
        entity = User(**user_data)

        self.session.add(entity)
        self.session.commit()

        return entity

    def delete(self, uid):
        user = self.get_one(uid)

        self.session.delete(user)
        self.session.commit()

    def update(self, user_data):
        uid = user_data.get("id")
        user = self.get_one(uid)
        user.username = user_data.get("username")
        user.password = user_data.get("password")
        user.role = user_data.get("role")

        self.session.add(user)
        self.session.commit()
