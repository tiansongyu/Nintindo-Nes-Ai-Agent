def linear_schedule(initial_value: float, final_value: float = 0.0):
    """Interpolate from initial to final as SB3 progress goes from 1 to 0."""

    def scheduler(progress: float) -> float:
        return final_value + progress * (initial_value - final_value)

    return scheduler
