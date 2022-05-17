import datetime
from store.models import Order
from .models import Boiler
from .constants import DELTA_TEMPERATURE, MAKING_TIME, MIN_TEMPERATURE, MAX_TEMPERATURE, DELTA_TIME, KI, KD, KP
import pytz

utc = pytz.UTC


def update_manual(boiler):
    if boiler.status == "IN_PROGRESS":
        timestamp = datetime.datetime.now().replace(tzinfo=utc)
        if boiler.ending_time_of_iteration.replace(tzinfo=utc) <= timestamp:
            tmp = boiler.initial_order_volume - boiler.made_volume
            if tmp > boiler.volume:
                boiler.made_volume += boiler.volume
                boiler.ending_time_of_iteration = timestamp + \
                    datetime.timedelta(milliseconds=MAKING_TIME)
            else:
                boiler.made_volume = 0
                boiler.status = "VACANT"
                boiler.order.status = Order.READY_FOR_SHIPPING
                boiler.order.save()
                boiler.order = None
        else:
            if boiler.order.status != Order.IN_PROGRESS:
                boiler.order.status = Order.IN_PROGRESS
                boiler.order.save()

        boiler.engine_temperature += DELTA_TEMPERATURE
    elif boiler.status in ["VACANT", "ALARM", "DONE"]:
        if boiler.engine_temperature > MIN_TEMPERATURE:
            boiler.engine_temperature -= DELTA_TEMPERATURE * 10
    if boiler.engine_temperature >= MAX_TEMPERATURE:
        boiler.status = "ALARM"


def get_difference(timestamp, ending_time_of_iteration):
    init = ending_time_of_iteration - \
        datetime.timedelta(milliseconds=MAKING_TIME)
    difference = timestamp-init
    return difference.seconds


def update_auto(boiler):
    if boiler.status == "IN_PROGRESS":
        timestamp = datetime.datetime.now().replace(tzinfo=utc)
        if boiler.ending_time_of_iteration.replace(tzinfo=utc) <= timestamp:
            tmp = boiler.initial_order_volume - boiler.made_volume
            if tmp > boiler.volume:
                boiler.made_volume += boiler.volume
                boiler.ending_time_of_iteration = timestamp + \
                    datetime.timedelta(milliseconds=MAKING_TIME)
            else:
                boiler.made_volume = 0
                boiler.status = "VACANT"
                boiler.order.status = Order.READY_FOR_SHIPPING
                boiler.order.save()
                boiler.order = None
                boiler.coef_i = 0
                boiler.coef_mv_bar = 0
                boiler.error_prev = 0
        else:
            if boiler.order.status != Order.IN_PROGRESS:
                boiler.order.status = Order.IN_PROGRESS
                boiler.order.save()

            e = boiler.engine_target_voltage - boiler.engine_voltage
            p = KP*e
            i = boiler.coef_i + KI*e*(DELTA_TIME)
            d = KD*(e-boiler.error_prev)/(DELTA_TIME)
            boiler.coef_i = i
            boiler.engine_voltage = boiler.coef_mv_bar+p+i+d
            boiler.error_prev = e

        boiler.engine_temperature += DELTA_TEMPERATURE
    elif boiler.status in ["VACANT", "ALARM", "DONE"]:
        if boiler.engine_temperature > MIN_TEMPERATURE:
            boiler.engine_temperature -= DELTA_TEMPERATURE * 10
    if boiler.engine_temperature >= MAX_TEMPERATURE:
        boiler.status = "ALARM"


def update_models():
    boilers = Boiler.objects.all()
    for boiler in boilers:
        if boiler.mode == 'MANUAL':
            update_manual(boiler)
        else:
            update_auto(boiler)
        boiler.save()
