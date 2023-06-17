import logging

logger = logging.getLogger('documents.document')
logger.setLevel(logging.DEBUG)


class Field:
    def __init__(self, **kwargs):
        self.required = kwargs.get('required')
        self.unique = kwargs.get('unique')
        self.default = kwargs.get('default')

        logger.debug('field initialized: {}'.format(self.__class__.__name__))

    def validate(self, data):
        valid = True
        if self.required is True:
            if data is None:
                raise ValueError('field is required')

        return valid


class StringField(Field):
    def __init__(self, max_length=None, min_length=None, **kwargs):
        super().__init__(**kwargs)

        self.max_length = max_length
        self.min_length = min_length

    def validate(self, data):
        valid = super().validate(data)

        if data is not None:
            if not isinstance(data, str):
                raise ValueError('data type must be a string type')

            if self.max_length:
                if len(data) > self.max_length:
                    raise ValueError('data exceeds maximum length')

            if self.min_length:
                if len(data) < self.min_length:
                    raise ValueError('data exceeds maximum length')

        return valid


class BooleanField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self, data):
        valid = super().validate(data)

        if data is not None:
            if not isinstance(data, bool):
                raise ValueError('data type must be a string type')

        return valid


class IntField(Field):
    def __init__(self, min_value=None, max_value=None, **kwargs):
        super().__init__(**kwargs)

        self.min_value = min_value
        self.max_value = max_value

    def validate(self, data):
        valid = super().validate(data)

        if data is not None:
            if not isinstance(data, int):
                raise ValueError('data type must be an integer type')

            if self.max_value:
                if data > self.max_value:
                    raise ValueError('data exceeds maximum value')

            if self.min_value:
                if data < self.min_value:
                    raise ValueError('data exceeds maximum length')

        return valid
