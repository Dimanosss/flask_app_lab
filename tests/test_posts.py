import unittest
from app import create_app, db
from app.posts.models import Post, CategoryEnum

class T(unittest.TestCase):
    def setUp(self):
        self.app=create_app("testing")
        self.ctx=self.app.app_context(); self.ctx.push()
        db.create_all()
        self.c=self.app.test_client()
    def tearDown(self):
        db.drop_all(); self.ctx.pop()
    def test_create(self):
        r=self.c.post('/post/create', data={
            'title':'A','content':'B','enabled':'y',
            'publish_date':'2025-01-01T12:00',
            'category':CategoryEnum.NEWS.value
        }, follow_redirects=True)
        assert r.status_code==200
        p=db.session.scalar(db.select(Post))
        assert p is not None

if __name__=='__main__':
    unittest.main()
