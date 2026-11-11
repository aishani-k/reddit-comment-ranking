from mesa import Agent


class CommentAgent(Agent):
    """A single synthetic comment in a discussion thread.

    The Mesa-generated ``unique_id`` is left untouched. ``comment_id`` is the
    stable project-level identifier written to CSV files.
    """

    def __init__(
        self,
        model,
        comment_id: str,
        timestamp: int,
        upvotes: int,
        downvotes: int,
    ):
        super().__init__(model)
        self.comment_id = comment_id
        self.timestamp = timestamp
        self.upvotes = upvotes
        self.downvotes = downvotes

    @property
    def net_score(self) -> int:
        """Return upvotes minus downvotes."""
        return self.upvotes - self.downvotes
