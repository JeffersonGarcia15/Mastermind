# Credits to Anurag Uniyal
# https://stackoverflow.com/questions/1958219/how-to-convert-sqlalchemy-row-object-to-a-python-dict
def model_to_dict(model):
    d = {}
    for column in model.__table__.columns:
        d[column.name] = str(getattr(model, column.name))

    return d