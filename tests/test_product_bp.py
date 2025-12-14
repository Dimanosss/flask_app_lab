import unittest
from app import create_app

class TestProductBlueprint(unittest.TestCase):
    """Тести для блюпринта products"""
    
    def setUp(self):
        """Налаштування перед кожним тестом"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_list_products_route(self):
        """Тест маршруту /products/"""
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Каталог продуктів'.encode('utf-8'), response.data)
        self.assertIn('продукт'.encode('utf-8'), response.data.lower())
    
    def test_product_detail_route(self):
        """Тест маршруту /products/<product_id>"""
        # Тест з існуючими продуктами
        for product_id in [1, 2, 3]:
            with self.subTest(product_id=product_id):
                response = self.client.get(f'/products/{product_id}')
                self.assertEqual(response.status_code, 200)
                self.assertIn('грн'.encode('utf-8'), response.data)
    
    def test_product_detail_not_found(self):
        """Тест маршруту /products/<product_id> з неіснуючим ID"""
        response = self.client.get('/products/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('не знайдено'.encode('utf-8'), response.data.lower())
    
    def test_product_detail_with_invalid_id(self):
        """Тест маршруту /products/<product_id> з невалідним ID"""
        response = self.client.get('/products/abc')
        # Flask поверне 404 для невалідного int
        self.assertEqual(response.status_code, 404)
    
    def test_products_template_inheritance(self):
        """Перевірка, що шаблони products наслідують base.html"""
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        # Перевірка наявності елементів з base.html
        self.assertIn(b'Lab3', response.data)
        self.assertIn(b'navbar', response.data)
    
    def test_product_list_contains_products(self):
        """Перевірка, що список продуктів містить дані"""
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        # Перевірка наявності назв продуктів
        self.assertIn('Ноутбук'.encode('utf-8'), response.data)
        self.assertIn('Смартфон'.encode('utf-8'), response.data)
        self.assertIn('Планшет'.encode('utf-8'), response.data)

if __name__ == '__main__':
    unittest.main()

