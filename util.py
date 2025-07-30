def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


def partial(func, *args, **kwargs):
    def inner(*iargs, **ikwargs):
        # Combine the positional arguments (this part is fine)
        combined_args = args + iargs

        # Combine the keyword arguments using update()
        combined_kwargs = kwargs.copy() # Start with a copy of kwargs
        combined_kwargs.update(ikwargs) # Add/overwrite with ikwargs

        # Call the function with the combined arguments
        return func(*combined_args, **combined_kwargs)

    return inner