##again borrowed from openface project:
### https://github.com/cmusatyalab/openface/blob/master/models/get-models.sh
checkCmd() {
  command -v $1 >/dev/null 2>&1 \
    || die "'$1' command not found. Please install from your package manager."
}
##end of borrowed code

checkCmd wget
checkCmd bunzip2


if [ ! -f ./pose_iter_160000.caffemodel ]; then
    wget http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/mpi/pose_iter_160000.caffemodel
    [ $? -eq 0 ] || die "+ Error in wget."      
fi

if [ ! -f ./pose_deploy_linevec_faster_4_stages.prototxt ]; then
    wget https://raw.githubusercontent.com/CMU-Perceptual-Computing-Lab/openpose/master/models/pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt
      [ $? -eq 0 ] || die "+ Error in wget."
fi

checkCmd wget
checkCmd bunzip2

mkdir -p dlib
if [ ! -f dlib/shape_predictor_68_face_landmarks.dat ]; then
  wget -nv \
       http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2 \
       -O dlib/shape_predictor_68_face_landmarks.dat.bz2
  [ $? -eq 0 ] || die "+ Error in wget."
  bunzip2 dlib/shape_predictor_68_face_landmarks.dat.bz2
  [ $? -eq 0 ] || die "+ Error using bunzip2."
fi
