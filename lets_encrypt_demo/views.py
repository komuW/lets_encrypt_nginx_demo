from django.shortcuts import render
from django.views.generic.base import View


class HomeView(View):
    template = 'home.html'

    def get(self, request):

        template_vals = {
        'encrypted': "Yo, I'm not encrypted"
        }


        return render(request, self.template, template_vals)

