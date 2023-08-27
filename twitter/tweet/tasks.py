from celery import shared_task
from . import models
from django.core.mail import send_mail
from django.contrib.auth.models import User
import datetime

def cal_five_top_like(user):
    posts = models.Post.objects.filter(user_followers=user, created__lte=datetime.datetime.now())\
                                            .order_by('-likes_count').limit(5)
    return posts
    
    
@shared_task
def send_mail_five_top_post():
    subject = "five top posts"
    from_email = 'email@example.com'

    users =  User.objects.all()
    for user in users:
        message = ''
        posts = cal_five_top_like(user)
        if not posts:
            continue
        for post in posts:
            message.apend(f"{post.body} \n")
        send_mail(subject, message, from_email, [user.email])


