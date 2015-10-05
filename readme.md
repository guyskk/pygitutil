# Python Git Util

Python Git Util call git from shell, so you should have git installed before getting started.

This package can deal with different encoding of shells, all params must be unicode string.


## Install

    pip install pygitutil


## Usage

### operate url

- parse_giturl
- build_giturl
- build_fileurl

```python
>>> from gitutil import gitutil,shell
>>> gitutil.parse_giturl("git@github.com:guyskk/pygitutil.git")
('github.com', 'guyskk', 'pygitutil')
>>> gitutil.parse_giturl("https://github.com/guyskk/pygitutil.git")
('github.com', 'guyskk', 'pygitutil')
>>> gitutil.build_giturl('guyskk', 'pygitutil', host='github.com')
u'https://github.com/guyskk/pygitutil.git'
>>> gitutil.build_giturl('guyskk', 'pygitutil', host='github.com',style="ssh")
u'git@github.com:guyskk/pygitutil.git'
>>> gitutil.build_fileurl('guyskk', 'pygitutil', "readme.md", branch="master",
                  schema="https", host="github.com")
... u'https://github.com/guyskk/pygitutil/raw/master/readme.md'
>>> 
```

### clone,pull,diff

```python
clone(repo_url, dest)
pull(repo_url, dest, branch="master")
pull_or_clone(repo_url, dest, branch="master")
--> (err,return_value)

modified_files(dest, repo_url, commit1, commit2=None)
--> [(status, filepath),...]

```

### shell

```python
>>> from gitutil import gitutil,shell
>>> h=shell.run("python --help")
>>> h
(None, u"usage: python [option] ... 
>>> h=shell.run("python --h")
>>> h
(CalledProcessError(), None)
>>> 
>>> h=shell.run(["echo",u"中文"])
>>> h
(None, u'\u4e2d\u6587\r\n')
>>>
```


## Test

    py.test
    
or

    tox

## license 

MIT License