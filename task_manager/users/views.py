from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm


class UsersIndexView(ListView):

    model = User
    template_name = 'users/index.html'


class UsersCreateFormView(View):
    __template = 'users/create.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, self.__template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.__template, {'form': form})

# def login(request):
#     m = Member.objects.get(username=request.POST["username"])
#     if m.check_password(request.POST["password"]):
#         request.session["member_id"] = m.id
#         return HttpResponse("You're logged in.")
#     else:
#         return HttpResponse("Your username and password didn't match.")

# def logout(request):
#     try:
#         del request.session["member_id"]
#     except KeyError:
#         pass
#     return HttpResponse("You're logged out.")


# class UsersUpdateFormView(View):

#     def get(self, request, *args, **kwargs):
#         user_id = kwargs.get('pk')
#         user = User.objects.get(id=user_id)
#         form = UsersForm(instance=user)
#         return render(
#             request,
#             'users_update.html',
#             {'form': form, 'pk': user_id}
#         )

#     def post(self, request, *args, **kwargs):
#         user_id = kwargs.get('pk')
#         user = User.objects.get(id=user_id)
#         form = UsersForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('users_index')
#         return render(
#             request,
#             'users_update.html',
#             {'form': form, 'pk': user_id}
#         )


# class ArticleDeleteFormView(View):

#     def post(self, request, *args, **kwargs):
#         user_id = kwargs.get('pk')
#         user = User.objects.get(id=user_id)
#         if user:
#             user.delete()
#         return redirect('articles_index')
