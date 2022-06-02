from django.test import TestCase

from catalog.models import Music, Account, Easy, Normal, Hard, Expert, Master
#Create your tests here.

#template.

#class YourTestClass(TestCase):
#
#    @classmethod
#    def setUpTestData(cls):
#        print("setUpTestData: Run once to set up non-modified data for all class methods.")
#        pass
#
#    def setUp(self):
#        print("setUp: Run once for every test method to setup clean data.")
#        pass
#
#    def test_false_is_false(self):
#        print("Method: test_false_is_false.")
#        self.assertFalse(False)
#
#    def test_false_is_true(self):
#        print("Method: test_false_is_true.")
#        self.assertTrue(False)
#
#    def test_one_plus_one_equals_two(self):
#        print("Method: test_one_plus_one_equals_two.")
#        self.assertEqual(1 + 1, 2)

class EasyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Easy.objects.create(Difficulty=1)
    
    def test_Difficulty_label(self):
        easy = Easy.objects.get(pk=1)
        field_label = easy._meta.get_field('Difficulty').verbose_name
        self.assertEqual(field_label, 'Difficulty')

class MusicModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        easy = Easy.objects.create(Difficulty=1)
        normal = Normal.objects.create(Difficulty=5)
        hard = Hard.objects.create(Difficulty=10)
        expert = Expert.objects.create(Difficulty=20)
        master = Master.objects.create(Difficulty=30)
        Music.objects.create(title="TEST001", easy = easy, normal = normal, hard = hard, expert = expert, master = master, num=1)
    
    def test_Easy_label(self):
        music = Music.objects.get(num=1)
        field_label = music._meta.get_field("easy").verbose_name
        self.assertEqual(field_label, 'easy')
    def test_Normal_label(self):
        music = Music.objects.get(num=1)
        field_label = music._meta.get_field("normal").verbose_name
        self.assertEqual(field_label, 'normal')
    def test_Hard_label(self):
        music = Music.objects.get(num=1)
        field_label = music._meta.get_field("hard").verbose_name
        self.assertEqual(field_label, 'hard')
    def test_Expert_label(self):
        music = Music.objects.get(num=1)
        field_label = music._meta.get_field("expert").verbose_name
        self.assertEqual(field_label, 'expert')
    def test_Master_label(self):
        music = Music.objects.get(num=1)
        field_label = music._meta.get_field("master").verbose_name
        self.assertEqual(field_label, 'master')
    
    def test_Title_label(self):
        music = Music.objects.get(num=1)
        field_label = music._meta.get_field("title").verbose_name
        self.assertEqual(field_label, 'title')

    def test_Num_label(self):
        music = Music.objects.get(num=1)
        field_label = music._meta.get_field("num").verbose_name
        self.assertEqual(field_label, 'num')
    
    def test_get_absoulte_url(self):
        music = Music.objects.get(num=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(music.get_absolute_url(),'/catalog/musics/1/')
