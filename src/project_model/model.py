import pandas as pd
from mesa import Model

from .agents import CommentAgent


class ThreadModel(Model):
    """Mesa model for a synthetic Reddit-style discussion thread.

    One model step applies the selected ranking rule and stores the resulting
    top-ten ranking. Comment vote counts are fixed in this initial prototype.
    """

    def __init__(
        self,
        num_comments: int = 100,
        reserved_slots: int = 0,
        seed: int = 42,
        newer_cutoff: int = 50,
    ):
        if num_comments < 10:
            raise ValueError("num_comments must be at least 10.")
        if not 0 <= reserved_slots <= 10:
            raise ValueError("reserved_slots must be between 0 and 10.")
        if not 0 <= newer_cutoff < num_comments:
            raise ValueError("newer_cutoff must be within the comment timestamps.")
        if reserved_slots and (num_comments - newer_cutoff) < reserved_slots:
            raise ValueError("There are not enough newer comments for reserved_slots.")

        # Mesa owns the seeded random generator used to create the synthetic data.
        super().__init__(seed=seed)
        self.num_comments = num_comments
        self.reserved_slots = reserved_slots
        self.newer_cutoff = newer_cutoff
        self.run_count = 0
        self.last_ranking = None

        for i in range(self.num_comments):
            # Earlier comments generally receive more votes in this illustrative
            # dataset. This is an explicit synthetic assumption, not Reddit data.
            base_votes = max(1, int(self.random.gauss(100 - i, 15)))
            downvotes = self.random.randint(0, int(base_votes * 0.3))

            # Mesa Agent.__init__ registers each new agent with the model.
            CommentAgent(
                model=self,
                comment_id=f"comment_{i:03d}",
                timestamp=i,
                upvotes=base_votes,
                downvotes=downvotes,
            )

    def get_raw_data(self) -> pd.DataFrame:
        """Return the complete comment dataset in deterministic timestamp order."""
        records = [
            {
                "comment_id": agent.comment_id,
                "timestamp": agent.timestamp,
                "upvotes": agent.upvotes,
                "downvotes": agent.downvotes,
                "net_score": agent.net_score,
            }
            for agent in self.agents
        ]
        return (
            pd.DataFrame(records)
            .sort_values(["timestamp", "comment_id"])
            .reset_index(drop=True)
        )

    def _reserved_rank_positions(self) -> list[int]:
        """Return zero-based positions spread through the top ten.

        With two reserved slots, positions 4 and 7 in human counting are used
        (zero-based indexes 3 and 6), rather than placing both at the bottom.
        """
        if self.reserved_slots == 0:
            return []
        return [
            int((index + 1) * 10 / (self.reserved_slots + 1))
            for index in range(self.reserved_slots)
        ]

    @staticmethod
    def _score_sort(df: pd.DataFrame) -> pd.DataFrame:
        """Stable ranking: score descending, then older timestamp, then ID."""
        return df.sort_values(
            ["net_score", "timestamp", "comment_id"],
            ascending=[False, True, True],
            kind="mergesort",
        )

    def _calculate_top10(self) -> pd.DataFrame:
        df = self.get_raw_data().copy()
        df["is_newer"] = df["timestamp"] >= self.newer_cutoff

        if self.reserved_slots == 0:
            top10 = self._score_sort(df).head(10).copy()
            top10["reserved_slot"] = False
        else:
            newer = self._score_sort(
                df[df["timestamp"] >= self.newer_cutoff]
            )
            reserved_picks = newer.head(self.reserved_slots).copy()
            reserved_ids = set(reserved_picks["comment_id"])

            general_pool = self._score_sort(
                df[~df["comment_id"].isin(reserved_ids)]
            )
            general_picks = iter(general_pool.to_dict("records"))
            reserved_picks_by_position = {
                position: row
                for position, row in zip(
                    self._reserved_rank_positions(),
                    reserved_picks.to_dict("records"),
                )
            }

            ordered_records = []
            for position in range(10):
                if position in reserved_picks_by_position:
                    row = dict(reserved_picks_by_position[position])
                    row["reserved_slot"] = True
                else:
                    row = dict(next(general_picks))
                    row["reserved_slot"] = False
                ordered_records.append(row)

            top10 = pd.DataFrame(ordered_records)

        top10 = top10.reset_index(drop=True)
        top10.insert(0, "rank_position", range(1, len(top10) + 1))
        return top10[
            [
                "rank_position",
                "comment_id",
                "timestamp",
                "upvotes",
                "downvotes",
                "net_score",
                "is_newer",
                "reserved_slot",
            ]
        ]

    def step(self):
        """Execute one model tick by applying the selected ranking mechanism."""
        self.last_ranking = self._calculate_top10()
        self.run_count += 1

    def get_ranked_top10(self) -> pd.DataFrame:
        """Return the most recent step result, running one step if needed."""
        if self.last_ranking is None:
            self.step()
        return self.last_ranking.copy()
