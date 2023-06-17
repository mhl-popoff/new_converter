import os
import logging
import json

from documents.fields import Field


logger = logging.getLogger('documents.document')
logger.setLevel(logging.DEBUG)


class Document:
    def __init__(self, **kwargs):
        for arg, value in kwargs.items():
            setattr(self, arg, value)

    def objects(self, **kwargs):
        path = self.__class__.__name__.lower() + '.json'

        # open the file and read the contents
        try:
            with open(path, 'r') as f:
                records = json.loads(f.read())
        except FileNotFoundError:
            records = []

        if len(kwargs) > 0 and len(records) > 0:
            matching_records = []

            for record in records:
                match = True
                for k, v in kwargs.items():
                    if kwargs[k] != record.get(k):
                        match = False

                if match:
                    matching_records.append(record)

            records = matching_records

        return Records(records)

    def _get_fields(self):
        return {k: v for k, v in self.__class__.__dict__.items() if isinstance(v, Field)}

    def save(self):
        saved = True
        path = self.__class__.__name__.lower() + '.json'

        # open the file and read the contents
        try:
            with open(path, 'r') as f:
                records = json.loads(f.read())
        except FileNotFoundError:
            records = []

        record = dict()

        try:
            for name, field_obj in self._get_fields().items():
                data = vars(self).get(name)
                field_obj.validate(data)

                if field_obj.unique:
                    collection_fields = [record[name] for record in records]

                    if data in collection_fields:
                        raise ValueError('failed unique constraint')

                if data is not None:
                    record[name] = data

        except ValueError as e:
            saved = False
            logger.error('validation problem: {} - aborting save'.format(e))
            return saved

        logger.debug('document save path: {}'.format(self.__class__.__name__.lower()))

        # save the new record into the array
        records.append(record)

        # save the new record set
        with open(path, 'w') as f:
            logger.debug(json.dumps(records))
            f.write(json.dumps(records))

        return saved


class Records(list):
    def __init__(self, elements: list):
        super().__init__(self)
        for e in elements:
            self.append(e)

    def count(self):
        return len(self)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    doc = Document(email2='three@four.com')
    doc.email = 'one@two.com'
    print(vars(doc))

    doc.save()

