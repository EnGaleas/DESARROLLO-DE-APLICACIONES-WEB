from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id_usuario, usuario, email):
        self.id = id_usuario
        self.usuario = usuario
        self.email = email