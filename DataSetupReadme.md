# Data setup

Once you have the ok for the ShotLink data, you can get the data in one fell swoop from our private data repo at https://github.com/aenfield/golf_course_project_data. 

This repo uses Git LFS, so before cloning it, you'll need to (once) install and configure Git LFS.

To install, use your package manager (works well with Homebrew, requires extra config on Ubuntu) or install the binary for your platform - for example, by downloading the installer and running it. Depending on how you install, you may need to afterwards run 'git lfs install' (again, just once) from a command prompt. Follow the details here: http://github.com/git-lfs/git-lfs#getting-started. See the 'Mac | Windows | Linux' links at the top for different platforms.

Then you should be able to clone the data repo, and run unzip.py to extract everything. On my machines, I've put the golf_course_project and golf_course_project_data repos at the same level (i.e., as children of the same parent directory), and code I've written assumes this location. 
