from rest_framework import serializers
from .models import Book , Author , Bookshelf , Subject , Language , Format
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name' , 'birth_year' , 'death_year']
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['code']
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']
class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookshelf
        fields = ['name']
class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ['mime_type' , 'url']
class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True , read_only=True)
    languages = LanguageSerializer(many=True , read_only=True)
    subjects = SubjectSerializer(many=True , read_only=True)
    bookshelves = BookshelfSerializer(many=True , read_only=True)
    download_links = FormatSerializer(source='formats' , many=True , read_only=True)
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',
            'download_count',
            'gutenberg_id',
            'title' ,
            'authors' ,
            'genres' ,
            'languages' ,
            'subjects' ,
            'bookshelves' ,
            'download_links'
        ]

    def get_genres(self , obj):
        genres_list = set()
        for subject in obj.subjects.all():
            genres_list.add(subject.name)
        for bookshelf in obj.bookshelves.all():
            genres_list.add(bookshelf.name)
        return list(genres_list)