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

import hashlib
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
from django.db.utils import DatabaseError

from google.appengine.ext import deferred
from google.appengine.runtime import DeadlineExceededError

from .models import Word, Dictionary, WordLoad, NEW, ACCEPTED, REJECTED
from .forms import WordForm

def dictionary_list(request):
    return object_list(request, Dictionary.objects.all(),
                       template_object_name='dictionary', paginate_by=10)

def word_list(request, dict_abbrev, alpha=None, status='accepted'):
    status = {'new': NEW, 'accepted': ACCEPTED, 'rejected': REJECTED}[status]
    if status == NEW and not request.user.is_authenticated():
        raise Http404
    if status == REJECTED and not request.user.is_staff:
        raise Http404

    dictionary = get_object_or_404(Dictionary, abbrev=dict_abbrev)
    words = Word.objects.filter(dictionary=dictionary,
                                status=status).order_by('original')

    if alpha:
        words = words.filter(alpha=alpha)

    context = {
        'dictionary': dictionary,
        'alphabets': [a.strip() for a in dictionary.alphabets.split() if
                      a.strip()]
    }
    return object_list(request, words, template_object_name='word',
                       paginate_by=50, extra_context=context)

@login_required
def word_comments(request, wid):
    word = get_object_or_404(Word, pk=wid)
    return render_to_response('bangladict/word_detail.html', {'word': word},
                              RequestContext(request))

def word_detail(request, dict_abbrev, word):
    dictionary = get_object_or_404(Dictionary, abbrev=dict_abbrev)
    words = Word.objects.filter(original=word, dictionary=dictionary)
    context = {'dictionary': dictionary}
    return object_list(request, words, template_object_name='word',
                       extra_context=context)

def word_search(request):
    abbrev = request.GET.get('dict', None)
    word = request.GET.get('word', None)
    if not all([abbrev, word]):
        raise Http404

    return HttpResponseRedirect(reverse('dict_word_detail', args=[abbrev,
                                                                  word]))

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
            entity.alpha = entity.original[0]
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

@login_required
def word_accept(request, wid, status):
    if not request.user.is_staff:
        raise Http404

    word = get_object_or_404(Word, pk=wid)
    current_status = {'accept': ACCEPTED, 'reject': REJECTED}[status]
    previous_status = word.status
    word.status = current_status
    word.save()

    profile = word.contributor.get_or_create_profile()
    if current_status == ACCEPTED:
        profile.number_accepted += 1
        profile.save()
    elif current_status == REJECTED and previous_status == ACCEPTED:
        profile.number_accepted -= 1
        profile.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@csrf_protect
@login_required
def bulk_load(request):
    context = None
    if request.method == 'POST':
        f = request.FILES.get('file', None)
        if f:
            current = f.read()
            try:
                j = json.loads(current)
                hash = hashlib.sha1(current).hexdigest()

                if WordLoad.objects.filter(hash=hash).count() > 0:
                    msg = _('Already uploaded this file')
                else:
                    wfile = WordLoad(file=current, contributor=request.user,
                                     hash=hash)
                    wfile.save()
                    deferred.defer(add_words_from_file, wfile.pk)
                    msg = _('Thanks for the input. It will be added to the database soon')
            except Exception, e:
                logging.info(e)
                msg = _('Could not save this file.')
        else:
            msg = _('No file uploaded. Please select a file to upload')

        context = {'load_message': msg}

    return render_to_response('bangladict/bulk_load.html', context,
                              RequestContext(request))

def add_words_from_file(fid, index=0):
    logging.info("updating: %d %d" % (fid, index))
    wfile = WordLoad.objects.get(pk=fid)
    dicts = Dictionary.objects.all()
    dictionaries = {}
    for d in dicts:
        dictionaries[d.abbrev] = d

    profile = wfile.contributor.get_or_create_profile()

    try:
        word_file = json.loads(wfile.file)
        if index >= len(word_file):
            return

        counter = index
        for words in word_file[index:]:
            model = words.get('model', None)
            if not model or model != 'bangladict.word':
                continue
            fields = words.get('fields', None)
            if not fields:
                continue
            dictionary = dictionaries[fields['dictionary']]
            word = Word(dictionary=dictionary, contributor=wfile.contributor,
                        alpha=fields['original'][0],
                        original=fields['original'],
                        translation=fields['translation'],
                        phoneme=fields['phoneme'], pos=fields['pos'],
                        synonyms=fields['synonyms'],
                        antonyms=fields['antonyms'],
                        description=fields['description'])
            word.save()
            counter += 1
    except DeadlineExceededError:
        logging.info('DeadlineExceededError')
        deferred.defer(add_words_from_file, fid, counter)
    except DatabaseError:
        logging.info('DatabaseError')
        deferred.defer(add_words_from_file, fid, counter+1)
    except Exception, e:
        logging.warning(e)
        logging.info('%s %d' % wfile.contributor.username, wfile.pk)

    profile.number_words += counter - index
    profile.save()

    logging.info(counter)

