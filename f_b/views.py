from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def topics(request):
    #Show all topics
    topics =  Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'topics.html', context)

@login_required
def topic(request, topic_id):
    #Show a single topic and all its entries
    topic = get_object_or_404(Topic, id=topic_id)
    #Make sure the topic belong to current user
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'topic.html', context)


@login_required
def new_topic(request):
    #Add a new topic.
    if request.method != 'POST':
        #No data submitted; creat a blank form.
        form = TopicForm()
    else:
        #POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('f_b:topics')
    #Display a blank or invalid form.
    context = {'form':form}
    return render(request, 'new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    #Add a new entry for a particular topic.
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        #No data submitted; creat a blank form.
        form = EntryForm()
    else:
        #POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('f_b:topic', topic_id=topic_id)
    #Display a blank or invalid form.
    context = {'topic':topic, 'form':form}
    return render(request, 'new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    #Edit existing entry.
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        #Pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        #POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('f_b:topic', topic_id=topic.id)
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'edit_entry.html', context)
