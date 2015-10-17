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


def setup_module(module):
    test_pull_or_clone()


def test_pull_or_clone():
    err, ret = gitutil.pull_or_clone(REPO_URL, REPO_EN)
    assert not err
    err, ret = gitutil.pull_or_clone(REPO_URL, REPO_CN)
    assert not err


def test_modified_files():

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


def test_git_log():
    host, owner, repo = gitutil.parse_giturl(REPO_URL)
    t_en = gitutil.git_log(os.path.join(REPO_EN, repo))
    t_cn = gitutil.git_log(os.path.join(REPO_CN, repo))
    expect = [(u'e744949159ecea5a9f68a1715e8d1e4fafd87dea', u'guyskk', u'1316792450@qq.com', u'Sun Sep 27 15:24:39 2015 +0800', u'add md'),
              (u'1a1bba5d3c2a4958644e4bbfb1a4ebb8abfafd23', u'kk', u'1316792450@qq.com', u'Sun Sep 27 11:51:26 2015 +0800', u'Initial commit')]
    assert len(t_en) >= 2
    assert t_en[-2:] == expect
    assert t_cn == t_en
