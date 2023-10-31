from django.test import TestCase
from djangoProject.models import QueryModel
class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        # models tests
        q = QueryModel(system="system", query="query", data="data")
        print(q)
        print(q.get_data())
        print(q.get_query())
        print(q.get_system())
        q.save()
        models = QueryModel.objects.filter(system="system", query="query", data="data")
        print(models)

    # def test_false_is_true(self):
    #     print("Method: test_false_is_true.")
    #     self.assertTrue(False)
    #
    # def test_one_plus_one_equals_two(self):
    #     print("Method: test_one_plus_one_equals_two.")
    #     self.assertEqual(1 + 1, 2)