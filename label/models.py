from urllib.parse import urljoin

import requests
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils.translation import gettext as _

from project.settings import TEMP_ROOT, MEDIA_URL

__all__ = (
    'Manufactory',
    'Kind',
    'Image',
    'Label',
)


class Manufactory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('Производитель')
        verbose_name_plural = _('Производители')

    def __str__(self):
        return '{class_name}("{name}")'.format(class_name=self.__class__.__name__, name=self.name)


class Kind(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return '{class_name}("{name}")'.format(class_name=self.__class__.__name__, name=self.name)

    class Meta:
        verbose_name = _('Сорт')
        verbose_name_plural = _('Сорта')


class Image(models.Model):
    label = models.ForeignKey('label.Label', verbose_name=_('Этикетка'), on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name=_('Изображение'), upload_to='images/')
    is_default = models.BooleanField(verbose_name=_('Изображение по-умолчанию'), default=False)

    class Meta:
        verbose_name = _('Изображение')
        verbose_name_plural = _('Изображения')

    def __str__(self):
        return '{class_name}(id={id}, label="{name}")'.format(
            class_name=self.__class__.__name__,
            id=self.label.id,
            name=self.label.name,
        )

    def save(self, *args, **kwargs):
        image_url = kwargs.pop('image_url', None)
        if image_url:
            with requests.get(image_url) as response:
                content_type = response.headers['Content-Type']
                suffix = '.' + content_type.split('/')[-1]

                img_temp = NamedTemporaryFile(dir=TEMP_ROOT, delete=True, suffix=suffix)
                img_temp.write(response.content)
                img_temp.seek(0)

                self.image = SimpleUploadedFile(
                    name=img_temp.name,
                    content=img_temp.read(),
                )

        if self.is_default:
            self.label.images.update(is_default=False)
        else:
            self.is_default = False if self.label.images.filter(is_default=True).first() else True
        super(Image, self).save(*args, **kwargs)


class Label(models.Model):
    manufactory = models.ForeignKey('label.Manufactory', verbose_name=_('Производитель'), on_delete=models.SET_NULL, related_name='labels', null=True)
    kind = models.ForeignKey('label.Kind', verbose_name=_('Сорт'), on_delete=models.SET_NULL, related_name='labels', null=True)
    name = models.CharField(verbose_name=_('Наименование'), max_length=255)
    year = models.SmallIntegerField(verbose_name=_('Год выпуска'))
    added_dt = models.DateTimeField(verbose_name=_('Дата добавления'), auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(verbose_name=_('Время последнеднего изменения'), auto_now=True, null=True)
    seen = models.IntegerField(verbose_name=_('Просмотрено'), default=0)
    rating = models.DecimalField(verbose_name=_('Рейтинг'), max_digits=3, decimal_places=2, default=5)

    class Meta:
        verbose_name = _('Этикетка')
        verbose_name_plural = _('Этикетки')

    def __str__(self):
        return '{class_name}("{name}")'.format(class_name=self.__class__.__name__, name=self.name)

    @property
    def default_image(self):
        return self.images.filter(is_default=True).first()

    def get_related_labels(self, count):
        result = []

        related_by_kind = Label.objects.filter(kind=self.kind)[:count]
        result += list(related_by_kind)
        if len(result) >= count:
            return result

        needed_labels = count - len(result)
        related_by_manufactory = Label.objects.filter(manufactory=self.manufactory).exclude(kind=self.kind)[:needed_labels]
        result += list(related_by_manufactory)
        if len(result) >= count:
            return result

        needed_labels = count-len(result)
        related_by_other = Label.objects.difference(related_by_kind, related_by_manufactory)[:needed_labels]
        result += list(related_by_other)
        return result
