import requests
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.db import models
from django.utils.translation import gettext as _

from project.settings import TEMP_ROOT

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


class Kind(models.Model):
    name = models.CharField(max_length=255)

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
            self.is_default = True if self.label.images.filter(is_default=True).first() else False
        super(Image, self).save(*args, **kwargs)


class Label(models.Model):
    manufactory = models.ForeignKey('label.Manufactory', verbose_name=_('Производитель'), on_delete=models.SET_NULL, related_name='labels', null=True)
    kind = models.ForeignKey('label.Kind', verbose_name=_('Сорт'), on_delete=models.SET_NULL, related_name='labels', null=True)
    name = models.CharField(verbose_name=_('Наименование'), max_length=255)
    year = models.SmallIntegerField(verbose_name=_('Год выпуска'))

    class Meta:
        verbose_name = _('Этикетка')
        verbose_name_plural = _('Этикетки')

    def __str__(self):
        return '{class_name}("{name}")'.format(class_name=self.__class__.__name__, name=self.name)

    @property
    def default_image(self):
        return self.images.filter(is_default=True).first()