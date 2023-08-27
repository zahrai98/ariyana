from celery import shared_task, periodic_task
from . import models
from django.core.mail import send_mail
from django.contrib.auth.models import User
import datetime
from django.db.models import Count
from celery.schedules import crontab
from twitter.settings import EMAIL_HOST_USER


def cal_five_top_like(user):
    day_long = datetime.datetime.now() - datetime.timedelta(days=1)

    posts = (
        models.Post.objects.filter(
            user_followers=user,
            created__gte=day_long,
        )
        .annotate(num_likes=Count("pvotes"))
        .order_by("-num_likes")[:5]
    )

    return posts


@periodic_task(run_every=(crontab(minute=0, hour=0)))
def send_mail_five_top_post():
    subject = "five top posts"
    from_email = EMAIL_HOST_USER

    users = User.objects.all()
    for user in users:
        message = ""
        posts = cal_five_top_like(user)
        if not posts:
            continue
        for post in posts:
            message.apend(f"{post.body} \n")
        send_mail(subject, message, from_email, [user.email])
