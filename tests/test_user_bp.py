import unittest
from app import create_app

class TestUserBlueprint(unittest.TestCase):
    """Тести для блюпринта users"""
    
    def setUp(self):
        """Налаштування перед кожним тестом"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_hi_route(self):
        """Тест маршруту /users/hi/<name>"""
        # Тест з різними іменами
        test_names = ['Іван', 'Марія', 'TestUser', '123']
        
        for name in test_names:
            with self.subTest(name=name):
                response = self.client.get(f'/users/hi/{name}')
                self.assertEqual(response.status_code, 200)
                self.assertIn(name.encode('utf-8'), response.data)
                self.assertIn('Привіт'.encode('utf-8'), response.data)
    
    def test_admin_route(self):
        """Тест маршруту /users/admin"""
        response = self.client.get('/users/admin')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Адміністративна панель'.encode('utf-8'), response.data)
        self.assertIn(b'admin', response.data.lower())
    
    def test_hi_route_with_special_characters(self):
        """Тест маршруту /users/hi/<name> зі спеціальними символами"""
        response = self.client.get('/users/hi/User%20Name')
        self.assertEqual(response.status_code, 200)
    
    def test_hi_template_inheritance(self):
        """Перевірка, що шаблон hi.html наслідує base.html"""
        response = self.client.get('/users/hi/Test')
        self.assertEqual(response.status_code, 200)
        # Перевірка наявності елементів з base.html
        self.assertIn(b'Lab3', response.data)
        self.assertIn(b'navbar', response.data)

if __name__ == '__main__':
    unittest.main()
