# GitHub submission checklist

1. Copy the contents of this project folder into the existing `reddit-comment-ranking` repository.
2. Confirm `src/civil_violence/` contains the preserved Mesa example and `SOURCE.md`.
3. Commit the four files in `outputs/`, the project model, tests, README, and requirements.
4. From a clean environment, follow the README setup and run commands.
5. Run `python -m unittest discover -s tests -v`.
6. Confirm all four CSV files are regenerated.
7. Create an annotated tag named `DEL02` with message:
   `DEL02.2 - Submission - Initial Computational Prototype`
8. Create a GitHub Release from that tag named `DEL02 Release`.
9. Include short release notes describing the baseline/alternative comparison, run command, and limitations.
10. Submit the release URL in the DEL02.2 field and the repository URL in DEL02.1.

Do not claim the GitHub release is complete until the tag and release exist on GitHub.
