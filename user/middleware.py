from .models import MiddleWareModel


class UserMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        print("one time  Intialization")

    def __call__(self, request):
        print("this is  before view")
        response = self.get_response(request)
        print("this is  after view")
        url = request.build_absolute_uri()
        method = request.method
        obj, created = MiddleWareModel.objects.get_or_create(
            method=method, url=url
        )
        method_id = obj.id
        if not created:
            data_count = obj.count + 1
            res = MiddleWareModel.objects.get(id=method_id)
            res.count = data_count
            res.save()
        return response
