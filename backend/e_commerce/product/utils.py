from typing import Union


def increase_view_count(
    cooldown_period: int = 3600 * 24,
    instance_name: Union[str | None] = None,
):
    """
    For incrementing the view count of an django model instance and 
    setting a cooldown period by using the current client's IP.
    """

    def decorator(get_method):
        def wrapper(*args, **kwargs):
            # do someting before
            response = get_method(*args, **kwargs)
            # do something after functions execution
            return

        return wrapper

    return decorator
