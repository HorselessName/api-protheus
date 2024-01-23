from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Executor


class ExecutorSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Executor
        load_instance = True
        include_fk = True
        ordered = True
