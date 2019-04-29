'''
    Display the file system block usage (not file size) for each file argument
    and each directory in the file hierarchy in a recursive manner.

    Add the following options:

        '-c' Display a grand total

        '-d depth' Display an entry for all files and
         directories up to 'depth' deep

        -h use 'Human-readable' output i.e.
         Show file size as appropriately needed by using unit suffices:
         Byte, Kilobyte, Megabyte, Gigabyte, Terabyte and Petabyte.


'''
import os
import argparse


class File_Size(object):
    def __init__(self, path):
        """
        :param path: Path of file/Directory
        """
        self.path = path
        self.file_detail = []
        print('Path is: ', self.path)


    def calculate_size(self):
        """
        Method to calculate the list of files/directory

        :return self.file_detail: List of dictionary containin file details
        """
        print('calculation of file size')
        for root, file, direc in os.walk(self.path, topdown=False):
            files_info = {'root_folder': [], 'folder_info': [], 'file_name': []}
            files_info["root_folder"].append(root)
            files_info["folder_info"].append(file)
            files_info["file_name"].append(direc)
            self.file_detail.append(files_info)
        return self.file_detail

    def calculate_file(self, file_total):
        """
        Method to calculate the total number of files/directory

        :return None
        """
        print("Calculation of total size")
        sum_value = 0
        for i in file_total:
            sum_value = sum_value + len(i['file_name'][0])

        print('Total number of files:- ', sum_value)
        sum_folder = 0

        for i in file_total:
            sum_folder = sum_folder + len(i['folder_info'][0])
        print('Total number of folder:- ', sum_folder)


    def calculate_block_usage(self, file_detail_info):
        """
        Method to calculate the block size

        :param file_detail_info: List of dictionary containing file details
        :return : tuple containing free, total and used bytes
        """
        print("Calculating the blocks")
        if not isinstance(file_detail_info, list):
            file_detail_info = list(file_detail_info)

        for path in file_detail_info:
            stat = os.statvfs(path)
            print('--------', path)

            free = (stat.f_bavail * stat.f_frsize) / 1024
            total = (stat.f_blocks * stat.f_frsize) / 1024
            used = ((stat.f_blocks - stat.f_bfree) * stat.f_frsize)
            print('\nTotal:- {} B and used;- {} B and free:- {} B'.format(total, used, free))
        return(free, total, used)


    def remove_unwanted_files(self, files_information):
        """
        Method to remove the unwanted files

        :param files_information: List of dictionary containing file details
        :return file_path: List containing file paths
        """
        print('Remove the unwanted files:- *.pyc and *.py~')
        file_path = []
        for file in files_information:
            files = [name for name in file['file_name'][0] if not name.endswith('pyc') and not name.endswith('py~')]
            folder_name = file['root_folder'][0]
            for name in files:
                file_path.append(os.path.join(folder_name, name))
        return file_path


if __name__ == '__main__':
    print("Calculating the File System block usage")
    parser = argparse.ArgumentParser()

    parser.add_argument("--c", help="display the grand total of files",
                        action="store_true")
    parser.add_argument("--d", help="display for all the files",
                        action="store_true")
    parser.add_argument("--h", help="display in the human Human-readable format",
                        action="store_true")
    parser.add_argument("--p", help="pass the file path",
                        action="store")

    args = parser.parse_args()

    # checking for the file path argument
    if not args.p:
        print("\nPath is not provided. Taking current working directory\n")
        args.p = os.getcwd()

    # take an instance of File_Size()
    file_calculation = File_Size(args.p)

    # calculate for the deep recursive way
    if args.d:
        print("\nDisplay calculation for all the files\n")
        files_information = file_calculation.calculate_size()
        file_path = file_calculation.remove_unwanted_files(files_information)

        # calculate the file system block for all path
        file_calculation.calculate_block_usage(file_path)

    # display the human readble format
    elif args.h:
        print("\nDisplay calculation in human readble format\n")
        files_information = file_calculation.calculate_size()
        file_path = file_calculation.remove_unwanted_files(files_information)

        # calculate the file system block for all path
        free, total, used = file_calculation.calculate_block_usage(file_path)
        print("\n\nDetail:-\n Free:- {} Gigabyte and total:- {} Gigabyte and \
            used: {} Gigabyte ".format(free / float(10**6), total / float(10 ** 6), used / float(10 ** 6)))

    # display the grand total of file system blocks
    elif args.c:
        print("\nDisplay the total numbers\n")
        files_information = file_calculation.calculate_size()
        file_path = file_calculation.remove_unwanted_files(files_information)

        # calculate the total file system block for all path
        print('Total number of files are:- including hidden files')
        file_calculation.calculate_file(files_information)
