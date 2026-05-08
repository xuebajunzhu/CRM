from django.test import TestCase
from django.urls import reverse
from app01 import models


class CustomerModelTest(TestCase):
    """Test cases for Customer model."""
    
    def setUp(self):
        """Set up test data."""
        self.customer = models.Customer.objects.create(
            qq='123456',
            name='Test User',
            phone='13800138000'
        )
    
    def test_customer_creation(self):
        """Test customer is created correctly."""
        self.assertEqual(self.customer.qq, '123456')
        self.assertEqual(self.customer.name, 'Test User')
        self.assertEqual(self.customer.phone, '13800138000')
    
    def test_soft_delete(self):
        """Test soft delete functionality."""
        # Customer should be visible by default
        self.assertIn(self.customer, models.Customer.objects.all())
        
        # Soft delete
        self.customer.delete_status = True
        self.customer.save()
        
        # Should not appear in default queryset
        self.assertNotIn(self.customer, models.Customer.objects.all())
        
        # Should appear in all_objects
        self.assertIn(self.customer, models.Customer.all_objects.all())
    
    def test_status_display(self):
        """Test status display with color coding."""
        html = self.customer.status_show()
        self.assertIn('span', html)
        self.assertIn('red', html)  # unregistered status is red


class UserInfoModelTest(TestCase):
    """Test cases for UserInfo model."""
    
    def test_user_creation(self):
        """Test user creation."""
        user = models.UserInfo.objects.create(
            username='testuser',
            password='hashed_password',
            telephone='13800138000',
            email='test@example.com'
        )
        self.assertEqual(str(user), 'testuser')


class AuthViewTest(TestCase):
    """Test cases for authentication views."""
    
    def setUp(self):
        """Set up test user with hashed password."""
        from django.contrib.auth.hashers import make_password
        self.user = models.UserInfo.objects.create(
            username='testuser',
            password=make_password('testpass123'),
            telephone='13800138000',
            email='test@example.com'
        )
    
    def test_login_success(self):
        """Test successful login."""
        response = self.client.post(reverse('app01:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('app01:home'))
    
    def test_login_failure(self):
        """Test failed login with wrong password."""
        response = self.client.post(reverse('app01:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "用户名或密码错误")
    
    def test_logout(self):
        """Test logout clears session."""
        # Login first
        self.client.post(reverse('app01:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # Logout
        response = self.client.get(reverse('app01:logout'))
        self.assertRedirects(response, reverse('app01:login'))


class PaginationTest(TestCase):
    """Test cases for pagination utility."""
    
    def test_init_page_creation(self):
        """Test InitPage initialization."""
        from utils.page import InitPage
        
        page = InitPage(current_page=1, data_length=100, show_data_number=10)
        
        self.assertEqual(page.current_page, 1)
        self.assertEqual(page.total_page_count, 10)
        self.assertEqual(page.start_data_number, 0)
        self.assertEqual(page.end_data_number, 10)
    
    def test_invalid_page_number(self):
        """Test handling of invalid page numbers."""
        from utils.page import InitPage
        
        # Test with string
        page = InitPage(current_page='invalid', data_length=100)
        self.assertEqual(page.current_page, 1)
        
        # Test with negative
        page = InitPage(current_page=-5, data_length=100)
        self.assertEqual(page.current_page, 1)
        
        # Test with too large
        page = InitPage(current_page=999, data_length=100)
        self.assertEqual(page.current_page, 10)
