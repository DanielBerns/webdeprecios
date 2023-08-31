from datetime import date

def get_value(form, field, key):
    value = None
    try:
        value = form[key]
    except KeyError:
        raise ValidationError(
             field.gettext(f"Invalid field name {key:s}")
        )    
    return value


class DateValidator:
    """
    Validate a date value, composed of three form fields.
    The names of the three form fields start with prefix,
    and ends with '_year', '_month', and '_day'
    

    :param prefix:
        The prefix of three form fields (year, month and day)
    :param message:
        Error message to raise in case of a validation error.
    """
    
    def __init__(self, prefix, message=None):
        self.year = f'{prefix:s}_year'
        self.month = f'{prefix:s}_month'
        self.day = f'{prefix:s}_day'        
        self.message = message if message else "No valid date"


    def __call__(self, form, field):
        year = get_value(form, field, self.year)
        month = get_value(form, field, self.month)
        day = get_value(form, field, self.day)        
        
        try:
            value = date(year.data, month.data, day.data)
        except ValueError as error:
            source = str(error)
            if source.endswith('month'):
                message = f"{self.message:s}: day is out of range for this month"
            elif source.endswith('1..12'):
                message = f"{self.message:s}: month is out of range"
            else:
                message = f"{self.message:s}: {source:s}"
            raise ValidationError(message)
        else:
            pass
 
