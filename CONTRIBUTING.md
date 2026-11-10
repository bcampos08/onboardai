# How we work in this repository

These rules keep everyone's work separate until it has been reviewed and tested, so that integration problems are caught in a pull request instead of at the deadline.

## 1. Branching strategy

`main` always holds working, reviewed code. Nobody pushes to `main` directly; GitHub blocks it.

All work happens on a short-lived branch created from the latest `main`:

| Prefix | Use for | Example |
| --- | --- | --- |
| `feature/` | New functionality | `feature/escalation-api` |
| `fix/` | Bug fixes | `fix/citation-page-number` |
| `test/` | Adding or improving tests | `test/llm-gateway-timeouts` |
| `docs/` | Documentation changes | `docs/update-contracts` |

```bash
git switch main
git pull
git switch -c feature/escalation-api
# ...make changes and commit...
git push -u origin feature/escalation-api
```

Then open a pull request on GitHub. Keep branches small: one component or one task per branch, merged within a few days.

## 2. Pull requests and peer review

A pull request can be merged only when:

1. **At least one teammate other than the author has approved it.**
2. **All CI checks pass.** GitHub Actions runs the tests automatically on every pull request.
3. All review comments are resolved.

Reviewers check that the code works, that it follows the interface contracts, and that it has tests. Use **Request changes** when something must be fixed and **Approve** when it is ready. Give specific, kind feedback, and explain the reason for each requested change.

Merge with **Squash and merge**, then delete the branch.

## 3. Keeping components compatible

Most integration problems come from mismatched JSON field names, API paths, or function names. To prevent that:

- **Section 3 of the Design Specification (in `docs/`) is the source of truth** for API paths, JSON fields, and Python interfaces.
- If your code needs a contract change, update `docs/` in the **same pull request** and request a review from the owner of that section.
- Use the component names from the architecture diagram in code, issues, and branch names.
- Before opening a pull request, update your branch with the latest `main` and run the tests:

```bash
git switch main && git pull
git switch feature/your-branch
git merge main
cd backend && pytest
```

## 4. Resolving merge conflicts

1. The **pull request author** resolves conflicts on their branch, not on `main`.
2. If the conflict touches someone else's code, talk to that person before choosing a version.
3. After resolving, run the tests again and push. Reviewers re-check the conflicting files.

## 5. Policy for AI-generated code

AI tools are welcome for writing tests, finding bugs, and suggesting improvements, but **AI output is treated like code from a new teammate: it is never merged without human review and passing tests.**

1. **Disclose it.** Tick the AI section of the pull request template and say what the AI was used for.
2. **Understand it.** The author must be able to explain every AI-generated line during review.
3. **Verify it.** Check that suggested libraries, functions, and facts exist and work as claimed. AI tools can invent APIs.
4. **Test it.** AI-generated code needs passing tests. AI-generated tests must be checked to make sure they would actually fail if the code were wrong.
5. **Independent review.** The approving reviewer cannot be the person who prompted the AI.
6. **Protect data.** Never paste API keys, passwords, `.env` contents, or real company or employee data into an AI tool.
7. **Respect ownership.** If an AI tool edits a file owned by a teammate, that teammate must approve the change.

## 6. Commit messages

Write short, present-tense messages that say what changed: `Add timeout fallback to LLM Gateway`, not `fixed stuff`.

## 7. Secrets

Never commit `.env` or API keys. Copy `.env.example` to `.env` for local settings. If a secret is committed by accident, tell the team immediately and rotate the key.
