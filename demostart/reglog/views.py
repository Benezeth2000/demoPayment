from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
import requests
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCfbubhTk2m5Sp2VJophn6TwloCRfvRHmY",
    "authDomain": "garbage-164ba.firebaseapp.com",
    "databaseURL": "https://garbage-164ba-default-rtdb.firebaseio.com",
    "projectId": "garbage-164ba",
    "storageBucket": "garbage-164ba.appspot.com",
    "messagingSenderId": "406029003743",
    "appId": "1:406029003743:web:49a4775bdbeefa1270b26a",
    "measurementId": "G-24VX9N61HT"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()


def is_internet_available():
    try:
        # Make a request to a reliable server
        response = requests.get('https://www.google.com')
        return response.status_code == 200

    except requests.RequestException:
        return False


def signup_view(request):
    if request.method == 'POST':

        # Check for internet connectivity
        if not is_internet_available():
            error_message = "No internet connection available"
            messages.error(request, error_message)
            return render(request, 'registration.html')

        # Process registration form data
        username = request.POST.get('username')
        # location = request.POST.get('location')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Retrieve the 'users' node from Firebase Realtime Database
            users = db.child("users").get()

            # Check if 'users' variable is not None before iterating
            if users is not None:
                email_taken = any(user.val().get('email') == email for user in users.each())

                if email_taken:
                    error_message = "Email already taken, try another"
                    messages.error(request, error_message)
                    return render(request, 'registration.html')

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                error_message = "Username is already taken, try another"
                return render(request, "registration.html", {'error_message': error_message})

            else:
                # Create a new user in django
                userDjango = User.objects.create_user(username=username, email=email, password=password)

                # Save the user to the database
                userDjango.save()

                # Create the user in Firebase Authentication
                user = auth.create_user_with_email_and_password(
                    email=email,
                    password=password
                )

                # Set custom user claims (e.g., location)
                # auth.set_custom_user_claims(user.uid, {'location': location})

                # Save user data to the Realtime Database
                user_data = {
                    'name': username,
                    'email': email,
                    'password': password
                }

                # Push the user data to the firebase
                db.child("users").push(user_data)

                # Additional logic or actions after successful user creation
                # For example, you can save the user ID to your database or perform other operations

                return redirect('reglog:loginpage')  # Redirect to a success page
        except ValueError as e:
            error_message = str(e)
            # Handle the registration error
            return render(request, 'registration.html', {'error_message': error_message})

    return render(request, 'registration.html')


def login_view(request):
    if request.method == 'POST':

        # Check for internet connectivity
        if not is_internet_available():
            error_message = "No internet connection available"
            messages.error(request, error_message)
            return render(request, 'login.html')

        # Get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            users = db.child("users").get()
            user_found = False

            for user in users.each():
                if user.val().get('email') == username:
                    user_found = True
                    break

            if user_found:
                user = auth.sign_in_with_email_and_password(username, password)
                return redirect('reglog:mainpage')

            else:
                error_message = "Invalid email or password"
                messages.error(request, error_message)

        except Exception as e:
            error_message = str(e)

            # Check if the error message is related to invalid password
            if "INVALID_PASSWORD" in error_message:
                error_message = "Invalid email or password"

            messages.error(request, error_message)

    return render(request, 'login.html')


def main_screen(request):
    return render(request, 'mainpage.html')
# Create your views here.
