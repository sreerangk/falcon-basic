from db.engine import engine
from db.models import metadata

metadata.create_all(engine)
