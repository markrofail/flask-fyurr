def parse_errors(error_dict):
    error_messages = ""
    for error_label, error_data in error_dict.items():
        error_label = error_label.replace("_", " ").title()

        if isinstance(error_data, dict):
            error_messages += parse_errors(error_data)
        else:
            if isinstance(error_data, list):
                error_data = error_data[0]
            error_messages += f"{error_label}: {error_data}\n"
    return error_messages


def flash_error(error_msg):
    from flask import flash

    flash(error_msg, "danger")
