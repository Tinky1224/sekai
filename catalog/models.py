from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL pattern.
from django.core.validators import MaxValueValidator, MinValueValidator #Used to limit the number of IntegerField.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
class Easy(models.Model):
    Difficulty = models.IntegerField(default = 1, validators=[MinValueValidator(1), MaxValueValidator(40)])

    def __str__(self):
        return f"LV {self.Difficulty}"

class Normal(models.Model):
    Difficulty = models.IntegerField(default = 1, validators=[MinValueValidator(1), MaxValueValidator(40)])

    def __str__(self):
        return f"LV {self.Difficulty}"

class Hard(models.Model):
    Difficulty = models.IntegerField(default = 1, validators=[MinValueValidator(1), MaxValueValidator(40)])

    def __str__(self):
        return f"LV {self.Difficulty}"

class Expert(models.Model):
    Difficulty = models.IntegerField(default = 1, validators=[MinValueValidator(1), MaxValueValidator(40)])

    def __str__(self):
        return f"LV {self.Difficulty}"

class Master(models.Model):
    Difficulty = models.IntegerField(default = 1, validators=[MinValueValidator(1), MaxValueValidator(40)])

    def __str__(self):
        return f"LV {self.Difficulty}"

class Music(models.Model):
    title = models.CharField(max_length = 36)
    # ondelete定義當刪除物件時所使用的方法 https://www.delftstack.com/zh-tw/howto/django/django-on_delete-parameter/
    # null=True 代表空值為NULL, blank=True 代表不為必塡項，可以空著
    #author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True) #ForeignKey (多對一)
    easy = models.ForeignKey('Easy', on_delete=models.SET_NULL, null=True)
    normal = models.ForeignKey('Normal', on_delete=models.SET_NULL, null=True)
    hard = models.ForeignKey('Hard', on_delete=models.SET_NULL, null=True)
    expert = models.ForeignKey('Expert', on_delete=models.SET_NULL, null=True)
    master = models.ForeignKey('Master', on_delete=models.SET_NULL, null=True)
    num = models.IntegerField(default = 999, help_text="Unique ID for its url")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('music_detail', kwargs={"num":self.num})

    class meta:
        ordering = ['num']

'''
class MusicInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular music')
    music = models.ForeignKey('Music', on_delete=models.SET_NULL, null=True)
#    Max_combos = models.IntegerField(default = 1, validators=[MinValueValidator(1), MaxValueValidator(9999)])
#    time = models.IntegerField(default = 1, validators=[MinValueValidator(1), MaxValueValidator(300)])

    def __str__(self):
        return f'{self.id} ({self.music})'

class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    musics = models.ManyToManyField(Music)

    def music_nums(self):
        return [(music.num, music.title) for music in self.musics.all()]
    def music_names(self):
        return ', '.join([music.title for music in self.musics.all()])
    music_names.short_description = 'Music Names'
    def __str__(self):
        return self.user.username + ': ' + self.music_names()
'''

class AccountManage(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
          )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None):
        user = self.create_user(
             email,
             password=password,
          )
        user.is_admin = True
        user.save(using=self._db)
        return user

#繼承django預設user model.
class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    favorite_musics = models.ManyToManyField(Music, blank=True)

    objects = AccountManage()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    def is_staff(self):
        return self.is_staff
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_perms(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return self.is_admin
    def my_musics(self):
        return [music for music in self.favorite_musics.all()]