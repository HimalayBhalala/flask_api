from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limitater = Limiter(key_func=get_remote_address,default_limits=["200 per day","5 per hour"])