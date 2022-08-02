
""" ``model`` module.
"""

from datetime import date
from datetime import datetime
from datetime import time
from time import strptime

from wheezy.validation.comp import Decimal
from wheezy.validation.comp import PY3
from wheezy.validation.comp import bytes_type
from wheezy.validation.comp import null_translations
from wheezy.validation.comp import ref_gettext
from wheezy.validation.comp import str_type
from wheezy.validation.comp import tob
from wheezy.validation.i18n import decimal_separator
from wheezy.validation.i18n import default_date_input_format
from wheezy.validation.i18n import default_datetime_input_format
from wheezy.validation.i18n import default_time_input_format
from wheezy.validation.i18n import fallback_date_input_formats
from wheezy.validation.i18n import fallback_datetime_input_formats
from wheezy.validation.i18n import fallback_time_input_formats
from wheezy.validation.i18n import thousands_separator
from wheezy.validation.patches import patch_strptime_cache_size


if not patch_strptime_cache_size():  # pragma: nocover
    from warnings import warn
    warn('Failed to patch _strptime._CACHE_MAX_SIZE')
    del warn
del patch_strptime_cache_size


def try_update_model(model, values, results, translations=None):
    """ Try update `model` with `values` (a dict of lists or strings),
        any errors encountered put into `results` and use `translations`
        for i18n.
    """
    if translations is None:
        translations = null_translations
    gettext = ref_gettext(translations)
    if hasattr(model, '__iter__'):
        attribute_names = model
        model_type = type(model)
        getter = model_type.__getitem__
        setter = model_type.__setitem__
    else:
        attribute_names = list(model.__dict__)
        attribute_names.extend([name for name in model.__class__.__dict__
                                if name[:1] != '_'])
        getter = getattr
        setter = setattr
    succeed = True
    for name in attribute_names:
        if name not in values:
            continue
        value = values[name]
        attr = getter(model, name)
        # Check if we have a deal with list like attribute
        if hasattr(attr, '__setitem__'):
            # Guess type of list by checking the first item,
            # fallback to str provider that leaves value unchanged.
            if attr:
                provider_name = type(attr[0]).__name__
                if provider_name in value_providers:
                    value_provider = value_providers[provider_name]
                else:  # pragma: nocover
                    continue
            else:
                value_provider = value_providers['str']
            items = []
            try:
                for item in value:
                    items.append(value_provider(item, gettext))
                attr[:] = items
            except (ArithmeticError, ValueError):
                results[name] = [gettext(
                    "Multiple input was not in a correct format.")]
                succeed = False
        else:  # A simple value attribute
            provider_name = type(attr).__name__
            if provider_name in value_providers:
                value_provider = value_providers[provider_name]
                if isinstance(value, list):
                    value = value and value[-1] or ''
                try:
                    value = value_provider(value, gettext)
                    setter(model, name, value)
                except (ArithmeticError, ValueError):
                    results[name] = [gettext(
                        "Input was not in a correct format.")]
                    succeed = False
    return succeed


# region: internal details

# value_provider => lambda value, gettext: parsed_value

def bytes_value_provider(value, gettext):
    """ Converts ``value`` to ``bytes``.
    """
    if value is None:
        return None
    t = type(value)
    if t is bytes_type:
        return value
    if t is str_type:
        return value.encode('UTF-8')
    return tob(value)


def str_value_provider(value, gettext):
    """ Converts ``value`` to ``str``.
    """
    if value is None:
        return None
    t = type(value)
    if t is str_type:
        return value.strip()
    if t is bytes_type:
        return value.strip().decode('UTF-8')
    return str_type(value)


def int_value_provider(value, gettext):
    """ Converts ``value`` to ``int``.
    """
    if value is None or type(value) is int:
        return value
    value = str(value).strip()
    if value:
        s = thousands_separator(gettext)
        if s in value:
            value = value.replace(s, '')
        return int(value)
    else:
        return None


decimal_zero = Decimal(0)
decimal_zero_values = ['0', '0.0', '0.00']


def decimal_value_provider(value, gettext):
    """ Converts ``value`` to ``Decimal``.
    """
    if value is None:
        return None
    value = str(value).strip()
    if value:
        s = thousands_separator(gettext)
        if s in value:
            value = value.replace(s, '')
        s = decimal_separator(gettext)
        if s in value:
            value = value.replace(s, '.', 1)
        if value in decimal_zero_values:
            return decimal_zero
        return Decimal(value)
    else:
        return None


boolean_true_values = ['1', 'True']


def bool_value_provider(value, gettext):
    """ Converts ``value`` to ``bool``.
    """
    if value is None or type(value) is bool:
        return value
    value = str(value).strip()
    return value in boolean_true_values


def float_value_provider(value, gettext):
    """ Converts ``value`` to ``float``.
    """
    if value is None or type(value) is float:
        return value
    value = str(value).strip()
    if value:
        s = thousands_separator(gettext)
        if s in value:
            value = value.replace(s, '')
        s = decimal_separator(gettext)
        if s in value:
            value = value.replace(s, '.', 1)
        return float(value)
    else:
        return None


def date_value_provider(value, gettext):
    """ Converts ``value`` to ``datetime.date``.
    """
    if value is None:
        return None
    value = str(value).strip()
    if value:
        try:
            return date(*strptime(
                value,
                default_date_input_format(gettext))[:3])
        except ValueError:
            for fmt in fallback_date_input_formats(gettext).split('|'):
                try:
                    return date(*strptime(value, fmt)[:3])
                except ValueError:
                    continue
            raise ValueError()
    else:
        return None


def time_value_provider(value, gettext):
    """ Converts ``value`` to ``datetime.time``.
    """
    if value is None:
        return None
    value = str(value).strip()
    if value:
        try:
            return time(*strptime(
                value,
                default_time_input_format(gettext))[3:6])
        except ValueError:
            for fmt in fallback_time_input_formats(gettext).split('|'):
                try:
                    return time(*strptime(value, fmt)[3:6])
                except ValueError:
                    continue
            raise ValueError()
    else:
        return None


def datetime_value_provider(value, gettext):
    """ Converts ``value`` to ``datetime.datetime``.
    """
    if value is None:
        return None
    value = str(value).strip()
    if value:
        try:
            return datetime(*strptime(
                value,
                default_datetime_input_format(gettext))[:6])
        except ValueError:
            for fmt in fallback_datetime_input_formats(gettext).split('|'):
                try:
                    return datetime(*strptime(value, fmt)[:6])
                except ValueError:
                    continue
            value = date_value_provider(value, gettext)
            return datetime(value.year, value.month, value.day)
    else:
        return None


value_providers = {
    'int': int_value_provider,
    'Decimal': decimal_value_provider,
    'bool': bool_value_provider,
    'float': float_value_provider,
    'date': date_value_provider,
    'time': time_value_provider,
    'datetime': datetime_value_provider
}

if PY3:  # pragma: nocover
    value_providers['str'] = str_value_provider
    value_providers['bytes'] = bytes_value_provider
else:  # pragma: nocover
    value_providers['str'] = bytes_value_provider
    value_providers['unicode'] = str_value_provider
