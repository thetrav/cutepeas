# py2exe #

I've been using the py2exe app, http://www.py2exe.org/.
Once you've got the right modules installed you should be able to build the app by opening a command prompt, navigating to the src dir and then running:
python setup.py py2exe

That'll produce a lot of output, probably warn about some missing packages, and create a folder called build and a folder called dist.

To do upgrades I just grab the library.zip file out of the dist folder, it's got all the cutepeas python code in it.