import datetime
import pytz
from .models import Boiler
from .constants import DELTA_TEMPERATURE, MAX_TEMPERATURE, MIN_TEMPERATURE, KP, KI, DELTA_TIME, KD, MAKING_TIME

utc = pytz.UTC


def do_auto_job(boiler):
    e = boiler.engine_target_voltage - boiler.engine_voltage
    p = KP*e
    i = boiler.coef_i + KI * e * DELTA_TIME * 0.001
    d = KD * (e - boiler.error_prev) / (DELTA_TIME * 0.001)
    boiler.engine_voltage = boiler.coef_mv_bar+p+i+d
    boiler.coef_i = i
    boiler.error_prev = e


def increase_temperature(boiler):
    boiler.engine_temperature += DELTA_TEMPERATURE


def is_unit_ended(boiler):
    timestamp = datetime.datetime.now().replace(tzinfo=utc)
    return boiler.ending_time_of_iteration.replace(tzinfo=utc) <= timestamp


def clean_done_boiler(boiler, rest_volume):
    boiler.ending_time_of_iteration = None
    boiler.status = "DONE"
    boiler.engine_voltage = 0
    boiler.error_prev = 0
    boiler.coef_i = 0
    boiler.coef_mv_bar = 0
    boiler.made_volume += rest_volume
    boiler.order.made_volume += boiler.made_volume
    boiler.order.save()


def iterate_unit(boiler):
    rest_volume = boiler.initial_order_volume - boiler.made_volume
    if rest_volume <= boiler.volume:
        clean_done_boiler(boiler, rest_volume)
    else:
        boiler.made_volume += boiler.volume
        boiler.ending_time_of_iteration = datetime.datetime.now() + datetime.timedelta(milliseconds=MAKING_TIME)


def iterate_if_unit_ended(boiler):
    if is_unit_ended(boiler):
        iterate_unit(boiler)


def alarm_if_overheated(boiler):
    if boiler.status == "IN_PROGRESS" and boiler.engine_temperature >= MAX_TEMPERATURE:
        boiler.status = "ALARM"


def decrease_temperature(boiler):
    boiler.engine_temperature = max(boiler.engine_temperature - DELTA_TEMPERATURE, MIN_TEMPERATURE)


def do_job():
    boilers = Boiler.objects.all()
    for boiler in boilers:
        if boiler.status == "IN_PROGRESS":
            if boiler.mode == "AUTO":
                do_auto_job(boiler)
            iterate_if_unit_ended(boiler)
            increase_temperature(boiler)
            alarm_if_overheated(boiler)
        else:
            decrease_temperature(boiler)

        boiler.save()
