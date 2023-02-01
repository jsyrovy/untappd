from database.database import Db
from utils import is_test

db = Db(use_test_db=is_test())
