from django.shortcuts import render


async def registration(request):
    return render(request, "registration.html", {})


async def login(request):
    return render(request, "login.html", {})


async def email(request):
    return render(request, "email.html", {})


async def password(request):
    return render(request, "password.html", {})


async def account(request):
    return render(request, "account.html", {})


async def profile(request):
    return render(request, "profile.html", {})


async def historyorder(request):
    return render(request, "historyorder.html", {})
