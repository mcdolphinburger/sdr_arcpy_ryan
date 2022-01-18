# pp install gitpython

import git
repo = git.Repo('C:/Data/SDR_Git/SDR_Scripting')
repo.remotes.origin.pull()

current = repo.head.commit
repo.remotes.origin.pull()