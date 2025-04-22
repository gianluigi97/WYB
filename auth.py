from connectionDB import Database

class Player: 

    def __init__(self, nome, email, password):
        self.name = nome
        self.email = email
        self.__password = password

    @property 
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, new_password):
        self.__password = new_password
        

