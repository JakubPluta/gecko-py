def validate_coma_sep(s: str):
    pass


def convert_list_to_coma_sep(l: list):
    if isinstance(l, list) and len(l) > 0:
        return ",".join(l)
    else:
        return l
