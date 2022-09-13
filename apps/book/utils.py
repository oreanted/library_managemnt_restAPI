from rest_framework.response import Response
from rest_framework import status as rest_status, serializers
# third party imports
from rest_framework.routers import DefaultRouter
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet


def custom_error_response(status, detail, **kwargs):
    """
    function is used for getting same global error response for all api
    :param detail: error message .
    :param status: http status.
    :return: Json response
    """
    if not detail:
        detail = {}
    return Response({"detail": detail}, status=status, **kwargs)


def custom_response(status=rest_status.HTTP_200_OK, detail=None, data=None, **kwargs):
    """
    function is used for getting same global response for all api
    :param detail: success message
    :param data: data
    :param status: http status
    :return: Json response
    """
    return Response({"detail": detail, "data": data}, status=status, **kwargs)


def fun_get_list(list_self):
    """
    To get user list data
    :param list_self: this is self object
    :return: paginated data
    """
    login_user = list_self.request.user
    object_detail = list_self.get_queryset()
    page = list_self.paginate_queryset(object_detail)
    current_page = list_self.paginator.page.number
    error = None
    data = None
    if not page:
        error = custom_error_response(status=rest_status.HTTP_204_NO_CONTENT, detail=None)
    else:
        list_data = list_self.serializer_class(page, many=True, context={'user': login_user}).data
        data = list_self.paginator.get_paginated_response(list_data).data
        data['current_page'] = current_page
    return error, data


def custom_list_response(status, detail, data=None, **kwargs):
    """
    function is used for getting same global response for all api
    :param detail: success message
    :param data: data
    :param status: http status
    :return: Json response
    """
    if data:
        data['records_per_page'] = len(data['results'])
        data['page_limit'] = 20
    return Response({"data": data, "detail": detail}, status=status, **kwargs)


class CreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return custom_response(status=status.HTTP_201_CREATED, detail=None, data=serializer.data, headers=headers)
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=list(serializer.errors.values())[0][0])

    @staticmethod
    def get_success_headers(data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return custom_response(status=status.HTTP_200_OK, detail=None, data=serializer.data)


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return custom_response(status=status.HTTP_200_OK, detail=None, data=serializer.data)


class UpdateModelMixin:
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=False):
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return custom_response(status=status.HTTP_200_OK, detail=None, data=serializer.data)
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=list(serializer.errors.values())[0][0])

    @staticmethod
    def perform_update(serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return custom_response(status=status.HTTP_204_NO_CONTENT, detail=None, data=None)


class CustomModelViewSet(CreateModelMixin,
                         RetrieveModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin,
                         ListModelMixin,
                         GenericViewSet):
    """
    A view-set that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions, and provide a unique response format .
    """
    pass


class CustomModelListViewSet(ListModelMixin, GenericViewSet):
    """
    To get only list
    """
    pass


"""
 Custom routers for job sourcing .
"""


class OptionalSlashRouter(DefaultRouter):
    """
    optional slash router class
    """

    def __init__(self):
        """
            explicitly appending '/' in urls if '/' doesn't exists for making common url patterns .
        """
        super(OptionalSlashRouter, self).__init__()
        self.trailing_slash = '/?'
