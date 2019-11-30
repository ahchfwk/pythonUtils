cd $1
cd ..
nicad4 functions java $2
mv *_functions-clones/* /home/fdse/fwk/nicad/NiCad-4.0/detectResult/
rm -r *_functions.xml *.log *_functions-clones

