from django.http import JsonResponse
from django.shortcuts import render
from book_server.models import get_story_list_by_category, get_story_detail_by_id


def book_list(request):
    genre = request.GET.get('genre')
    books = list(get_story_list_by_category(genre))
    for book in books:
        del book['_id']
    return JsonResponse(books, safe=False)


def book_detail(request):
    object_id = request.GET.get('objectId')
    book = get_story_detail_by_id(object_id)
    del book['_id']
    return JsonResponse(book)

def app_state(request):
    version = request.GET.get('version', '1.0')
    if version == '1.0':
        return JsonResponse({'in_review': True})
    else:
        return JsonResponse({'in_review': False})
