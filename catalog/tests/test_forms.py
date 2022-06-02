from django.test import TestCase

from catalog.forms import MusicForm
from catalog.models import Music, Easy, Normal, Hard, Expert, Master

class AddMusicFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        easy = Easy.objects.create(Difficulty=1)
        normal = Normal.objects.create(Difficulty=5)
        hard = Hard.objects.create(Difficulty=10)
        expert = Expert.objects.create(Difficulty=20)
        master = Master.objects.create(Difficulty=30)
        music = Music.objects.create(title="TEST001", easy = easy, normal = normal, hard = hard, expert = expert, master = master, num=1)

    def test_MusicForm_Title_Label(self):
        form = MusicForm()
        self.assertTrue(form.fields['title'].label == 'Title')
    def test_MusicForm_Easy_Label(self):
        form = MusicForm()
        self.assertTrue(form.fields['easy'].label == 'Easy')
    def test_MusicForm_Normal_Label(self):
        form = MusicForm()
        self.assertTrue(form.fields['normal'].label == 'Normal')
    def test_MusicForm_Hard_Label(self):
        form = MusicForm()
        self.assertTrue(form.fields['hard'].label == 'Hard')
    def test_MusicForm_Expert_Label(self):
        form = MusicForm()
        self.assertTrue(form.fields['expert'].label == 'Expert')
    def test_MusicForm_Master_Label(self):
        form = MusicForm()
        self.assertTrue(form.fields['master'].label == 'Master')
    def test_MusicForm_Num_Label(self):
        form = MusicForm()
        self.assertTrue(form.fields['num'].label == 'Num')

    def test_MusicForm_create(self):
        easy = Easy.objects.get(Difficulty=1)
        normal = Normal.objects.get(Difficulty=5)
        hard = Hard.objects.get(Difficulty=10)
        expert = Expert.objects.get(Difficulty=20)
        master = Master.objects.get(Difficulty=30)
        data = {'title':'test002' ,'easy':easy, 'normal':normal, 'hard':hard, 'expert':expert, 'master':master, 'num':2}
        form = MusicForm(data = data)

        self.assertTrue(form.is_valid())    

    def test_MusicForm_create_existed_num(self):
        easy = Easy.objects.get(Difficulty=1)
        normal = Normal.objects.get(Difficulty=5)
        hard = Hard.objects.get(Difficulty=10)
        expert = Expert.objects.get(Difficulty=20)
        master = Master.objects.get(Difficulty=30)
        data = {'title':'test002' ,'easy':easy, 'normal':normal, 'hard':hard, 'expert':expert, 'master':master, 'num':1}
        form = MusicForm(data = data)
        self.assertTrue(form.is_valid())    

    def test_MusicForm_create_existed_title(self):
        easy = Easy.objects.get(Difficulty=1)
        normal = Normal.objects.get(Difficulty=5)
        hard = Hard.objects.get(Difficulty=10)
        expert = Expert.objects.get(Difficulty=20)
        master = Master.objects.get(Difficulty=30)
        data = {'title':'TEST001' ,'easy':easy, 'normal':normal, 'hard':hard, 'expert':expert, 'master':master, 'num':2}
        form = MusicForm(data = data)
        self.assertTrue(form.is_valid())    

    def test_MusicForm_create_without_difficulty(self):
        normal = Normal.objects.get(Difficulty=5)
        hard = Hard.objects.get(Difficulty=10)
        expert = Expert.objects.get(Difficulty=20)
        master = Master.objects.get(Difficulty=30)
        data = {'title':'TEST001' , 'normal':normal, 'hard':hard, 'expert':expert, 'master':master, 'num':2}
        form = MusicForm(data = data)
        self.assertFalse(form.is_valid())    
