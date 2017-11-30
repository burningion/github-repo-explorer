# Github Repo Explorer
Exploring Pull Requests Using Requests and IPython

# What is this?

This is an example Python3 program to load all of an organization's pull requests into memory.

It then jumps into an IPython shell, allowing you to explore and interact with a dictionary containing each of the organization's Repositories and Pull Requests.

It's a good starting point for understanding how both `pagination` and `requests` work in Python 3.

# How do I get it running?

You'll need Python 3, `requests`, `IPython`, and ar installed.

Once you've got Python 3 installed, you can do a:

```bash
$ python3 -m pip install requests ipython
```

...And you're ready to go!

# Usage

```bash
$ python3 pull_requests.py -token YOURGITHUBTOKEN -org THEORGYOUWANTTOSEE
```

