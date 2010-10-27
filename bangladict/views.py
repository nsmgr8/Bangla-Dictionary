#
# Copyright 2010 BengDict Project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging

from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

from .models import Word, Dictionary, WordLoad
from .forms import WordForm

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

@csrf_protect
@login_required
def word_edit(request, dict_abbrev, wid=None):
    dictionary = get_object_or_404(Dictionary, abbrev=dict_abbrev)
    if wid:
        word = get_object_or_404(Word, pk=wid)
        if not request.user.is_staff:
            if request.user != word.contributor:
                raise Http404('Not the contributor')
    else:
        word = None

    if request.method == 'POST':
        form = WordForm(data=request.POST, instance=word)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.dictionary = dictionary
            entity.contributor = request.user
            entity.save()
            if not word:
                contrib = request.user.get_or_create_profile()
                contrib.number_words += 1
                contrib.save()
            return HttpResponseRedirect(reverse('dict_word_comments',
                                                args=[entity.pk]))
    else:
        form = WordForm(instance=word)

    context = {'form': form, 'dictionary': dictionary, 'word': word}

    return render_to_response('bangladict/word_edit.html', context,
                              RequestContext(request))

@csrf_protect
@login_required
def bulk_load(request):
    if request.method == 'POST':
        f = request.FILES.get('file', None)
        if f:
            loads = WordLoad.objects.filter(contributor=request.user)
            current = f.read()
            loaded = False
            for f in loads:
                if f.file == current:
                    loaded = True
                    break
            if not loaded:
                WordLoad(file=current, contributor=request.user).save()

    context = {}

    return render_to_response('bangladict/bulk_load.html', context,
                              RequestContext(request))

