from bson import ObjectId


class PydanticObjectId(ObjectId):
    # from https://stackoverflow.com/questions/59503461/how-to-parse-objectid-in-a-pydantic-model
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise TypeError('Invalid ObjectId')
        return str(v)

    # from: https://github.com/tiangolo/fastapi/issues/68#issuecomment-1048969124
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')
