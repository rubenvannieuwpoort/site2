from pathlib import Path
from collections import defaultdict
import subprocess


class CommitNotFoundError(Exception):
    pass


class CommitMessageNotUniqueError(Exception):
    pass


def get_commit_from_msg(msg, repo):
    cmd = ["git", "log", "--format=%H %s"]
    commits = list(map(
        lambda line: line.split(' ', 1),
        subprocess.check_output(cmd, text=True, cwd=repo).splitlines(),
    ))

    commit_msg_map = defaultdict(list)

    for commit_sha, commit_msg in commits:
        commit_msg_map[commit_msg] += [commit_sha]

    commits_with_matching_msg = commit_msg_map.get(msg, [])

    if len(commits_with_matching_msg) == 0:
        raise CommitNotFoundError

    if len(commits_with_matching_msg) > 1:
        raise CommitMessageNotUniqueError

    return commits_with_matching_msg[0]


def get_diff_from_commit(commit, repo):
    cmd = ["git", "show", "--format=", "--patch", commit]
    diff = subprocess.check_output(cmd, text=True, cwd=repo)
    return diff



def diff_for_commit_message(repo: str | Path, msg: str) -> str:
    commit = get_commit_from_msg(msg, repo)
    return get_diff_from_commit(commit, repo)
