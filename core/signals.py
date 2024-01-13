import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from core.models import User, Article


@receiver([pre_save, post_delete], sender=Article)
def remove_old_cover(sender, instance: Article, signal, **kwargs):
    """Elimina del sistema de archivos la imagen anteriormente guardada"""

    if signal == pre_save:
        article = Article.objects.filter(pk=instance.pk).first()

        if article:
            if (
                os.path.isfile(article.cover_image.path)
                and article.cover_image.path != instance.cover_image.path
            ):
                os.remove(article.cover_image.path)

    elif signal == post_delete:
        if instance.cover_image:
            if os.path.isfile(instance.cover_image.path):
                os.remove(instance.cover_image.path)


@receiver(pre_save, sender=User)
def remove_old_profile_image(sender, instance: User, **kwargs):
    """Elimina del sistema de archivos la imagen anteriormente guardada"""

    user = User.objects.filter(pk=instance.pk).first()

    if user:
        is_image_user_default = user.profile_image.path.endswith(
            "/backend/images/user.png"
        )

        if (
            not is_image_user_default
            and user.profile_image.path != instance.profile_image.path
        ):
            if os.path.isfile(user.profile_image.path):
                os.remove(user.profile_image.path)
