#include <iostream>
#include <fstream>
#include <filesystem>
#include <memory>
#include <chrono>
#include <fstream>

#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>


//#include <direct.h>
//namespace fs = std::filesystem;
//#include "VideoDetector.h"
#include "AffdexException.h" //for StatusListener

//#include <PhotoDetector.h>
#include "ProcessStatusListener.h"
#include <FrameDetector.h>

#define PROCESS_BUFFER_SIZE 100

using namespace std;
using namespace affdex;


class StatusListener : public ProcessStatusListener {
private:
	std::mutex m;
	bool mIsRunning;
public:
	StatusListener() :mIsRunning(true) {}
	void onProcessingException(AffdexException ex) {
		std::cerr << "Affdex Exception: " << ex.what() << std::endl;
		m.lock();
		mIsRunning = false;
		m.unlock();
	}
	void onProcessingFinished() {
		m.lock();
		mIsRunning = false;
		m.unlock();
	}
	bool isRunning() {
		bool ret;
		m.lock();
		ret = mIsRunning;
		m.unlock();
		return ret;
	}
};

class AFaceListener : public FaceListener
{
	void onFaceFound(float timestamp, FaceId faceId)
	{
		std::cout << "Face id " << faceId << " found at timestamp " << timestamp << std::endl;
	}
	void onFaceLost(float timestamp, FaceId faceId)
	{
		std::cout << "Face id " << faceId << " lost at timestamp " << timestamp << std::endl;
	}
};

class FrameProcessor : public ImageListener {
private:
	std::ofstream mSaveFile;
	unsigned int mFrameCount = 0;
	unsigned int mBufferFrames = 0;
	unsigned int mProcessedFrames = 0;
	std::mutex mMutex;
public:
	//std::mutex mMutex;
	bool setCSVFile(std::string filename) {
		mSaveFile.open(filename);
		mFrameCount = 0;
		bool isOpened = mSaveFile.is_open();
		if (isOpened) {
			mSaveFile << "frame,timestamp";
			mSaveFile << ",joy,fear,anger,contempt,disgust,sadness,surprise";
			mSaveFile << ",engagement,valence";
			mSaveFile << ",age,gender,glasses,ethnicity";
			mSaveFile << ",smirk,attention,eyeWiden,FACS";
			mSaveFile << ",orientation";
			mSaveFile << endl;
		}
			//mSaveFile << "frame,timestamp,joy,engagement,valence,age" <<endl;
		return isOpened;
	}
	void closeFile() {
		if(mSaveFile.is_open())
			mSaveFile.close();
	}

	void onImageCapture(Frame image) {
		std::lock_guard<std::mutex> lg(mMutex);
		//cout << "Reading image " << image.getTimestamp() << std::endl;
		
	}
	void onImageResults(std::map< FaceId, Face > faces, Frame image)
	{
		std::lock_guard<std::mutex> lg(mMutex);
		//std::cout << "Number of faces " << faces.size() << std::endl;
		//getBufferSize();
		mBufferFrames++;
		if (faces.size() > 0) {
			for (auto& face_id_pair : faces) {				
				Face f = face_id_pair.second;
				mFrameCount++;
				std::string age_str[8] = { "Unknown", "< 18", "18-24", "25-34", "35-44", "45-54", "55-64","65+" };
				std::string gender_str[3] = { "Unknown", "Male", "Female" };
				std::string glasses_str[2] = { "False", "True" };
				std::string ethnicity_str[6] = { "UNKNOWN", "EUROPEAN", "AFRICAN", "SOUTH_ASIAN", "EAST_ASIAN", "HISP/POLY" };
				
				std::string feature_point_str;
				for (const auto& p : f.featurePoints) feature_point_str += "(" + to_string(p.x) + "," + to_string(p.y) +","+to_string(p.id) + "),";
				feature_point_str.pop_back();  //remove last comma
				feature_point_str = "[" + feature_point_str + "]";

				std::string facs_str;
				std::vector<int> facs_units = {
					12, 1, 2, 4, 9, 5, 15,
					17, 18, 24, 28, 27,
					43, 6,  7,  14, 20,
					26
				};
				/*std::string facs_actions[] = { 
					"Smile", "innerBrowRaise", "browRaise", "browFurrow", 
					"noseWrinkle", "upperLipRaise", "lipCornerDepressor",
					"chinRaise", "lipPucker", "lipPress", "lipSuck", "mouthOpen",
					"eyeClosure", "cheekRaise", "lidTighten", "dimpler", "lipStretch",
					"jawDrop"
				};*/
				float au_values[] = {
					f.expressions.smile, f.expressions.innerBrowRaise, f.expressions.browRaise, f.expressions.browFurrow,
					f.expressions.noseWrinkle, f.expressions.upperLipRaise, f.expressions.lipCornerDepressor,
					f.expressions.chinRaise, f.expressions.lipPucker, f.expressions.lipPress, f.expressions.lipSuck, f.expressions.mouthOpen,
					f.expressions.eyeClosure, f.expressions.cheekRaise, f.expressions.lidTighten, f.expressions.dimpler, f.expressions.lipStretch,
					f.expressions.jawDrop
				};
				for (int i = 0; i < facs_units.size(); i++) {
					facs_str += to_string(facs_units[i]) +": " + to_string(au_values[i]) +"," ;
				}
				facs_str.pop_back();
				facs_str = "\"{" + facs_str + "}\"";

				/*
				std::cout << "Frame = " << mFrameCount<< std::endl;				
				std::cout << "Engagement = " << f.emotions.engagement << std::endl;
				std::cout << "Valence = " << f.emotions.valence << std::endl;
				std::cout << "age = " << age_str[f.appearance.age] << std::endl;
				std::cout << "gender = " << gender_str[(int)f.appearance.gender] << std::endl;
				std::cout << "glasses = " << glasses_str[(int)f.appearance.glasses] << std::endl;
				std::cout << "ethnicity = " << ethnicity_str[(int)f.appearance.glasses] << std::endl;
				std::cout << "quality = " << f.faceQuality.brightness << endl;
				std::cout << "points = " << feature_point_str << endl; */
				
				if (mSaveFile.is_open()) {
					mSaveFile << mFrameCount << "," << image.getTimestamp() << ","

						<< f.emotions.joy << "," << f.emotions.fear << "," <<
						f.emotions.anger << "," << f.emotions.contempt << "," <<
						f.emotions.disgust << "," << f.emotions.sadness << "," <<
						f.emotions.surprise

						<< "," << to_string(f.emotions.engagement) << "," << to_string(f.emotions.valence)

						<< "," << age_str[f.appearance.age] <<"," << gender_str[(int)f.appearance.gender] <<","
						   << glasses_str[(int)f.appearance.glasses] << "," << ethnicity_str[(int)f.appearance.ethnicity]
						
						<<","<<f.expressions.smirk<<","<<f.expressions.attention<<","<<f.expressions.eyeWiden
						<<","<<facs_str
						<<",\"("<<f.measurements.orientation.pitch<<","<<f.measurements.orientation.roll<<","<<f.measurements.orientation.yaw<<")\""
						<< endl						
						;
				}
				//std::cout << "gender = %s" << f.appearance.gender << std::endl;
				//std::cout << "ethnicity = %s" << f.appearance.ethnicity << std::endl;
			}
		}
		//mBufferFrames--;
		mProcessedFrames++;
	}
	unsigned int getBufferFrames() {
		std::lock_guard<std::mutex> lg(mMutex);
		return mBufferFrames;
	}
	unsigned int getProcessedFrames() {
		std::lock_guard<std::mutex> lg(mMutex);
		return mProcessedFrames;
	}
	void resetBufferCounter() {
		std::lock_guard<std::mutex> lg(mMutex);
		mBufferFrames = 0;
	}
};

/* //todo refactor
class SampleIterator {
	SampleIterator(std::string sampleDirectory) {
		mSampleDir = sampleDirectory;
	}
private:
	std::string mSampleDir;
};*/

class AffdexExtractor{
public:
	AffdexExtractor() : mDetector(PROCESS_BUFFER_SIZE), mFrameProcPtr(new FrameProcessor()){
		mSampleDir = "C:\\Users\\shath\\Documents\\projects\\affective-movie-evaluator\\data\\";
		mVideoPath = "";
		mWriteCSV = true;
		//initDetector();
	}
	void initDetector() {
		int process_framerate = 30;
		int nFaces = 1;
		int faceDetectorMode = (int)FaceDetectorMode::LARGE_FACES;
		//mFrameProcPtr = std::make_shared<FrameProcessor>();
		mStatusListenerPtr = std::make_shared<StatusListener>();
		//std::shared_ptr<Detector> detector;
		//PhotoDetector detector = PhotoDetector(2);
		//shared_ptr<FrameProcessor> listenPtr(new FrameProcessor());
		//shared_ptr<StatusListener> statusListenerPtr = std::make_shared<StatusListener>();

		//mDetector = FrameDetector(PROCESS_BUFFER_SIZE);
		affdex::path classifierPath(L"C:\\Program Files\\Affectiva\\AffdexSDK\\data");
		mDetector.disableAnalytics();
		mDetector.setClassifierPath(classifierPath);
		mDetector.setDetectAllEmotions(true);
		mDetector.setDetectAllAppearances(true);
		mDetector.setDetectAge(true);
		mDetector.setDetectAllExpressions(true);
		mDetector.setImageListener(mFrameProcPtr.get());
		mDetector.setProcessStatusListener(mStatusListenerPtr.get());
	}
	bool selectSample(std::string sample_id) {
		return selectSample(sample_id, false);
	}
	bool selectSample(std::string sample_id, bool gsr) {
		mDetector.reset();
		std::string sampleDir = getSampleDir(sample_id);
		
		if (filesystem::exists(sampleDir)) {
			std::string featurePath = getFeaturePath(sample_id);
			std::string videoPath = getInputVideoPath(sample_id,gsr);
			create_directory(getOutputDir(sample_id));
			mVideoPath = videoPath;
			if (mWriteCSV) {
				mFrameProcPtr.get()->setCSVFile(featurePath);
			}
			return true;
		}
		else {
			mVideoPath = "";
			return false;
		}
	}

	bool startExtracting() {
		std::lock_guard<std::mutex> lg(mMutex);
		if(mVideoPath.length() == 0){
			cerr << "AffdexExtractor: Videopath was null" << endl;
			return false;
		}
		cv::VideoCapture videoCapture(mVideoPath);
		cv::Mat frame;
		if (!videoCapture.isOpened()) {
			cout << "Cannot open file! " << mVideoPath << endl;
			return false;
		}
		//double fps = videoCapture.get(cv::CAP_PROP_FPS);
		double frame_count = videoCapture.get(cv::CAP_PROP_FRAME_COUNT);

		float time_stamp = 0.0f;
		unsigned int frame_n = 0;
		mDetector.start();
		while (true) {
			for (unsigned int i = 0; i < mFrameBufferSize; i++) {
				videoCapture >> frame;
				if (!frame.empty()) {
					double pos_ms = videoCapture.get(cv::CAP_PROP_POS_MSEC);
					double pos_ratio = videoCapture.get(cv::CAP_PROP_POS_AVI_RATIO);
					cout << "Position = " << pos_ratio << endl;
					affdex::Frame f(frame.size().width, frame.size().height, frame.data, Frame::COLOR_FORMAT::BGR, (float)pos_ms);
					time_stamp++;
					mDetector.process(f);
					//cv::imshow("Output", frame);
					//cv::waitKey(24);
					frame_n++;
				}
			}


			cout << "Processed frames=" << mFrameProcPtr->getProcessedFrames() << "/" << frame_count << " sent Frame #=" << frame_n << endl;
			if (mFrameProcPtr->getProcessedFrames() != frame_n - 1) {
				std::cout << "Waiting for frames to be processed!" << endl;
			}
			while (mFrameProcPtr->getProcessedFrames() < frame_n - 1) {
			}

			if (mFrameProcPtr->getProcessedFrames() >= frame_count) {
				break;
			}

		}	

		if (mWriteCSV) {
			mFrameProcPtr->closeFile();
		}
		
		videoCapture.release();
		
		mVideoPath = "";
		return true;
	}
	void done() {
		mDetector.stop();
	}
private:
	/** 
	* Returns the fullpath of the affdex output directory.
	**/
	std::string getSampleDir(std::string sample_id) {
		return mSampleDir + sample_id;
	}
	std::string getOutputDir(std::string sample_id) {
		return getSampleDir(sample_id) + "\\affdex_output";
	}
	std::string getFeaturePath(std::string sample_id) {
		return getOutputDir(sample_id) + "\\features.csv";
	}
	std::string getInputVideoPath(std::string sample_id, bool gsr) {
		return getSampleDir(sample_id) + (gsr?"\\gsrsample.avi":"\\sample.avi");
	}
	std::string getInputVideoPath(std::string sample_id) {
		return getInputVideoPath(sample_id, false);
	}
	void create_directory(std::string save_path) {
		if (filesystem::exists(save_path)) {
			cout << "Save path already exists.. Overwriting to savepath" << endl;
		}
		else {
			filesystem::create_directory(save_path);
			cout << "Affdex folder created";
		}
	}
	std::string mVideoPath, mSampleDir;
	unsigned int mFrameBufferSize = PROCESS_BUFFER_SIZE;
	shared_ptr<FrameProcessor> mFrameProcPtr;
	shared_ptr<StatusListener> mStatusListenerPtr;
	FrameDetector mDetector;
	bool mWriteCSV = false;
	std::mutex mMutex;
};


int main(int argc, char* argv[]) {
	//R* dir;
	/*std::string video_path = "C:\\Users\\shath\\Documents\\projects\\affective-movie-evaluator\\data\\0efad150-04cd-47d5-bd2d-0594662b7064\\sample.avi";

	std::string save_path = "C:\\Users\\shath\\Documents\\projects\\affective-movie-evaluator\\data\\0efad150-04cd-47d5-bd2d-0594662b7064\\affdex_output";
	std::string csv_path = "C:\\Users\\shath\\Documents\\projects\\affective-movie-evaluator\\data\\0efad150-04cd-47d5-bd2d-0594662b7064\\affdex_output\\features.csv";
	*/
	//affdex::path videoPath(L"C:\\Users\\shath\\Documents\\projects\\affective-movie-evaluator\\data\\0efad150-04cd-47d5-bd2d-0594662b7064\\sample.avi");
	//affdex::path videoPath(L"C:/Users/shath/Documents/projects/affective-movie-evaluator/data/0efad150-04cd-47d5-bd2d-0594662b7064/sample.avi");
	

	std::string path = "C:\\Users\\shath\\Documents\\projects\\affective-movie-evaluator\\data";
	//std::string path = "../";
	for (const auto& entry : filesystem::directory_iterator(path))
	{
		if (entry.is_directory()) {
			std::string sample_path = entry.path().string();
			std::cout << sample_path << std::endl;
			std::string sample_id = entry.path().filename().string();
			cout << "Processing " << sample_id << endl;

			AffdexExtractor extractor;
			extractor.initDetector();
			extractor.selectSample(sample_id, false);
			extractor.startExtracting();
			extractor.done();
			/*
			for (const auto& sampleFile : filesystem::directory_iterator(sample_path)) {
				std::string file_name = sampleFile.path().filename().string();
				std::string ext = sampleFile.path().extension().string();
				std::cout << "\t" << file_name << std::endl;
			}*/
		}
	}
	/*{
		AffdexExtractor extractor;
		extractor.initDetector();
		extractor.selectSample("0efad150-04cd-47d5-bd2d-0594662b7064", true);
		extractor.startExtracting();
		extractor.done();
	}

	{
		AffdexExtractor extractor;
		extractor.initDetector();
		extractor.selectSample("2af52810-851b-4b16-a2f6-629b502d1e5a", true);
		extractor.startExtracting();
		extractor.done();
	}*/
	
	return 0;

	//shared_ptr<FrameProcessor> listenPtr(new FrameProcessor());
	//shared_ptr<StatusListener> statusListenerPtr = std::make_shared<StatusListener>();
	//std::shared_ptr<FrameProcessor> imgListener(new FrameProcessor());
	
	/*
	if (filesystem::exists(save_path)) {
		cout << "Save path already exists.. Overwriting to savepath" << endl;
	}
	else {
		filesystem::create_directory(save_path);
		cout << "Affdex folder created";
	}

	int process_framerate = 30;
	int nFaces = 1;
	int faceDetectorMode = (int)FaceDetectorMode::LARGE_FACES;
	//std::shared_ptr<Detector> detector;
	//PhotoDetector detector = PhotoDetector(2);
	FrameDetector detector = FrameDetector(PROCESS_BUFFER_SIZE);
	

	affdex::path classifierPath(L"C:\\Program Files\\Affectiva\\AffdexSDK\\data");
	detector.disableAnalytics();
	detector.setClassifierPath(classifierPath);
	detector.setDetectAllEmotions(true);
	detector.setDetectAllAppearances(true);
	detector.setDetectAge(true);
	detector.setDetectAllExpressions(true);	
	detector.setImageListener(listenPtr.get());
	detector.setProcessStatusListener(statusListenerPtr.get());

	//detector = std::make_shared<VideoDetector>(process_framerate, nFaces,
	//											(affdex::FaceDetectorMode) faceDetectorMode);
	listenPtr.get()->setCSVFile(csv_path);
	cv::VideoCapture videoCapture(video_path);
	cv::Mat image;
	if (!videoCapture.isOpened()) {
		cout << "Cannot open file! " << video_path << endl;
		return -1;
	}

	double fps = videoCapture.get(cv::CAP_PROP_FPS);
	double frame_count = videoCapture.get(cv::CAP_PROP_FRAME_COUNT);
	
	
	//cv::namedWindow("Output", 1);
	//filesystem::exists(L"c:\\");
	cv::Mat frame;
	detector.start();
	float time_stamp = 0.0f;
	unsigned int frame_n = 0;
	std::cout << "FrameCount = " << frame_count << endl;
	while (true) {
	
		for (int i = 0; i < PROCESS_BUFFER_SIZE; i++) {
			videoCapture >> frame;
			if (!frame.empty()) {
				double pos_ms = videoCapture.get(cv::CAP_PROP_POS_MSEC);
				double pos_ratio = videoCapture.get(cv::CAP_PROP_POS_AVI_RATIO);
				//cout << "Position = " << pos_ratio << endl;

				affdex::Frame f(frame.size().width, frame.size().height, frame.data, Frame::COLOR_FORMAT::BGR, (float)pos_ms);
				time_stamp++;
				detector.process(f);
				frame_n++;
			}
		}

		cout << "Processed frames=" << listenPtr->getProcessedFrames() << " sent Frame #="<<frame_n<< endl;
		if (listenPtr->getProcessedFrames() != frame_n - 1) {
			std::cout << "Waiting for frames to be processed!"<<endl;
		}
		while (listenPtr->getProcessedFrames() < frame_n-1) {}

		if (listenPtr->getProcessedFrames() >= frame_count) {
			break;
		}
		

		//if (!statusListenerPtr->isRunning())
		//	break;
		//cv::imshow("Output", frame);
		//cv::waitKey(24);
		//cv::waitKey(1);

	}
	listenPtr.get()->closeFile();
	detector.stop();
	videoCapture.release();
	*/

	/*
	std::string path = "C:\\Users\\shath\\Documents\\projects\\affective-movie-evaluator\\data";	
	//std::string path = "../";
	for (const auto& entry : filesystem::directory_iterator(path))
	{
		if (entry.is_directory()) {
			std::string sample_path = entry.path().string();
			std::cout << sample_path << std::endl;		
			for (const auto& sampleFile: filesystem::directory_iterator(sample_path)){
				std::string file_name = sampleFile.path().filename().string();
				std::string ext = sampleFile.path().extension().string();
				std::cout <<"\t"<< file_name << std::endl;
			}
		}
	}
	*/
}