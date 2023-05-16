class Validate:

    @staticmethod
    def equals(actual, expected):
        if actual != expected:
            raise ValueError(f"Object not equal! expected:\n{expected}\nactual:{actual}")
