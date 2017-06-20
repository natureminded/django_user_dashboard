
# User Dashboard
This project allows users to register or login, with validations and encryption via bcrypt. Users can post messages and comments. The first user created is set to an admin. Admins may create or edit users. Normal users may edit their own profile only.

## Technologies:
+ `Django 1.11`
+ `bcrypt`
+ `Bootcamp`
+ `MVC` architecture

## Notes:
+ Be sure to `bower install` the `bower.json` file in the `apps/dashboard/static/dashboard` folder.

### Later Features / Changes Log:
+ Clean up error tags -- simplify nomenclature, ie: "profile_errors" would become "errors", and thus referenced in the template as `message_tags="profile error"` instead of `message_tags="profile_errors error"`
+ Refactor, Modularize `models.py`.
+ Setup lots of exceptions (for back button submission on forms -- delete , etc, etc.) IE, make sure various usage cases aren't missed causing your app to break.
