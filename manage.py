#!/usr/bin/env python

import os
import sys


def generate_token():
    
    import django
    django.setup() 

    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token

    try:
        user = User.objects.get(username="xhenrii")  
        token, created = Token.objects.get_or_create(user=user) 
        print(f"Token for user {user.username}: {token.key}")
    except User.DoesNotExist:
        print("User not found. Please create the user.")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'connectly_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

   
    if len(sys.argv) > 1 and sys.argv[1] == "generate_token":
        generate_token()
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
