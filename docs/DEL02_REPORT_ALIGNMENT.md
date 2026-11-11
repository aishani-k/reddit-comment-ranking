# DEL02.1 report alignment notes

Use this file as a checklist when updating the report so that the written report
matches the final code and output files.

## Revised inquiry question

How does reserving positions in the top ten of a Reddit-style discussion thread
for newer comments affect their visibility compared with ranking all comments
strictly by net vote score?

## Current targeted DEL02 slice

The prototype contains 100 synthetic comment agents. Each agent has a timestamp,
upvote count, downvote count, and net vote score. A `ThreadModel.step()` applies
one ranking condition and stores the resulting top ten.

- **Baseline:** zero reserved positions; all ten positions are selected by net
  vote score.
- **Alternative:** two positions are reserved for the highest-scoring comments
  with timestamps 50–99. The reserved positions are distributed through the
  top ten (positions 4 and 7); the other eight positions are filled by net vote
  score.
- **Controlled comparison:** both conditions use seed 42 and the same
  deterministic synthetic data. The experiment checks that the two raw
  dataframes are identical before saving the outputs.

## Output filenames

- `baseline_raw_00_comment_scores.csv`
- `baseline_processed_00_top10_ranking.csv`
- `alternative_raw_00_comment_scores.csv`
- `alternative_processed_00_top10_ranking.csv`

The processed files include `is_newer` and `reserved_slot` flags to make the
intervention visible. Do not claim the reserved comments are necessarily the
two lowest-scoring comments; they are the highest-scoring comments among the
newer half and may still rank highly overall.

## Important limitations

The prototype does not simulate readers, commenters, changing votes,
position-driven exposure, visible-score influence, handheld devices, laptops,
or Reddit's actual ranking algorithm. The source Mesa Epstein Civil Violence
model is preserved as the required starting example, but the project adaptation
does not reproduce civil-violence behaviour. It replaces that model's agents
and focal process with comment agents and a ranking rule.

## Suggested correction to the report's revision explanation

The original inquiry about vote-based comment visibility was retained and
narrowed into a runnable ranking comparison. The initial computational slice
uses synthetic comment states and compares vote-only sorting with a hybrid
ranking rule that reserves two top-ten positions for newer comments. Dynamic
reader behaviour and voting feedback are deferred because they require
additional behavioural assumptions and are outside this first implementation.

If the report still mentions handheld-device versus laptop scrolling, remove
that statement unless that comparison is actually implemented in the model.
