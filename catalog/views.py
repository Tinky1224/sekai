from django.shortcuts import render, redirect
from django.views import generic
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django_filters.views import FilterView
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from .forms import MusicForm, RegisterForm
from .models import Music, Easy, Normal, Hard, Expert, Master, Account#, Person
from .filters import MusicFilter

class MusicListView(FilterView):
    model = Music
    context_name = "Music_list"
#    queryset = Music.objects.filter(title__icontains='Tell your world')[:]
    template_name = "catalog/music_list.html"
    paginate_by = 10
    filterset_class = MusicFilter

'''class MusicListView(generic.ListView):
    model = Music
    context_name = "Music_list"
#    queryset = Music.objects.filter(title__icontains='Tell your world')[:]
    template_name = "catalog/music_list.html"
    paginate_by = 20
    filterset_class = MusicFilter
'''
class MusicListView_filter(generic.ListView):
    model = Music
    context_name = "Music_list"
#    queryset = Music.objects.filter(title__icontains='Tell your world')[:]
    template_name = "catalog/music_list.html"
    paginate_by = 20

class MusicDetailView(generic.DetailView):
    model = Music
    def get_object(self, queryset = None):
        return Music.objects.get(num = self.kwargs.get('num'))
#    template_name = "catalog/music_detail.html"
#    queryset = Music.objects.get(pk=self.kwargs['num'])
    
def index(request):
    music_count = Music.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    context = {
        "music_count" : music_count,
        "num_visits" : num_visits,
    }

    return render(request, 'index.html', context=context)

def music_detail_view(request, primary_key):
    try:
        music = Music.objects.get(num=primary_key)
    except Music.DoesNotExist:
        raise Http404('Music does not exist!')
    return render(request, 'catalog/music_detail.html', context={'music':music})


class user_love_song_view(LoginRequiredMixin,generic.ListView):
    model = Account
    template_name = 'catalog/user_love_musics.html'
#    paginate_by = 10

    def get_queryset(self):
        return Account.objects.filter(email=self.request.user.email)

@permission_required('staff_member_required')
def music_create(request):
    if request.method == 'POST':
        form = MusicForm(request.POST)
        if Music.objects.get(num = request.POST.get('num')):
            return redirect('music_detail', request.POST.get('num'))
        if form.is_valid():
            music = form.save()
            return redirect('music_detail', music.num)
    else:
        form = MusicForm()
    return render(request, 'catalog/music_create.html', {'form': form})

def like_music(request, num):
    music = Music.objects.get(num=num)
    user = request.user
    user.favorite_musics.add(music)
    return redirect(request.GET.get('from', 'music'))

def unlike_music(request, num):
    music = Music.objects.get(num=num)
    user = request.user
    user.favorite_musics.remove(music)
    return redirect(request.GET.get('from', 'music'))

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'catalog/register.html', context=context)
