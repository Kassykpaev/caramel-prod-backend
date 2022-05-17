import datetime
from store.models import Order
from .models import Boiler
from .constants import DELTA_TEMPERATURE, MAKING_TIME, MIN_TEMPERATURE, MAX_TEMPERATURE, DELTA_TIME, KI, KD, KP
import pytz

utc = pytz.UTC


def reset_boiler(boiler):
    boiler.engine_voltage = 0
    boiler.coef_i = 0
    boiler.coef_mv_bar = 0
    boiler.error_prev = 0
    boiler.made_volume = 0
    boiler.status = "VACANT"
    boiler.order.status = Order.READY_FOR_SHIPPING
    boiler.order.save()
    boiler.order = None


def check_order_in_progress(boiler):
    if boiler.order.status != Order.IN_PROGRESS:
        boiler.order.status = Order.IN_PROGRESS
        boiler.order.save()


def check_for_engine_overheat(boiler):
    if boiler.engine_temperature >= MAX_TEMPERATURE:
        boiler.status = "ALARM"


def decrease_temperature(boiler):
    if boiler.engine_temperature > MIN_TEMPERATURE:
        boiler.engine_temperature -= DELTA_TEMPERATURE * 10


def is_finished(boiler):
    timestamp = datetime.datetime.now().replace(tzinfo=utc)
    return boiler.ending_time_of_iteration.replace(tzinfo=utc) <= timestamp


def set_next_batch_if_has_more(boiler):
    tmp = boiler.initial_order_volume - boiler.made_volume
    if tmp > boiler.volume:
        timestamp = datetime.datetime.now().replace(tzinfo=utc)
        boiler.made_volume += boiler.volume
        boiler.ending_time_of_iteration = timestamp + \
            datetime.timedelta(milliseconds=MAKING_TIME)
    else:
        reset_boiler(boiler)


def calculate_pid(boiler):
    e = boiler.engine_target_voltage - boiler.engine_voltage
    p = KP*e
    i = boiler.coef_i + KI*e*(DELTA_TIME)
    d = KD*(e-boiler.error_prev)/(DELTA_TIME)
    boiler.coef_i = i
    boiler.engine_voltage = boiler.coef_mv_bar+p+i+d
    boiler.error_prev = e


def update_models():
    boilers = Boiler.objects.all()
    for boiler in boilers:
        if boiler.status == "IN_PROGRESS":
            if is_finished(boiler):
                set_next_batch_if_has_more(boiler)
            else:
                check_order_in_progress(boiler)
                if boiler.mode == "AUTO":
                    calculate_pid(boiler)
            boiler.engine_temperature += DELTA_TEMPERATURE
        elif boiler.status in ["VACANT", "ALARM", "DONE"]:
            decrease_temperature(boiler)
        check_for_engine_overheat(boiler)

        boiler.save()
