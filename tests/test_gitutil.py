# coding:utf-8

from __future__ import unicode_literals
import gitutil
import os
URLS = {
    "ssh": "git@github.com:guyskk/kkblog.git",
    "git": "git://github.com/guyskk/kkblog.git",
    "https": "https://github.com/guyskk/kkblog.git",
    "subversion": "https://github.com/guyskk/kkblog",
}

REPO_URL = "git@github.com:guyskk/webhooks_test.git"
REPO_EN = os.path.abspath("./__test_repo__/repo")
REPO_CN = os.path.abspath("./__test_repo__/中文路径仓库")
if not os.path.exists(REPO_EN):
    os.makedirs(REPO_EN)
if not os.path.exists(REPO_CN):
    os.makedirs(REPO_CN)


def test_pull_or_clone():
    err, ret = gitutil.pull_or_clone(REPO_URL, REPO_EN)
    assert not err
    err, ret = gitutil.pull_or_clone(REPO_URL, REPO_CN)
    assert not err


def test_modified_files():
    test_pull_or_clone()
    host, owner, repo = gitutil.parse_giturl(REPO_URL)
    t_en = gitutil.modified_files(os.path.join(REPO_EN, repo), "1a1bba5d3")
    t_cn = gitutil.modified_files(os.path.join(REPO_CN, repo), "1a1bba5d3")
    assert t_cn == t_en


def test_parse_giturl():

    for url in URLS.values():
        host, owner, repo = gitutil.parse_giturl(url)
        assert (host, owner, repo) == ("github.com", "guyskk", "kkblog")


def test_build_giturl():
    ("github.com", "guyskk", "kkblog")
    for k, v in URLS.items():
        url = gitutil.build_giturl("guyskk", "kkblog",
                                   style=k, host="github.com")
        assert url == v


def test_build_fileurl():
    url = gitutil.build_fileurl('guyskk', 'pygitutil', "readme.md", branch="master",
                                schema="https", host="github.com")
    assert url == "https://github.com/guyskk/pygitutil/raw/master/readme.md"
