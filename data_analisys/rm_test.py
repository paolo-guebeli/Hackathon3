import os

import SimpleITK as sitk
import six

import radiomics as rm
from radiomics import featureextractor


def main():
    data_dir = '.'
    imageName, maskName = rm.getTestCase('brain1', data_dir)
    params = os.path.join(data_dir, "Params.yaml")
    extractor = featureextractor.RadiomicsFeatureExtractor(params)
    result = extractor.execute(imageName, maskName)
    for key, val in six.iteritems(result):
        print("\t%s: %s" % (key, val))
    result = extractor.execute(imageName, maskName, voxelBased=True)
    for key, val in six.iteritems(result):
        if isinstance(val, sitk.Image):  # Feature map
            sitk.WriteImage(val, key + '.nrrd', True)
            print("Stored feature %s in %s" % (key, key + ".nrrd"))
        else:  # Diagnostic information
            print("\t%s: %s" % (key, val))


if __name__ == '__main__':
    main()
