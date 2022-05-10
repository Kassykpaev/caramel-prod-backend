from tabnanny import verbose
from django.db import models
from django.forms import ValidationError
from account.models import User


class Config(models.Model):
    class Meta:
        verbose_name = "Конфигурация"
        verbose_name_plural = "Конфигурация"

    price_per_unit = models.FloatField(
        verbose_name='Стоимость литра сиропа (тг)', default=5000, null=False)

    def __str__(self):
        return 'Конфигурация'

    def save(self, *args, **kwargs):
        if not self.pk and Config.objects.exists():
            # if you'll not check for self.pk
            # then error will also raised in update of exists model
            raise ValidationError('There is can be only one Config instance')
        return super(Config, self).save(*args, **kwargs)


class Address(models.Model):
    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    city = models.CharField(verbose_name='Город', default='',
                            null=False, blank=False, max_length=255)
    street = models.CharField(
        verbose_name='Улица', default='', null=False, blank=False, max_length=255)
    house_number = models.CharField(
        verbose_name='Номер дома', default='', null=False, blank=False, max_length=255)

    def __str__(self):
        return '%s, %s %s' % (self.city, self.street, self.house_number)


class Order(models.Model):

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    status_updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='client_id', verbose_name='Пользователь', null=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    total_price = models.FloatField(
        verbose_name='Общая стоимость', default=0, null=False)
    price_per_unit = models.FloatField(
        verbose_name='Стоимость одного литра', default=5000, null=False)
    volume = models.FloatField(
        verbose_name='Объем', default=0, null=False)
    payment_received = models.BooleanField(
        verbose_name='Оплачен', default=False)

    CREATED = 'Created'
    IN_PROGRESS = 'Progress'
    READY_FOR_SHIPPING = 'Ready for shipping'
    SHIPPING = 'Shipping'
    DONE = 'Done'
    DECLINED = 'Declined'

    STATUS_CHOICES = (
        (CREATED, 'Создан'),
        (IN_PROGRESS, 'В процессе'),
        (READY_FOR_SHIPPING, 'Готов к доставке'),
        (SHIPPING, 'Доставляется'),
        (DONE, 'Завершен'),
        (DECLINED, 'Отклонен'),
    )
    status = models.CharField(verbose_name='Статус',
                              max_length=255, choices=STATUS_CHOICES, default=CREATED)

    def __str__(self):
        return 'Заказ от %s | %s' % (self.created_at, self.status)
