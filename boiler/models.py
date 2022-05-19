from django.db import models
from store.models import Order
# Create your models here.


class Boiler(models.Model):
    class Meta:
        verbose_name = "Котел"
        verbose_name_plural = "Котлы"

    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='order_performing',
                              verbose_name='Выполняемый заказ', null=True, blank=True)
    volume = models.FloatField(
        verbose_name='Объем котла', null=False, default=200.0)
    engine_temperature = models.FloatField(
        verbose_name='Температура двигателя', null=False, default=17.0)
    ending_time_of_iteration = models.DateTimeField(
        verbose_name='Конечное время выполнения нышней партии', null=True,  blank=True)
    initial_order_volume = models.FloatField(
        verbose_name='Общий объем заказа', null=True,  blank=True)
    made_volume = models.FloatField(
        verbose_name='Проделанный объем заказа', null=True, blank=True)
    engine_voltage = models.FloatField(
        verbose_name='PV', null=True,  blank=True)
    engine_target_voltage = models.FloatField(
        verbose_name='SP', null=True,  blank=True)
    error_prev = models.FloatField(
        verbose_name='Предыдущая ошибка', default=0.0)
    coef_i = models.FloatField(verbose_name='Коэфициент I', default=0.0)
    coef_mv_bar = models.FloatField(verbose_name='Коэфициент MV', default=0.0)

    STATE_CHOICES = (
        ("VACANT", "Готова к работе"),
        ("IN_PROGRESS", "В процессе выполнения заказа"),
        ("DONE", "Закончена работа над заказом"),
        ("ALARM", "Перегрев двигателя")
    )

    MODE_CHOICES = (
        ("AUTO", "Автоматический режим"),
        ("MANUAL", "Ручной режим")
    )

    status = models.CharField(
        verbose_name='Статус', max_length=255, choices=STATE_CHOICES, default="VACANT")
    mode = models.CharField(
        verbose_name='Режим', max_length=255, choices=MODE_CHOICES, default="MANUAL")

    def __str__(self):
        return 'Котел номер {id}, режим {mode}, статус {status}, температура {temperature}'\
            .format(id=self.id, mode=self.mode, status=self.status, temperature=self.engine_temperature)
