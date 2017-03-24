from __future__ import unicode_literals

from django.db import models

import re
import datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def regVal(self, postData):
        current_date = datetime.datetime.today().strftime('%Y-%m-%d')
        error_messages = []
        if len(postData['name']) < 2:
            error_messages.append('Name too short')
        elif postData['name'].isdigit():
            error_messages.append('Name cannot contain numbers')
        if len(postData['alias']) < 2:
            error_messages.append('Alias too short')
        if postData['birthday'] > current_date:
            error_messages.append('Invalid birthday')
        if not EMAIL_REGEX.match(postData['email']):
            error_messages.append('Invalid email')
        if len(postData['password']) < 8:
            error_messages.append('Password too short')
        if postData['password'] != postData['confirmpw']:
            error_messages.append('Passwords do not match')
        if error_messages == []:
            password = postData['password'].encode()
            password = bcrypt.hashpw(password, bcrypt.gensalt())
            user = self.create(name = postData['name'], alias = postData['alias'], birthday = postData['birthday'], email = postData['email'], password = password)
            return { "theUser": user }
        else:
            return { "errors": error_messages }
    def login(self, postData):
        error_messages = []
        if self.filter(email = postData['email']).exists():
            password = postData['password'].encode('utf-8')
            stored_hash = User.userManager.get(email=postData['email']).password
            if bcrypt.hashpw(password, stored_hash.encode('utf-8')) != stored_hash:
                error_messages.append('incorrect password')
            else:
                user = self.get(email = postData['email'])
        else:
            error_messages.append('Email does not exist')
        if not error_messages:
            return { "theUser": user }
        else:
            return { "errors": error_messages }



class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    userManager = UserManager()

class Quote(models.Model):
    content = models.TextField(max_length=1000)
    author = models.CharField(max_length=255)
    favorites = models.ManyToManyField(User, related_name="favorites")
