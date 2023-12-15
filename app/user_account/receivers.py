from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from user_account.models import User


@receiver(pre_save, sender=User)
def user_pre_save(*args, **kwargs):
    print('PRE SAVE IN SIGNAL')


@receiver(post_save, sender=User)
def user_pre_save(*args, **kwargs):
    print('POST SAVE IN SIGNAL')

    @receiver(pre_save, sender=User)
    def user_set_phone_number(instance, *args, **kwargs):
        if instance.phone_number:
            instance.phone_number = "".join(
                [num for num in instance.phone_number if num in range(0, 10)]
            )
