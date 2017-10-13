
# User Dashboard
This project allows users to register or login, with validations and encryption via bcrypt. Users can post messages and comments.

**Important Note**: The first five users created are set to an admin. Admins may create or edit users. Normal users may edit their own profile only. All users after the first 5 users, are normal users.

## Features:
- Add new admin-level and normal-level users.
- Edit your own profile.
- Admins can edit normal-level user's profiles.
- Admins can create new users.
- Admins can delete users.
- All users can create messages and comments.
- Ordinate time styling on messages (ie, x days ago...)

## Technologies:
+ `Django 1.11`
+ `bcrypt`
+ `Bootstrap`
+ `MVC` architecture

## Notes:
+ Be sure to `bower install` the `bower.json` file in the `apps/dashboard/static/dashboard` folder and to pip install `requirements.txt`.

### Later Features / Changes Log:
+ Refactor, Modularize `models.py` (medium-priority).
+ None of your API routes check for valid session--backend routes are insecure. Tighten these up so spoofed request cannot be made (high-priority).
+ Add some validations to `user description` on profile page (low-priority).
