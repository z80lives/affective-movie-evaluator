##again borrowed from openface project:
### https://github.com/cmusatyalab/openface/blob/master/models/get-models.sh
checkCmd() {
  command -v $1 >/dev/null 2>&1 \
    || die "'$1' command not found. Please install from your package manager."
}
##end of borrowed code

checkCmd wget

if [ ! -f ./_mini_XCEPTION.102-0.66.hdf5 ]; then
    wget -O _mini_XCEPTION.102-0.66.hdf5 https://github.com/omar178/Emotion-recognition/blob/master/models/_mini_XCEPTION.102-0.66.hdf5?raw=true
    [ $? -eq 0 ] || die "+ Error in wget."      
fi

if [ ! -f ../haarcascade_files/haarcascade_frontalface_default.xml ]; then
      wget -P ../haarcascade_files/ https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
      [ $? -eq 0 ] || die "+ Error in wget."
fi


if [ ! -f ./mmod_human_face_detector.dat.bz2 ]; then
    wget https://github.com/davisking/dlib-models/raw/master/mmod_human_face_detector.dat.bz2
    [ $? -eq 0 ] || die "+ Error in wget."      
    bunzip2 mmod_human_face_detector.dat.bz2
    [ $? -eq 0 ] || die "+ Error using bunzip2."
fi

