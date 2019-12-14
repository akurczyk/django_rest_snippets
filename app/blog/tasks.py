from __future__ import absolute_import, unicode_literals

from celery import shared_task


@shared_task
def periodic_task(x, y):
    print(x*y)
    return x*y


@shared_task
def delayed_task(x, y):
    print(x+y)
    return x + y
