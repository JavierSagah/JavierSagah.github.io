from django.shortcuts import render
from Poker_app.CommandHandler import CommandHandler
from django.views import View
from Poker_app.models import Account


# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        command_handler = CommandHandler()
        command_input = request.POST["command"]
        username = request.POST["username"]
        response = command_handler.command(command_input, username)
        user = Account.objects.filter(username=username)
        if user:
            user = user[0]
        return render(request, 'index.html', {"message": response, "user": user})