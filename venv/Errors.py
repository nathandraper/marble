class OrientationError(Exception):
    def __init__(self, orientation):
        self.message = (f"{orientation} is not an accepted orientation. Orientation must be: \"left\", \"right\", "
                        f"\"up\", or \"down\".")

    def __str__(self):
        return repr(self.message)
