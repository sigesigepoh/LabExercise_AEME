from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def homepage(request):
    return render(request, "homepage.html")


def login_page(request):
    """Simple login view: shows a form (GET) and authenticates (POST).

    On successful auth, logs the user in and redirects to the homepage.
    On failure, adds a message and re-renders the form.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            # Redirect to next param if provided, otherwise homepage
            next_url = request.GET.get("next") or request.POST.get("next") or "/"
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("/")


def about_page(request):
    return render(request, "about.html")


def contact_page(request):
    return render(request, "contact.html")
