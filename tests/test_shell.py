# coding:utf-8

from gitutil import shell


def test_base():
    err, ret = shell.run(["python", "-h"])
    assert not err
    assert type(ret) == unicode
    err, ret = shell.run(["git", "--help"])
    assert not err
    assert type(ret) == unicode


def test_unicode():
    words = [u"haha", u"中文", u"哈哈"]
    for w in words:
        err, ret = shell.run(["echo", w])
        assert not err
        assert type(ret) == unicode
        assert ret.strip() == w
