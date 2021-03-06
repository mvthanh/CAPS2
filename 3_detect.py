# -*- coding: utf-8 -*-
import cv2
import digit_detector.region_proposal as rp

import digit_detector.detect as detector
import digit_detector.file_io as file_io
import digit_detector.preprocess as preproc
import digit_detector.classify as cls
import ImgProcess.DetectDigit as ImgProcess

detect_model = "detector_model.hdf5"
recognize_model = "recognize_model.hdf5"

mean_value_for_detector = 200
mean_value_for_recognizer = 200

model_input_shape = (32, 32, 1)
DIR = './data'

if __name__ == "__main__":
    # 1. image files
    img_files = file_io.list_files(directory=DIR, pattern="*.jpg", recursive_option=False, n_files_to_sample=None,
                                   random_order=False)

    preproc_for_detector = preproc.GrayImgPreprocessor(mean_value_for_detector)
    preproc_for_recognizer = preproc.GrayImgPreprocessor(mean_value_for_recognizer)

    char_detector = cls.CnnClassifier(detect_model, preproc_for_detector, model_input_shape)
    char_recognizer = cls.CnnClassifier(recognize_model, preproc_for_recognizer, model_input_shape)

    digit_spotter = detector.DigitSpotter(char_detector, char_recognizer, rp.MserRegionProposer())
    path = 'D:/Caps2/Re_Digit/CAPS2/grade.pdf'
    index_student = ImgProcess.run(path)

    i = 0
    for img_file in img_files[0:]:
        i += 1
        # 2. image
        img = cv2.imread(img_file)

        res = digit_spotter.run(img, threshold=0.5, do_nms=True, nms_threshold=0.2)
        print(i, index_student[i-1], res[2])
