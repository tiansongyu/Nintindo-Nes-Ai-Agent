def linear_schedule(initial_value, final_value=0.0):
    if isinstance(initial_value, str):
        initial_value = float(initial_value)
    if isinstance(final_value, str):
        final_value = float(final_value)

    def scheduler(progress):
        return final_value + progress * (initial_value - final_value)

    return scheduler

