from django.shortcuts import render
from django.views import View

# Create your views here.
class index(View):
    def get(self, request):
        return render(request, 'user/index.html')

class register(View):
    def get(self, request):
        return render(request, 'user/register.html')
    