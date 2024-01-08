from rest_framework import serializers
from apps.book.models import BookData


class BookSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, )
    auther_name = serializers.CharField()
    release_year = serializers.CharField()
    price = serializers.IntegerField(
        required=True,
        error_messages=""
    )
    membership = serializers.CharField(required=False, allow_null=True)

    def create(self, validated_data):
        """
        Create book instance and update respective response
        :param validated_data:
        :return: book instance
        """
        # save Book instance
        book_instance = BookData.objects.create(
            **validated_data
        )
        return book_instance

    def update(self, instance, validated_data):
        """
        Update book_data obj
        :param instance: book instance
        :param validated_data: post data
        :return: Book_data instance
        """
        instance.title = validated_data.get('name', instance.title)
        instance.description = validated_data.get('auther_name', instance.description)
        instance.save()
        return instance

    class Meta:
        """
        Employee Meta class
        """
        model = BookData
        fields = ('name', 'auther_name', 'release_year', 'membership', 'price',
                  )


class AllBookGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookData
        fields = ('name', 'auther_name', 'release_year', 'membership', 'price',
                  )