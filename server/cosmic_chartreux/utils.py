

def login_required(func):
    @wraps
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)
