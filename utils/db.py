from tinydb import TinyDB, where
from datetime import datetime

DB_FILE = 'db.json'


class AccountsDB:
    def __init__(self):
        db = TinyDB(DB_FILE)
        self.accounts = db.table('Accounts')

    def save(self, email: str, token: str, remarks: str = ''):
        email = email.strip()
        token = token.strip()
        date = datetime.today().strftime('%Y-%m-%d')
        if self.accounts.get(where('token') == token):
            raise Exception('Token already exists in database')
        self.accounts.insert({
            'email': email,
            'token': token,
            'remarks': remarks,
            'date': date
        })

    def all(self):
        return self.accounts.all()

    def get(self, doc_id: int):
        return self.accounts.get(doc_id=int(doc_id))

    def remove(self, doc_id: int):
        self.accounts.remove(doc_ids=[int(doc_id)])

    def count(self):
        return len(self.accounts.all())
