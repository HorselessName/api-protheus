from marshmallow import post_load, pre_load, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.inspection import inspect


class BaseSchema(SQLAlchemyAutoSchema):
    json = fields.Dict(dump_only=True)

    class Meta:
        model = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.Meta.model and hasattr(self.Meta.model(), 'to_dict'):
            for field_name in self.Meta.model().to_dict().keys():
                setattr(self, field_name, fields.Field())

    @staticmethod
    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

    @pre_load
    def process_dataclass(self, data):
        if self.Meta.model and isinstance(data, self.Meta.model):
            if hasattr(data, 'to_dict'):
                data = data.to_dict()
            else:
                data = data.__dict__
        return data

    @post_load
    def trim_strings(self, data):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data
