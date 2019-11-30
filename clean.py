import os,sys
import shutil

src = "C-C++_releases/"
tar = "c++_c_src/"
suffix = (".cpp",".c",".h",".hpp",".hxx",".cc",".C",".cxx",".C++")
repos = os.listdir("C-C++_releases")
for r in repos:
    if os.path.isdir("C-C++_releases/"+r):
        for root,dir,f in os.walk(r):
            if f.endswith(suffix):
                if not os.path.exists("c++_c_src/"+root[15:]):
                    os.makedirs("c++_c_src/"+root[15:])
                shutil.copyfile(os.path.join(root,f), os.path.join("c++_c_src/"+root[15:],r))
