def validate_fields(*args):
    return all(arg.strip() != '' for arg in args)