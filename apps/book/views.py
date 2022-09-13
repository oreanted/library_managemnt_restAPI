from rest_framework import status
from rest_framework.filters import SearchFilter

from apps.book.utils import custom_response, custom_error_response, fun_get_list, custom_list_response
from apps.book.utils import CustomModelViewSet
from apps.book.serializers import BookSerializer, AllBookGetSerializer
from apps.book.models import BookData


# Create your views here.
class EmployeeViewSet(CustomModelViewSet):
    """
    This photo view-set is used for upload photo
    Note - this api is form data api so check this api only postman
    """
    serializer_class = BookSerializer
    http_method_names = ('post', 'get', 'delete', 'put',)
    queryset = BookData
    filter_backends = (SearchFilter,)
    search_fields = ['name', ]

    def create(self, request, *args, **kwargs):
        """
        To add Employee Data -
        Note - this api is form data api so check this api only postman
        :param request: wsgi request
        :param args: None
        :param kwargs: None
        :return: success message or error
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return success response
            response = custom_response(
                status=status.HTTP_201_CREATED, detail=None,
                data=None
            )
            return response
        return custom_error_response(
            status=status.HTTP_400_BAD_REQUEST, detail=serializer.errors
        )

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        """
        queryset = (
            self.queryset.objects.filter(
            ).order_by('name')
        )
        employee_list = self.filter_queryset(queryset)
        return employee_list

    def list(self, request, *args, **kwargs):
        """
        List of Video instance
        :param request: wsgi request
        :param args: argument list
        :param kwargs: keyword argument object
        :return: success message or error
        """
        self.serializer_class = AllBookGetSerializer
        error, employee_obj = fun_get_list(self)
        # check is any error for employee_obj
        if error is not None:
            return error
        return custom_list_response(status=status.HTTP_200_OK, detail=None, data=employee_obj)

    def update(self, request, *args, **kwargs):
        """
        To update video data
        Note - this api is form data api so check this api only postman
        :param request: wsgi request put
        :param args: video id
        :param kwargs: None
        :return: success message or error
        """
        instance = self.get_object()
        serializer = AllBookGetSerializer(data=request.data)
        if serializer.is_valid() and instance:
            serializer.update(instance, request.data)
            # return success response
            response = custom_response(
                status=status.HTTP_200_OK, detail=None,
                data=None
            )
            return response
        return custom_error_response(
            status=status.HTTP_400_BAD_REQUEST, detail=serializer.errors
        )

    def destroy(self, request, *args, **kwargs):
        """
        To delete video
        :param request: wsgi request
        :param args: allows for any number of optional positional arguments (parameters), which will be assigned to a
        tuple named args
        :param kwargs: video id required
        :return: Json Response
        """
        main_video_obj = self.get_object()
        if main_video_obj:
            # Deleting a video also from feed
            main_video_obj.delete()
            return custom_response(
                status=status.HTTP_200_OK, detail=None, data="delete successfully delete  "
            )
        return custom_error_response(
            status=status.HTTP_400_BAD_REQUEST, detail="Book_id is Invalid"
        )
    