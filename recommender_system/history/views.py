from django.http import JsonResponse

def test(request):
    return JsonResponse({"message": "Intake app is working"})
