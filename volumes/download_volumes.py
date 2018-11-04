##   Copyright (c) Aslak W. Bergersen, Henrik A. Kjeldsberg. All rights reserved.
##   See LICENSE file for details.

##      This software is distributed WITHOUT ANY WARRANTY; without even 
##      the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
##      PURPOSE.  See the above copyright notices for more information.

from os import system, path
from sys import platform


def download_testdata(test_path, outputfile):
    if platform == "darwin":
        system("curl {} --output {}".format(test_path, outputfile))
        system("tar -zxvf {}".format(outputfile))
        system("rm {}".format(outputfile))
    elif platform == "linux" or platform == "linux2":
        system("wget {}".format(test_path))
        system("tar -zxvf {}".format(outputfile))
        system("rm {}".format(outputfile))
    elif platform == "win32":
        # FIXME: Test on a windows system.
        cmd0 = "bitsadmin /create download"
        cmd1 = "bitsadmin /addfile download {} {}".format(test_path, outputfile)
        cmd2 = "bitsadmin /resume download"
        # TODO: Windows command for extracting tar file


def common_input(case, restrict_to_ica):
    abs_path = path.dirname(path.abspath(__file__))

    # Path to test data
    test_path = "http://ecm2.mathcs.emory.edu/aneuriskdata/download/{}/{}_volumes.tar.gz"
    test_path = test_path.format(case, case)
    outputfile = path.join(abs_path, "{}_volumes.tar.gz".format(case))

    # Download test data if necessary
    print(test_path)
    if not path.exists(path.join(abs_path, case)):
        try:
            download_testdata(test_path, outputfile)
        except Exception:
            print("Problem downloading the testdata, please do it manually from "
                  + test_path + " and extract the compressed tarball in the"
                  + " test folder")

    if restrict_to_ica:
        # Only keep the folders which includes the internal carotid artery
        if path.exists(path.join(abs_path, case, "manifest.csv")):
            tmp_csv = open(path.join(abs_path, case, "manifest.csv"), "r")
            line1 = tmp_csv.readline()
            line2 = tmp_csv.readline()
            tmp_dict = dict(zip(line1.split(","), line2.split(",")))

            if tmp_dict["aneurysmLocation"] not in ["ICA", "MCA"]:
                system("rm -rf " + outputfile.split("_")[0])


if __name__ == "__main__":
    base_case = "C00"
    for i in range(1, 100):
        number = str(i) if i > 9 else "0" + str(i)
        common_input(base_case + number, restrict_to_ica=False)
