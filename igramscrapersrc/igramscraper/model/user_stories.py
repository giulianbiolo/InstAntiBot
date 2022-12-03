from .initializer_model import InitializerModel

class UserStories(InitializerModel):

    def __init__(self, stories=None, owner=None):
        self.owner = owner
        if stories==None:
            self.stories = []
        super().__init__()
