def register(model_or_iterable, **options):
    """
    Registers the given model(s) with the given backoffice options.
    The model(s) should be Model classes, not instances.

    @register(Book)
    class BookBackoffice(BackofficeOptions):
        pass
    """
    from djbackoffice.core import BackofficeOptions, backoffice

    def wrapper(opts_class):
        if not issubclass(opts_class, BackofficeOptions):
            raise ValueError('Wrapped class must subclass BackofficeOptions.')
        backoffice.register(model_or_iterable, opts_class, **options)
        return opts_class

    return wrapper
