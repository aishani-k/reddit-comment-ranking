from pathlib import Path

from .model import ThreadModel


def run_experiment(output_dir: str | Path = "outputs") -> None:
    """Run baseline and alternative conditions and save DEL02 CSV outputs."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    baseline_model = ThreadModel(reserved_slots=0, seed=42)
    baseline_model.step()

    alternative_model = ThreadModel(reserved_slots=2, seed=42)
    alternative_model.step()

    baseline_raw = baseline_model.get_raw_data()
    alternative_raw = alternative_model.get_raw_data()

    # This is an essential experimental check: only the ranking rule changes.
    if not baseline_raw.equals(alternative_raw):
        raise RuntimeError(
            "Baseline and alternative starting datasets differ; "
            "the comparison is not controlled."
        )

    outputs = {
        "baseline_raw_00_comment_scores.csv": baseline_raw,
        "baseline_processed_00_top10_ranking.csv":
            baseline_model.get_ranked_top10(),
        "alternative_raw_00_comment_scores.csv": alternative_raw,
        "alternative_processed_00_top10_ranking.csv":
            alternative_model.get_ranked_top10(),
    }

    for filename, dataframe in outputs.items():
        dataframe.to_csv(output_path / filename, index=False)

    alternative_top10 = alternative_model.get_ranked_top10()
    reserved_count = int(alternative_top10["reserved_slot"].sum())

    print("Experiment complete.")
    print(f"Output directory: {output_path.resolve()}")
    for filename in outputs:
        print(f" - {filename}")
    print(
        "Comparison check: identical raw data in both conditions; "
        f"{reserved_count} newer comments occupy reserved positions."
    )


if __name__ == "__main__":
    run_experiment()
