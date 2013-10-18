githooks-pwfilter
=================

The pwfilter git-hook offers automatic removal/insertion of sensitive data in
public repositories. This way passwords and other sensitive data can be
removed automatically before a commit and restored afterwards.


Dependencies
------------
The hook itself needs Python (tested with 2.7.5 and 3.3.2) and uses
[pass](http://zx2c4.com/projects/password-store/) which in turn uses gpg to
encrypt its passwords. You'll probably want to use a gpg-agent.
This should really be re-written as a shell script so as to drop the Python dependency.


How it works
------------

In the working tree of the project that you want to be filtered, you need a file named filter (ingenious, I know). This file should contain relative paths to all files you want to filter. So if you want a file such as `@gitdir@/ssh/config` to be filtered put
`ssh/config` into the filter file.

The so specified path needs to be matched with an equally named pass entry which I'll just call filter from here on out. So for the previous example you would need to have a filter in `gitfilter/ssh/config` with `gitfilter` being a fixed prefix.

Inside each filter you can specify as many rules as you need for the file that should be filtered. Each rule looks like this: `REPLACEMENT:PASSWORD`. Upon `git commit` all strings matching PASSWORD will be replaced with REPLACEMENT before the commit is actually done. After committing the filter is inversed, so you'll get your passwords back. The same happens when the project is pulled/merged.


Installation
------------

Just call the install script:

    ./install PATH_TO_PROJECT_YOU_WANT_TO_FILTER
This installs three hooks: post-commit, post-merge, pre-commit.
Should you already have your own hooks, these will be replaced. So be careful and make a pull-request for your merge script.

Because hooks are not actually part of the git repo, the installation has to be repeated everytime you clone your project. You could add `githooks-pwfilter` as a submodule so you'll remember to install it.
