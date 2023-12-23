from django.test import TestCase

from vendors.models import ProductCategory, ServiceCategory, CommonFields, Product,Service,CustomUser
from vendors.forms import ServiceForm, ProductForm

# Create your tests here.

#Testing models
class ProductCategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified object used by all test methods
        ProductCategory.objects.create(name="Gums")

    #this test ensures that the 'name' field has the correct maximum length
    def test_name_max_length(self):
        category = ProductCategory.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length,255)

    #this checks that the string representation of a 'ProductCategory' instance is equal to its 'name' field 
    def test_object_name_is_name_field(self):
        category = ProductCategory.objects.get(id=1)
        excepted_object_name = category.name
        self.assertEquals(excepted_object_name,str(category))


class ServiceCategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified object used by all test methods
        ServiceCategory.objects.create(name="Repair")

    #this test ensures that the 'name' field has the correct maximum length
    def test_name_max_length(self):
        category = ServiceCategory.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length,255)

    #this checks that the string representation of a 'ServiceCategory' instance is equal to its 'name' field 
    def test_object_name_is_name_field(self):
        category = ServiceCategory.objects.get(id=1)
        excepted_object_name = category.name
        self.assertEquals(excepted_object_name,str(category))



class ProductModelTest(TestCase):
    def setUp(self):
        # Create a CustomUser for testing
        self.vendor = CustomUser.objects.create(username='vendor1', password='password123', email='vendor@example.com')

        # Create a ProductCategory for testing
        self.category = ProductCategory.objects.create(name='Electronics')

        # Create a Product instance for testing
        self.product_instance = Product.objects.create(
            vendor=self.vendor,
            item_name='Test Product',
            description='Test Product Description',
            category=self.category,
            items_in_store=10,
            price=99.99
        )

    def test_product_category(self):
        self.assertEqual(self.product_instance.category, self.category)

    def test_product_items_in_store(self):
        self.assertEqual(self.product_instance.items_in_store, 10)

    def test_product_price(self):
        self.assertEqual(self.product_instance.price, 99.99)

    def test_product_str_method(self):
        self.assertEqual(str(self.product_instance), 'Test Product')

    def test_common_fields_vendor(self):
        # Accessing common fields through Product instance
        self.assertEqual(self.product_instance.vendor, self.vendor)

    def test_common_fields_item_name(self):
        self.assertEqual(self.product_instance.item_name, 'Test Product')

    def test_common_fields_description(self):
        self.assertEqual(self.product_instance.description, 'Test Product Description')

    def test_common_fields_image(self):
        self.assertIsNone(self.product_instance.image.file) if self.product_instance.image else None # Since image is nullable

    def test_common_fields_abstract(self):
        # Attempting to create a CommonFields instance directly (should fail)
        with self.assertRaises(Exception):
            common_fields_instance = CommonFields.objects.create(
                vendor=self.vendor,
                item_name='Test Common Fields',
                description='Test Common Fields Description',
            )


class ServiceModelTest(TestCase):
    def setUp(self):
        # Create a CustomUser for testing
        self.vendor = CustomUser.objects.create(username='vendor1', password='password123', email='vendor@example.com')

        # Create a ServiceCategory for testing
        self.service_category = ServiceCategory.objects.create(name='Cleaning')

        # Create a Service instance for testing
        self.service_instance = Service.objects.create(
            vendor=self.vendor,
            item_name='Test Service',
            description='Test Service Description',
            image='service_images/test_image.jpg',
            category=self.service_category,
            is_active=True,
            pricing_type='hourly',
            hourly_rate=25.50
        )

    def test_service_category(self):
        self.assertEqual(self.service_instance.category, self.service_category)

    def test_service_is_active(self):
        self.assertTrue(self.service_instance.is_active)

    def test_service_pricing_type_hourly(self):
        self.assertEqual(self.service_instance.pricing_type, 'hourly')

    def test_service_hourly_rate(self):
        self.assertEqual(self.service_instance.hourly_rate, 25.50)

    def test_service_str_method(self):
        self.assertEqual(str(self.service_instance), 'Test Service')

    def test_common_fields_vendor(self):
        # Accessing common fields through Service instance
        self.assertEqual(self.service_instance.vendor, self.vendor)

    def test_common_fields_item_name(self):
        self.assertEqual(self.service_instance.item_name, 'Test Service')

    def test_common_fields_description(self):
        self.assertEqual(self.service_instance.description, 'Test Service Description')

    def test_common_fields_image(self):
        self.assertIsNotNone(self.service_instance.image)

    def test_common_fields_abstract(self):
        # Attempting to create a CommonFields instance directly (should fail)
        with self.assertRaises(Exception):
            common_fields_instance = CommonFields.objects.create(
                vendor=self.vendor,
                item_name='Test Common Fields',
                description='Test Common Fields Description',
            )


#Test case for forms
class ProductFormTest(TestCase):
    def setUp(self):
        # Create a ProductCategory for testing
        self.category = ProductCategory.objects.create(name='Electronics')

    def test_product_form_valid_data(self):
        form_data = {
            'item_name': 'Test Product',
            'description': 'Test Product Description',
            'image': 'product_images/test_image.jpg',
            'category': self.category.id,
            'items_in_store': 10,
            'price': 99.99,
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_product_form_missing_required_field(self):
        form_data = {
            'item_name': 'Test Product',
            'description': 'Test Product Description',
            'image': 'product_images/test_image.jpg',
            'category': '',  # Missing required field
            'items_in_store': 10,
            'price': 99.99,
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors.keys())

class ServiceFormTest(TestCase):
    def setUp(self):
        # Create a ServiceCategory for testing
        self.service_category = ServiceCategory.objects.create(name='Cleaning')

    def test_service_form_valid_data(self):
        form_data = {
            'item_name': 'Test Service',
            'description': 'Test Service Description',
            'image': 'service_images/test_image.jpg',
            'category': self.service_category.id,
            'is_active': True,
            'pricing_type': 'hourly',
            'hourly_rate': 25.50,
            'daily_rate': None,  # Optional field
            'per_job_rate': None,  # Optional field
        }
        form = ServiceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_service_form_missing_required_field(self):
        form_data = {
            'item_name': 'Test Service',
            'description': 'Test Service Description',
            'image': 'service_images/test_image.jpg',
            'category': '',  # Missing required field
            'is_active': True,
            'pricing_type': 'hourly',
            'hourly_rate': 25.50,
            'daily_rate': None,
            'per_job_rate': None,
        }
        form = ServiceForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors.keys())