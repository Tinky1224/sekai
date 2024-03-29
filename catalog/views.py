from django.shortcuts import render, redirect
from django.views import generic
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django_filters.views import FilterView
from django.contrib import messages
from django.urls import reverse

# Create your views here.
from .forms import MusicForm, RegisterForm
from .models import Music, Easy, Normal, Hard, Expert, Master, Account
from .filters import MusicFilter

class MusicListView(FilterView):
    model = Music
    context_name = "Music_list"
    template_name = "catalog/music_list.html"
#    paginate_by = 10
    filterset_class = MusicFilter

'''class MusicListView(generic.ListView):
    model = Music
    context_name = "Music_list"
#    queryset = Music.objects.filter(title__icontains='Tell your world')[:]
    template_name = "catalog/music_list.html"
    paginate_by = 20
    filterset_class = MusicFilter
'''

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
        return Account.objects.get(email=self.request.user.email).favorite_musics.all()

@permission_required('staff_member_required')
def music_create(request):
    if request.method == 'POST':
        form = MusicForm(request.POST)
        if Music.objects.filter(num = request.POST.get('num')):
            messages.info(request, "Failed, the num of music is existed!")
            return redirect('music_detail', request.POST.get('num'))
        if form.is_valid():
            music = form.save()
            messages.info(request, "Add music successful.")
            return redirect('music_detail', music.num)
    else:
        form = MusicForm()
    return render(request, 'catalog/music_create.html', {'form': form})

@login_required
def like_music(request, num):
    if not Music.objects.filter(num=num):
        return redirect(request.GET.get('from', 'music'))
    user = request.user
    if user.favorite_musics.filter(num=num):
        return redirect(request.GET.get('from', 'music'))
    user.favorite_musics.add(Music.objects.get(num=num))
    return redirect(request.GET.get('from', 'music'))
@login_required
def unlike_music(request, num):
    if not Music.objects.filter(num=num):
        return redirect(request.GET.get('from', 'music'))
    user = request.user
    if not user.favorite_musics.filter(num=num):
        return redirect(request.GET.get('from', 'music'))
    user.favorite_musics.remove(Music.objects.get(num=num))
    return redirect(request.GET.get('from', 'music'))

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get('next', 'index'))
    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'catalog/register.html', context=context)
