from django.shortcuts import render


class HomeView(View):
    template = 'home.html'

    def get(self, request):

            template_vals = {
            'encrypted': "Yo, I'm encrypted"
            }


            return render(request, self.template, template_vals)

        return response

