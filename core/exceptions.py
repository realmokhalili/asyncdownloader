class InvalidURL(ValueError):
    def __init__(self, url, *args):
        self.url = url
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{self.url} is invalid"