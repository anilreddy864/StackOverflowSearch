from datetime import datetime, timedelta
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from .StackoverflowAPI import get_questions, dateConverter
from .forms import SearchForm
import pytz

PER_MIN_SEARCHES = 2
PER_DAY_SEARCHES = 100
SESSION_MINUTES = 1
SESSION_DAY_MINUTES = 24 * 60
RESULTS_PER_PAGE = 10


def delete_session(request):
    try:
        del request.session['search-questions-post']
        del request.session['start-time']
        del request.session['count']
        cache.clear()
        cache.close()
    except KeyError:
        pass
    return redirect('/')


def home(request):
    try:
        del request.session['search-questions-post']
    except KeyError:
        pass
    return redirect('/')


def clear_cache(request):
    try:
        del request.session['search-questions-post']
        cache.clear()
        cache.close()
    except KeyError:
        pass
    return redirect('/')


def detail(request):
    params = {}
    output = {}
    global cache_key, cache_key_out
    start_time = None
    if not request.method == 'POST':
        if 'search-questions-post' in request.session:
            request.POST = request.session['search-questions-post']
            request.method = 'POST'
    if 'start-time' in request.session:
        start_time = request.session['start-time']
    if start_time is None:
        request.session['start-time'] = datetime.now(pytz.timezone('Asia/Calcutta')).strftime("%d %B %Y, %H:%M:%S:%f")
    request.session['search-questions-post'] = request.POST
    session_time_obj = datetime.strptime(request.session['start-time'], "%d %B %Y, %H:%M:%S:%f")

    # Getting the session time frame and current time
    per_min_obj = session_time_obj + timedelta(minutes=SESSION_MINUTES)
    per_day_obj = session_time_obj + timedelta(minutes=SESSION_DAY_MINUTES)
    current_time = datetime.strptime(datetime.now(pytz.timezone('Asia/Calcutta')).strftime("%d %B %Y, %H:%M:%S:%f"),
                                     "%d %B %Y, %H:%M:%S:%f")
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            params['page'] = form.cleaned_data['page']
            params['pagesize'] = form.cleaned_data['pagesize']
            params['from_date'] = dateConverter(form.cleaned_data['from_date'])
            params['to_date'] = dateConverter(form.cleaned_data['to_date'])
            params['order'] = form.cleaned_data['order']
            params['min'] = dateConverter(form.cleaned_data['min'])
            params['max'] = dateConverter(form.cleaned_data['max'])
            params['sort'] = form.cleaned_data['sort']
            params['q'] = form.cleaned_data['q']
            params['accepted'] = form.cleaned_data['accepted']
            params['answers'] = form.cleaned_data['answers']
            params['body'] = form.cleaned_data['body']
            params['closed'] = form.cleaned_data['closed']
            params['migrated'] = form.cleaned_data['migrated']
            params['notice'] = form.cleaned_data['notice']
            params['nottagged'] = form.cleaned_data['nottagged']
            params['tagged'] = form.cleaned_data['tagged']
            params['title'] = form.cleaned_data['title']
            params['user'] = form.cleaned_data['user']
            params['url'] = form.cleaned_data['url']
            params['views'] = form.cleaned_data['views']
            params['wiki'] = form.cleaned_data['wiki']
            params = {k: v for k, v in params.items() if v != '' and v is not None}

            if 'count' not in request.session:
                request.session['count'] = 0
            # Setting Cache Keys
            if not cache.get("keys"):
                cache.set("keys", [], None)
                cache_key = 1
                cache_key_out = str(cache_key) + '_out'
                output = get_questions(params)
                add_key_to_list(cache_key, cache_key_out, params, output)
                request.session['count'] = 1
                print('API Call', request.session['count'])
            else:
                # Checking Cache for Output for that Session
                for key in cache.get('keys'):
                    if params == cache.get(key):
                        output = cache.get(str(key) + '_out')
                        print('Getting Output From Cache')
                        break
            # If Output is not in Cache
            cache_key = max(cache.get('keys'))
            if output is None or output == {}:
                request.session['count'] = request.session['count'] + 1
                if current_time < per_min_obj:
                    if request.session['count'] > PER_MIN_SEARCHES:
                        log_msg = 'Only ' + str(PER_MIN_SEARCHES) + ' Searches are allowed per Minute Per Session'
                        form = SearchForm()
                        return render(request, 'form.html', {'form': form, 'msg': log_msg})
                if current_time < per_day_obj:
                    if request.session['count'] > PER_DAY_SEARCHES:
                        log_msg = 'Only ' + str(PER_DAY_SEARCHES) + ' Searches are allowed per Day Per Session'
                        form = SearchForm()
                        return render(request, 'form.html', {'form': form, 'msg': log_msg})
                output = get_questions(params)
                print('API Call', request.session['count'])
                cache_key = cache_key + 1
                cache_key_out = str(cache_key) + '_out'
                add_key_to_list(cache_key, cache_key_out, params, output)

            # If errors from API
            if 'error_id' in output.keys():
                log_msg = output['error_message']
                form = SearchForm()
                return render(request, 'form.html', {'form': form, 'msg': log_msg})
            if output == {}:
                log_msg = 'No Data Found for Query Combination'
                form = SearchForm()
                return render(request, 'form.html', {'form': form, 'msg': log_msg})

            # Pagination
            t = tuple(output.items())
            paginator = Paginator(t, RESULTS_PER_PAGE)
            page_number = request.GET.get('page')
            try:
                page_obj = paginator.page(page_number)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            session_time = request.session['start-time']
            message = 'Session Started At ' + session_time
            return render(request, 'Detail.html', {'output': page_obj, 'message': message})
        else:
            form = SearchForm()
    return render(request, 'form.html', {'form': form})


def add_key_to_list(cache_key, cache_key_out, params, output):
    cache.set(cache_key, params, None)
    cache.set(cache_key_out, output, None)
    if cache_key not in cache.get("keys"):
        keys_list = cache.get("keys")
        keys_list.append(cache_key)
        cache.set("keys", keys_list, None)
