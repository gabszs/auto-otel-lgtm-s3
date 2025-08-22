from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    def dict(self, *args, **kwargs):
        dct = super().model_dumps(*args, **kwargs)
        dct = {keys: values for keys, values in dct.items() if values is not None}
        return dct
