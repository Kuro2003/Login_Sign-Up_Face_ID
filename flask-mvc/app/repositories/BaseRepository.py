class BaseRepository:
    # def __init__(self, model, session):
    def __init__(self, model):
        print("Base repo")
        self.model = model
        # self.session = session
        
    def find_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
    
    def find_by_id(self, id):
        return self.model.query.filter_by(id=id).first()