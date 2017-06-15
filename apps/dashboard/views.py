# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages # access django's `messages` module.
from models import User, Message, Comment # access our models

# Add extra message levels to default messaging to handle login or registration error generation:
# https://docs.djangoproject.com/en/1.11/ref/contrib/messages/#creating-custom-message-levels
LOGIN_ERR = 50 # Messages level for login errors
REG_ERR = 60 # Messages level for registration errors
INDEX_MSG = 70 # Messages level for homepage messages


def index(request):
    """Loads homepage."""

    return render(request, "dashboard/index.html")

def login(request):
    """Loads login page if GET, if POST, logs in a user."""

    # Check if login form submission:
    if request.method == "POST":
        # Prepare login data for validation:
        login_data = {
            "email": request.POST["login_email"],
            "password": request.POST["login_password"],
        }
        validated = User.objects.login(**login_data)
        try:
            # If errors, reload login page with errors:
            if len(validated["errors"]) > 0:
                print "User could not be logged in."
                # Loop through errors and Generate Django Message for each with custom level and tag:
                for error in validated["errors"]:
                    messages.add_message(request, LOGIN_ERR, error, extra_tags="login_errors")
                # Reload login page:
                return redirect("/signin")
        except KeyError:
            # If validation successful, set session, and load dashboard based on user level:
            print "User passed validation..."

            # Set session to validated User:
            print "Setting session data for logged in user..."
            request.session["user_id"] = validated["logged_in_user"].id

            # Check user level (if 0, load normal user dashboard, if 1, load admin dashboard):
            if validated["logged_in_user"].user_level == 0:
                # Redirect to normal user dashboard:
                return redirect("/dashboard")
            elif validated["logged_in_user"].user_level == 1:
                # Redirect to admin dashboard:
                return redirect("/dashboard/admin")

            # Fetch dashboard data and load dashboard page:
            return redirect("/dashboard")
    else:
        # Otherwise, load login page:
        return render(request, "dashboard/login.html")

def register(request):
    """Loads register page if GET, if POST, registers a user."""

    # Check if register form submission:
    if request.method == "POST":
        # Prepare registration data for validation:
        reg_data = {
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
            "email": request.POST["email"],
            "password": request.POST["password"],
            "confirm_pwd": request.POST["confirm_pwd"],
        }
        # Validate registration data:
        validated = User.objects.register(**reg_data) # see `./models.py`, `UserManager.register()`
        # If errors, reload index page with errors:
        try:
            if len(validated["errors"]) > 0:
                print "User could not be registered."
                # Loop through errors and Generate Django Message for each with custom level and tag:
                for error in validated["errors"]:
                    messages.add_message(request, REG_ERR, error, extra_tags="reg_errors")
                # Reload register page:
                return redirect("/register")
        except KeyError:
            # If validation successful, set session and load dashboard based on user level:
            print "User passed validation and has been created..."

            # Set session to validated User:
            print "Setting session data for logged in new user..."
            request.session["user_id"] = validated["logged_in_user"].id

            # Check user level (if 0, load normal user dashboard, if 1, load admin dashboard):
            if validated["logged_in_user"].user_level == 0:
                # Redirect to normal user dashboard:
                return redirect("/dashboard")
            elif validated["logged_in_user"].user_level == 1:
                # Redirect to admin dashboard:
                return redirect("/dashboard/admin")

    else:
        # Otherwise, load registration page:
        return render(request, "dashboard/register.html")


def user_dashboard(request):
    """Loads normal user dashboard."""

    # Check for session before loading dashboard:
    try:
        request.session["user_id"]
        print "User session validated."

        # Get data for normal user dashboard:
        user_data = {
            "logged_in_user": User.objects.get(id=request.session["user_id"]),
            "all_users": User.objects.all().order_by("first_name")
        }

        # Remove password properties from all_users.
        # Note: Because these are normal level users, p/w must be protected:
        for user in user_data["all_users"]:
            # delete password property
            del user.password

        # Load normal user dashboard:
        return render(request, "dashboard/user_dashboard.html", user_data)

    except KeyError:
        # If session object not found, load index:
        print "User session not validated."
        messages.add_message(request, INDEX_MSG, "You must be logged in to view this page.", extra_tags="index_msg")
        return redirect("/")

def admin_dashboard(request):
    """Loads admin dashboard."""

    # Check for session before loading dashboard:
    try:
        request.session["user_id"]
        print "User session validated."

        # Get data for admin user dashboard:
        admin_data = {
            "logged_in_user": User.objects.get(id=request.session["user_id"]),
            "all_users": User.objects.all().order_by("first_name")
        }

        # We will not remove the passwords, as this is the admin account.
        return render(request, "dashboard/admin_dashboard.html", admin_data)

    except KeyError:
        # If session object not found, load index:
        print "User session not validated."
        messages.add_message(request, INDEX_MSG, "You must be logged in to view this page.", extra_tags="index_msg")
        return redirect("/")

def show_user(request, id):
    """If GET, show a user, if POST, send message."""

    # Check if message submission:
    if request.method == "POST":
        # Validate / Create message (errors returned if unsuccessful, else, new message returned):
        # Assemble data:
        message_data = {
            "description": request.POST["description"], # msg description
            "sender_id": request.session["user_id"], # logged in user whom sent msg
            "receiver_id": id, # user whose profile is receiving msg
        }
        validated = Message.objects.add(**message_data)

        # If errors, reload index page with errors:
        try:
            if len(validated["errors"]) > 0:
                print "Message could not be created."
                # Loop through errors and Generate Django Message for each with custom level and tag:
                for error in validated["errors"]:
                    messages.error(request, error, extra_tags="msg_errors")
                # Reload register page:
                return redirect("/users/show/" + id)
        except TypeError:
            # If validation successful, reload show page:
            print "Message passed validation and has been created..."
            return redirect("/users/show/" + id)
    else:
        # GET request, load show user page (assemble data for show template):
        user_data = {
            "show_user": User.objects.get(id=id), # Get user by id (for user profile)
            "logged_in_user": User.objects.get(id=request.session["user_id"]),
            "user_messages": User.objects.get(id=id).messages_received.all().order_by("-created_at"),
        }
        return render(request, "dashboard/show_user.html", user_data)

def edit_user(request, id):
    """If GET, load edit user page, if POST, edit user information."""

    pass

def delete_user(request, id):
    """Delete a user."""

    # Delete user by id:
    User.objects.get(id=id).delete()

    # If current user is admin, redirect to admin dashboard:
    logged_in_user = User.objects.get(id=request.session["user_id"])
    if logged_in_user.user_level == 1:
        return redirect('/dashboard/admin')
    elif logged_in_user.user.level == 0:
        # Otherwise, redirect to normal user dashboard:
        return redirect('/dashboard')

def comment(request, id):
    """Comment on a message."""

    # Prepare data for models:
    comment_data = {
        "description": request.POST["desc" + "_" + str(request.POST["message_id"])],
        "sender_id": request.session["user_id"], # logged in user
        "receiver_id": id, # receipient of message (user whose profile is being viewed)
        "message_id": request.POST["message_id"], # id of message comment belongs to
    }

    # Create / validate new comment:
    validated = Comment.objects.add(**comment_data)

    # If errors, reload user show page with errors:
    try:
        if len(validated["errors"]) > 0:
            print "Comment could not be created."
            # Loop through errors and Generate Django Message for each with custom level and tag:
            for error in validated["errors"]:
                messages.error(request, error, extra_tags="msg_errors")
            # Reload register page:
            return redirect("/users/show/" + id)
    except TypeError:
        # If validation successful, reload show page:
        print "Comment passed validation and has been created..."
        return redirect("/users/show/" + id)



def logout(request):
    """Logs out current user."""

    # Deletes session:
    del request.session['user_id']
    # Adds success message:
    messages.add_message(request, INDEX_MSG, "Successfully logged out.", extra_tags="index_msg")

    # Return to index page:
    return redirect("/")
