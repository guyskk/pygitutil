# coding:utf-8

from __future__ import unicode_literals
import os
import re
from . import shell

FORMATS = {
    'https or http or subversion':
    re.compile(r'^http[s]://(.*)/([^/]*)/([^/]*?)(?:\.git|)$'),
    'ssh': re.compile(r'^git@(.*):([^/]*)/([^/]*)\.git$'),
    'git': re.compile(r'^git://(.*)/([^/]*)/([^/]*)\.git$'),
}

URL_TEMPLATE = {
    "https": "https://{host}/{owner}/{repo}.git",
    "ssh": "git@{host}:{owner}/{repo}.git",
    "git": "git://{host}/{owner}/{repo}.git",
    "subversion": "https://{host}/{owner}/{repo}",
}


def parse_giturl(url):
    """parse_giturl

    :return: tuple(host,owner,repo)
    """
    for p in FORMATS.values():
        ret = p.findall(url)
        if ret:
            return ret[0]
    raise ValueError("invalid url: %s" % url)


def build_giturl(owner, repo, style="https", host="github.com"):
    """build_giturl
    :param stype: https ssh git or subversion
    :return: git repo url
    """
    if style not in URL_TEMPLATE:
        raise ValueError("invalid style: %s" % style)

    return URL_TEMPLATE[style].format(owner=owner, repo=repo, host=host)


def to_https_url(repo_url):
    host, owner, repo = parse_giturl(repo_url)
    return build_giturl(owner, repo, host=host)


def build_fileurl(owner, repo, filepath, branch="master",
                  schema="https", host="github.com"):
    """build_fileurl

    :return: url for file on github/gitlab
    """
    tmpl = "{schema}://{host}/{owner}/{repo}/raw"\
           "/{branch}/{filepath}"
    return tmpl.format(owner=owner, repo=repo, filepath=filepath,
                       branch=branch, schema=schema, host=host)


def clone(repo_url, dest):
    """git clone"""

    host, owner, repo = parse_giturl(repo_url)
    repo_url = build_giturl(owner, repo, host=host, style="https")
    assert type(repo_url) == unicode
    cwd = os.path.join(dest, repo)
    if os.path.exists(cwd):
        raise IOError("repo already exists: %s" % cwd)
    if not os.path.exists(dest):
        os.makedirs(dest)
    return shell.run(["git", "clone", repo_url], cwd=dest)


def pull(repo_url, dest, branch="master"):
    """git pull"""
    host, owner, repo = parse_giturl(repo_url)
    repo_url = build_giturl(owner, repo, host=host, style="https")
    cwd = os.path.join(dest, repo)
    if not os.path.exists(cwd):
        raise IOError("repo not exists: %s" % cwd)
    return shell.run(["git", "pull", repo_url, branch], cwd=cwd)


def pull_or_clone(repo_url, dest, branch="master"):
    """执行git pull，如果本地仓库不存在则自动执行git clone"""
    __, __, repo = parse_giturl(repo_url)
    cwd = os.path.join(dest, repo)
    if not os.path.exists(cwd):
        return clone(repo_url, dest)
    else:
        return pull(repo_url, dest, branch)


def modified_files(dest, commit1, commit2=None):
    """branch=master

    出现乱码问题需要执行:

        git config core.quotepath false

    Possible status letters are:

        A: addition of a file
        C: copy of a file into a new one
        D: deletion of a file
        M: modification of the contents or mode of a file
        R: renaming of a file
        T: change in the type of the file
        U: file is unmerged (you must complete the merge before it can be committed)
        X: "unknown" change type (most probably a bug, please report it)
    """
    # __, __, repo = parse_giturl(repo_url)
    # cwd = os.path.join(dest, repo)
    # if not os.path.exists(cwd):
    #     raise IOError("repo not exists: %s" % cwd)

    cmd = ["git", "diff", "--name-status", "--raw", commit1]
    if commit2:
        cmd.append(commit2)
    shell.run(["git", "config", "core.quotepath", "false"], cwd=dest)
    err, ret = shell.run(cmd, cwd=dest)
    if err:
        raise err
    result = []
    for line in ret.split("\n"):
        if line != "":
            status, filepath = tuple(line.split("\t"))
            filepath = filepath.strip("\"")
            result.append((status, filepath))
    return result
