# pp install gitpython

import git
git_dir = 'C:/Data/SDR_Git/SDR_Scripting'
g = git.cmd.Git(git_dir)
g.pull()
