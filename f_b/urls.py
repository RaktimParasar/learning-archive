from django.urls import path
from . import views
app_name = 'f_b'
urlpatterns = [
    #Homepage
    path('', views.index, name='index'),
    #Topicpage
    path('topics', views.topics, name='topics'),
    #Detail_Single_Topicpage
    path('topics/<int:topic_id>', views.topic, name='topic'),
    #New_Topicpage
    path('new_topic', views.new_topic, name='new_topic'),
    #Adding new enrty
    path('new_entry/<int:topic_id>', views.new_entry, name='new_entry'),
    #Editing entry
    path('edit_entry/<int:entry_id>', views.edit_entry, name='edit_entry'),
]