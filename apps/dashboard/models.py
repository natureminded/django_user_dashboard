# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re # regex for email validation
import bcrypt # bcrypt for password encryption/decryption

class UserManager(models.Manager):
    """Additional instance method functions for `User`"""

    def register(self, **kwargs):
        """
        Validates and registers a new user.

        Parameters:
        - `self` - Instance to whom this method belongs.
        - `**kwargs` - Dictionary object of registration values from controller to be validated.

        Validations:
        - First Name / Last Name - Required; No fewer than 2 characters; letters only
        - Email - Required, Valid Format, Not Taken
        - Password - Required; Min 8 char, Matches Password Confirmation
        """

        # Create empty errors list, which we'll return to generate django messages back in our controller:
        errors = []

        #---------------------------#
        #-- FIRST_NAME/LAST_NAME: --#
        #---------------------------#
        # Check if first_name or last_name is less than 2 characters:
        if len(kwargs["first_name"]) < 2 or len(kwargs["last_name"]) < 2:
            errors.append('First and last name are required must be at least 2 characters.')

        # Check if first_name or last_name contains letters only:
        alphachar_regex = re.compile(r'^[a-zA-Z]*$') # Create regex object
        # Test first_name and last_name against regex object:
        if not alphachar_regex.match(kwargs["first_name"]) or not alphachar_regex.match(kwargs["last_name"]):
            errors.append('First and last name must be letters only.')

        #------------#
        #-- EMAIL: --#
        #------------#
        # Check if email field is empty:
        if len(kwargs["email"]) < 5:
            errors.append('Email field is required.')

        # Else if email is greater than 5 characters:
        else:
            # Check if email is in valid format (using regex):
            email_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
            if not email_regex.match(kwargs["email"]):
                errors.append('Email format is invalid.')
            else:
                #---------------#
                #-- EXISTING: --#
                #---------------#
                # Check for existing User via email:
                if len(User.objects.filter(email=kwargs["email"])) > 0:
                    errors.append('Email address already registered.')

        #---------------#
        #-- PASSWORD: --#
        #---------------#
        # Check if password is less than 8 characters:
        if len(kwargs["password"]) < 8:
            errors.append('Password fields are required and must be at least 8 characters.')
        else:
            # Check if password matches confirmation password:
            if kwargs["password"] != kwargs["confirm_pwd"]:
                errors.append('Password and confirmation password must match.')

        # Check for validation errors:
        # If none, hash password, create user and send new user back:
        if len(errors) == 0:
            print "Registration data passed validation...hashing password..."
            kwargs["password"] = bcrypt.hashpw(kwargs["password"].encode(), bcrypt.gensalt(14))
            print "Creating new user with data..."
            # Create new validated User:
            validated_user = {
                "logged_in_user": User(first_name=kwargs["first_name"], last_name=kwargs["last_name"], email=kwargs["email"], password=kwargs["password"])
            }
            # Save new User:
            validated_user["logged_in_user"].save()
            print "New `User` created:"
            print "{} {} | {} | {}".format(validated_user["logged_in_user"].first_name,validated_user["logged_in_user"].last_name, validated_user["logged_in_user"].email, validated_user["logged_in_user"].created_at)
            print "Logging user in..."
            # Return created User:
            return validated_user
        else:
            # Else, if validation fails, print errors to console and return errors object:
            print "Errors validating User registration."
            for error in errors:
                print "Validation Error: ", error
            # Prepare data for controller:
            errors = {
                "errors": errors,
            }
            return errors

    def login(self, **kwargs):
        """
        Validates and logs in a new user.

        Parameters:
        - `self` - Instance to whom this method belongs.
        - `**kwargs` - Dictionary object of login values from controller.

        Validations:
        - All fields required.
        - Existing User is found.
        - Password matches User's stored password.
        """

        # Create empty errors list:
        errors = []

        #------------------#
        #--- ALL FIELDS ---#
        #------------------#
        # Check that all fields are required:
        if len(kwargs["email"]) < 5 or len(kwargs["password"]) < 8:
            errors.append('All fields are required.')
        else:
            #------------------#
            #---- EXISTING ----#
            #------------------#
            # Look for existing User to login:
            try:
                logged_in_user = User.objects.get(email=kwargs["email"])
                print "User found..."

                #------------------#
                #---- PASSWORD ----#
                #------------------#
                # Compare passwords with bcrypt:
                # Notes: We pass in our `kwargs['password']` chained to the `str.encode()` method so it's ready for bcrypt.
                try:
                    # If password is incorrect:
                    if bcrypt.hashpw(kwargs["password"].encode(), logged_in_user.password.encode()) != logged_in_user.password:
                        errors.append('Login invalid.')
                except ValueError:
                    # If user's stored password is unable to be used by bcrypt (meaning the created user's p/w was never hashed):
                    errors.append('This user is corrupt. Please contact the administrator.')

            # If existing User is not found:
            except User.DoesNotExist:
                print "Error, User has not been found."
                errors.append('Login invalid.')

        # If no validation errors, return logged in user:
        if len(errors) == 0:
            print "Login data passed validation...logging in..."
            # Prepare data for controller:
            validated_user = {
                "logged_in_user": logged_in_user,
            }
            # Send back validated logged in User:
            return validated_user
        # Else, if validation fails print errors and return errors to controller:
        else:
            print "Errors validating User login."
            for error in errors:
                print "Validation Error: ", error
            # Prepare data for controller:
            errors = {
                "errors": errors,
            }
            return errors

    def admin_add(self, **kwargs):
        """
        Creates a new User by an Administrator.

        Parameters:
        - `self` - Instance to whom this method belongs.
        - `**kwargs` - Dictionary object of new user values from controller.

        Validations:
        - First Name / Last Name - Required; No fewer than 2 characters; letters only
        - Email - Required, Valid Format, Not Taken
        - Password - Required; Min 8 char, Matches Password Confirmation
        """

        pass

    def update_info(self, **kwargs):
        """
        Updates a User's information.

        Parameters:
        - `self` - Instance to whom this method belongs.
        - `**kwargs` - Dictionary object of updated information from controller.

        Validations:
        - First Name / Last Name - Required; No fewer than 2 characters; letters only
        - Email - Required, Valid Format, Not Taken
        """

        # Retreive user by ID
        # Validate information
        # Update Information if passes
        # Otherwise send back errors

        pass

    def update_password(self, **kwargs):
        """
        Updates a User's password.

        Parameters:
        - `self` - Instance to whom this method belongs.
        - `**kwargs` - Dictionary object containing new password from controller.

        Validations:
        - Password - Required; Min 8 char, Matches Password Confirmation
        """

        # Retrieve user by ID
        # Validate password / confirm pass
        # Update information if passes
        # Otherwise send back errors

        pass

class MessageManager(models.Manager):
    """Additional instance method functions for `Message`"""

    def add(self, **kwargs):
        """
        Validates and creates new message.

        Parameters:
        - `**kwargs` - Dictionary list of message to be created.
        """

        errors = []

        # Check if field is empty:
        if len(kwargs["description"]) < 1:
            errors.append("Message description required.")
            errors = {
                "errors" : errors,
            }
            print errors["errors"]
            return errors

        # Create new message with sender and receiver:
        new_message = Message(description=kwargs["description"], sender=User.objects.get(id=kwargs["sender_id"]), receiver=User.objects.get(id=kwargs["receiver_id"]))
        new_message.save()
        return new_message


class CommentManager(models.Manager):
    """Additional instance method functions for `Comment`"""

    def add(self, **kwargs):
        """
        Add a new comment

        Parameters:
        - `**kwargs` - Dictionary list of comment to be created.
        """

        errors = []

        # Check if comment is empty:
        if len(kwargs["description"]) < 1:
            errors.append("Comment description required.")
            errors = {
                "errors": errors
            }
            return errors

        # Else if no errors detected above, Get Sender, Receiver, and Message to which Comment belongs, create Comment:
        new_comment = Comment(description=kwargs["description"], sender=User.objects.get(id=kwargs["sender_id"]), receiver=User.objects.get(id=kwargs["receiver_id"]), message=Message.objects.get(id=kwargs["message_id"]))
        new_comment.save()
        return new_comment

class User(models.Model):
    """Creates instances of a `User`."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=22)
    description = models.CharField(max_length=500, default="This user has not set a description yet.")
    user_level = models.IntegerField(default=0) # integer representing user level: 0 = normal user (default), 1 = administrator
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() # Adds additional instance methods to `User`

class Message(models.Model):
    """Creates instances of a `Message`."""

    description = models.CharField(max_length=500)
    sender = models.ForeignKey(User, related_name="messages_sent", on_delete=models.CASCADE) # This is the sender.
    receiver = models.ForeignKey(User, related_name="messages_received", on_delete=models.CASCADE) # This is the receiver.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager() # Adds additional instance methods to `Message`

class Comment(models.Model):
    """Creates instances of a `Comment`."""

    description = models.CharField(max_length=500)
    sender = models.ForeignKey(User, related_name="comments_sent", on_delete=models.CASCADE, default=None) # Many:1 relationship with `User`. Delete `Message` if `User` is deleted.
    receiver = models.ForeignKey(User, related_name="comments_received", on_delete=models.CASCADE) # Many:1 relationship with `User`. Delete `Message` if `User` is deleted.
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="comment") # Many:1 relationship with `Message`. Delete `Comment` if `Message` is deleted.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager() # Adds additional instance methods to `Comment`
