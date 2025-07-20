class Feature:
    """
    Base class for all feature modules.
    """

    def __init__(self, processor, storage):
        self.processor = processor
        self.storage = storage

    def update(self, city: str) -> None:
        """
        Update the feature with new data.
        """
        pass

    def render(self) -> None:
        """
        Render feature in GUI.
        """
        pass