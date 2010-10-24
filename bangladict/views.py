from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import get_object_or_404, render_to_response

from .models import Word, Dictionary

def dictionary_list(request):
    return object_list(request, Dictionary.objects.all(),
                       template_object_name='dictionary', paginate_by=10)

def word_list(request, dict_abbrev):
    dictionary = get_object_or_404(Dictionary, abbrev=dict_abbrev)
    words = Word.objects.filter(dictionary=dictionary)
    context = {'dictionary': dictionary}
    return object_list(request, words, template_object_name='word',
                       paginate_by=50, extra_context=context)

def word_comments(request, wid):
    word = get_object_or_404(Word, pk=wid)
    return object_detail(request, Word.objects.all(), wid,
                         template_object_name='word')

def word_detail(request, dict_abbrev, word):
    dictionary = get_object_or_404(Dictionary, abbrev=dict_abbrev)
    words = Word.objects.filter(original=word, dictionary=dictionary)
    context = {'dictionary': dictionary}
    return object_list(request, words, template_object_name='word',
                       extra_context=context)

def word_edit(request, wid=None):
    pass

