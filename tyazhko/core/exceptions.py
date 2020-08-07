class GnosisBaseError(Exception):
    def __str__(self):
        return "Unexpected server error!"

    def get_exception_path(self):
        return self.__class__.__name__


class GnosisCryptoKeyError(GnosisBaseError):
    def __str__(self):
        return "Invalid crypto key"
