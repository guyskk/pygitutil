# coding:utf-8

from __future__ import unicode_literals
from subprocess import check_output, CalledProcessError
import sys


def run(args, **kwargs):
    """safety call check_output,
    All string params must be unicode string

    :return: tuple(err,return_value)
    """
    err = None
    ret = None
    if sys.__stdin__.encoding is None:
        encoding = "utf-8"
    else:
        encoding = sys.__stdin__.encoding
    if isinstance(args, list):
        encoded_args = [s.encode(encoding) for s in args if s is not None]
    else:
        encoded_args = args.encode(encoding)
    if "cwd" in kwargs:
        cwd = kwargs["cwd"]
        assert type(cwd) == unicode, "All string params must be unicode string"
        # encode cwd to correct str
        kwargs["cwd"] = cwd.encode(sys.getfilesystemencoding())
    try:
        ret = check_output(encoded_args, **kwargs)
    except (OSError, CalledProcessError):
        try:
            ret = check_output(args, shell=True)
        except (OSError, CalledProcessError) as ex:
            err = ex
    if ret is not None:
        encodings = [sys.stdout.encoding, "utf-8", "gbk",
                     sys.getfilesystemencoding(), sys.getdefaultencoding()]
        encodings = [x for x in encodings if x is not None]
        ex = None
        for enco in encodings:
            try:
                ret = ret.decode(enco)
                break
            except UnicodeDecodeError as ex:
                pass
        if type(ret) != unicode:
            raise ValueError("Can't decode return value")
    return err, ret
