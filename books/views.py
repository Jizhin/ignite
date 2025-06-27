from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Book
from .serializers import BookSerializer
from .paginations import CustomPageNumberPagination

class BookListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Book.objects.all().order_by('-download_count').prefetch_related(
            'authors', 'languages', 'subjects', 'bookshelves', 'formats'
        )
        filters = request.query_params

        gutenberg_ids = filters.get('gutenberg_id')
        if gutenberg_ids:
            ids_list = gutenberg_ids.split(',')
            queryset = queryset.filter(gutenberg_id__in=ids_list)

        languages = filters.get('language')
        if languages:
            lang_codes = languages.split(',')
            queryset = queryset.filter(languages__code__iexact__in=lang_codes).distinct()

        mime_types = filters.get('mime_type')
        if mime_types:
            mime_list = mime_types.split(',')
            mime_query = Q()
            for mime_type in mime_list:
                mime_query |= Q(formats__mime_type__icontains=mime_type)
            queryset = queryset.filter(mime_query).distinct()

        topics = filters.get('topic')
        if topics:
            topic_list = topics.split(',')
            topic_query = Q()
            for topic in topic_list:
                topic_query |= Q(subjects__name__icontains=topic) | Q(bookshelves__name__icontains=topic)
            queryset = queryset.filter(topic_query).distinct()

        authors = filters.get('author')
        if authors:
            author_list = authors.split(',')
            author_query = Q()
            for author in author_list:
                author_query |= Q(authors__name__icontains=author)
            queryset = queryset.filter(author_query).distinct()

        titles = filters.get('title')
        if titles:
            title_list = titles.split(',')
            title_query = Q()
            for title in title_list:
                title_query |= Q(title__icontains=title)
            queryset = queryset.filter(title_query).distinct()
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = BookSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)