# social_site/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Notification, Friendship, Comment
from django.contrib.auth import get_user_model


@receiver(post_save, sender=Post)
def notify_on_post_creation(sender, instance, created, **kwargs):
    if created:
        # Notify all friends when a post is created
        friends = Friendship.objects.filter(
            from_user=instance.author, accepted=True
        ).values_list('to_user', flat=True)

        for friend_id in friends:
            Notification.objects.create(
                user_id=friend_id,
                message=f"{instance.author.username} has created a new post.",
                link=f"/posts/{instance.id}/"
            )


@receiver(post_save, sender=Friendship)
def notify_on_friendship_acceptance(sender, instance, created, **kwargs):
    if not created and instance.accepted:
        Notification.objects.create(
            user=instance.from_user,
            message=f"{instance.to_user.username} has accepted your friend request.",
            link=f"/users/{instance.to_user.id}/"
        )


@receiver(post_save, sender=get_user_model())
def set_default_profile_image(sender, instance, created, **kwargs):
    if created and not instance.profile_image:
        instance.profile_image = 'default/profile_placeholder.png'
        instance.save()


@receiver(post_save, sender=Comment)
def log_comment_activity(sender, instance, created, **kwargs):
    if created:
        print(f"New comment by {instance.author} on post {instance.post.id}: {instance.content}")