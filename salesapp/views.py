from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def homepage(request):
    return render(request, "homepage.html")


def login_page(request):
    """Simple login view: shows a form (GET) and authenticates (POST).

    On successful auth, logs the user in and redirects to the homepage.
    On failure, adds a message and re-renders the form.
    """
    if request.method == "POST":
        # Strip whitespace to avoid accidental leading/trailing spaces
        username = (request.POST.get("username") or "").strip()
        password = (request.POST.get("password") or "")

        # Try normal authentication first
        user = authenticate(request, username=username, password=password)

        # If authentication failed, try to allow login using email (user typed email)
        if user is None:
            # If the user entered an email address, try to find the associated username
            try:
                if "@" in username:
                    user_by_email = User.objects.filter(email__iexact=username).first()
                    if user_by_email:
                        user = authenticate(request, username=user_by_email.username, password=password)
            except Exception as e:
                # Keep exceptions from breaking the login flow; log to console for debugging
                print("login_page: email lookup error:", e)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            # Redirect to next param if provided, otherwise homepage
            next_url = request.GET.get("next") or request.POST.get("next") or "/"
            return redirect(next_url)
        else:
            # Helpful debug hint in server console (no passwords logged)
            try:
                exists = User.objects.filter(username__iexact=username).exists() or User.objects.filter(email__iexact=username).exists()
                print(f"login_page: failed login attempt for '{username}' (user exists: {exists})")
            except Exception:
                print("login_page: failed login attempt, couldn't check user existence")
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


@login_required(login_url='/login/')
def user_list_view(request):
    """Protected view that shows all User records in a simple table.

    Redirects to login if not authenticated (login_required decorator).
    """
    users = User.objects.all().order_by('date_joined')
    return render(request, 'user_list.html', {'users': users})
