from django.test import TestCase

from catalog.models import Music, Easy, Normal, Hard, Expert, Master, Account
from django.urls import reverse
from random import randint

class MusicListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_musics = 22
        for i in range(10):
            Easy.objects.create(Difficulty=1+i)
            Normal.objects.create(Difficulty=5+i)
            Hard.objects.create(Difficulty=10+i)
            Expert.objects.create(Difficulty=21+i)
            Master.objects.create(Difficulty=26+i)
        for i in range(number_of_musics):
            easy = Easy.objects.get(Difficulty=1+randint(0,9))
            normal = Normal.objects.get(Difficulty=5+randint(0,9))
            hard = Hard.objects.get(Difficulty=10+randint(0,9))
            expert = Expert.objects.get(Difficulty=21+randint(0,9))
            master = Master.objects.get(Difficulty=26+randint(0,9))
            Music.objects.create(title=f"TEST{i+1}", easy = easy, normal = normal, hard = hard, expert = expert, master = master, num=i+1)
    
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/catalog/musics/')
        self.assertEqual(resp.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('music'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('music'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'catalog/music_list.html')

class LikeorUnlikeMusictest(TestCase):

    def setUp(self):
        test_user = Account.objects.create_user(username='test1', email='test@test.com', password='sekai55012')
        test_user.save()
        
        #create music
        number_of_musics = 22
        for i in range(10):
            Easy.objects.create(Difficulty=1+i)
            Normal.objects.create(Difficulty=5+i)
            Hard.objects.create(Difficulty=10+i)
            Expert.objects.create(Difficulty=21+i)
            Master.objects.create(Difficulty=26+i)
        for i in range(number_of_musics):
            easy = Easy.objects.get(Difficulty=1+randint(0,9))
            normal = Normal.objects.get(Difficulty=5+randint(0,9))
            hard = Hard.objects.get(Difficulty=10+randint(0,9))
            expert = Expert.objects.get(Difficulty=21+randint(0,9))
            master = Master.objects.get(Difficulty=26+randint(0,9))
            Music.objects.create(title=f"TEST{i+1}", easy = easy, normal = normal, hard = hard, expert = expert, master = master, num=i+1)

    def test_redirect_if_not_login(self):
        resp = self.client.get(reverse('my_musics'))
        self.assertRedirects(resp, '/accounts/login/?next=/catalog/my_musics/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(email='test@test.com', password='sekai55012')
        resp = self.client.get(reverse('my_musics'))
        self.assertEqual(str(resp.context['user']), 'test1') #cehck login
        self.assertEqual(resp.status_code, 200) #check respone success.
        self.assertTemplateUsed(resp, 'catalog/user_love_musics.html')

    def test_only_favorite_musics_in_list(self):
        login = self.client.login(email='test@test.com', password='sekai55012')
        resp = self.client.get(reverse('my_musics'))
        self.assertTrue('user' in resp.context)
        self.assertEqual(str(resp.context['user']), 'test1') #cehck login
        self.assertEqual(resp.status_code, 200) #check respone success.
        self.assertTrue('object_list' in resp.context)
        self.assertEqual(len(resp.context['object_list']),0)

        ten_musics = Music.objects.all()[:10]
        user = Account.objects.get(username='test1')
        for music in ten_musics:
            user.favorite_musics.add(music)
        
        resp = self.client.get(reverse('my_musics'))
        self.assertTrue('user' in resp.context)
        self.assertEqual(str(resp.context['user']),'test1')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('object_list' in resp.context)
        for music in resp.context['object_list']:
            self.assertEqual(len(user.favorite_musics.filter(num=music.num)), 1)

    def test_like_and_unlike_button(self):
        #test redirect when user not logged in.
        resp = self.client.get('/catalog/like_music/1')
        self.assertRedirects(resp, '/accounts/login/?next=/catalog/like_music/1')

        resp = self.client.get('/catalog/unlike_music/1')
        self.assertRedirects(resp, '/accounts/login/?next=/catalog/unlike_music/1')

        login = self.client.login(email='test@test.com', password='sekai55012')
        self.assertTrue(login)
        test_user = Account.objects.get(email='test@test.com')
        if test_user.favorite_musics.all():
            for music in test_user.favorite_musics.all():
                test_user.favorite_musics.remove(music)

        resp = self.client.get('/catalog/like_music/1')
        self.assertRedirects(resp, reverse('music'))
        self.assertTrue(Music.objects.get(num=1) in test_user.favorite_musics.all())
        self.assertTrue(len(test_user.favorite_musics.all()) == 1)

        resp = self.client.get('/catalog/like_music/1')
        self.assertRedirects(resp, reverse('music'))
        self.assertTrue(Music.objects.get(num=1) in test_user.favorite_musics.all())
        self.assertTrue(len(test_user.favorite_musics.all()) == 1)

        resp = self.client.get('/catalog/like_music/999')
        self.assertRedirects(resp, reverse('music'))
        self.assertTrue(len(test_user.favorite_musics.all()) == 1)

        resp = self.client.get('/catalog/unlike_music/999')
        self.assertRedirects(resp, reverse('music'))
        self.assertTrue(len(test_user.favorite_musics.all()) == 1)

        resp = self.client.get('/catalog/unlike_music/1')
        self.assertRedirects(resp, reverse('music'))
        self.assertTrue(len(test_user.favorite_musics.all()) == 0)
        self.assertTrue(Music.objects.get(num=1) not in test_user.favorite_musics.all())

class PremissionRequiredTest(TestCase):
    
    def setUp(self):
        user1 = Account.objects.create_user(username='normalUser', email='test@test.com', password='sekai55012')
        user1.save()
        user2 = Account.objects.create_superuser(username='superUser', email='test@super.com', password='sekai55012')
        user2.save()

    def test_premission_required(self):
        #not logged in.
        resp = self.client.get(reverse('music-create'))
        self.assertRedirects(resp, '/accounts/login/?next=/catalog/add_music/')

        #normal user.
        login = self.client.login(email='test@test.com', password='sekai55012')
        self.assertTrue(login)
        resp = self.client.get(reverse('music-create'))
        self.assertEqual(resp.status_code,302)
        self.assertRedirects(resp, '/accounts/login/?next=/catalog/add_music/')

        #super user.
        login = self.client.login(email='test@super.com', password='sekai55012')
        self.assertTrue(login)
        resp = self.client.get(reverse('music-create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalog/music_create.html')
