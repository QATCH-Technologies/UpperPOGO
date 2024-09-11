import shutil
import sys
import os

class pack_output:

    def __init__(self, argv=sys.argv):

        if len(argv) >= 3:
            self.root = argv[2]
        else:
            self.root = os.path.dirname(os.path.dirname(argv[0])) # os.getcwd()

        if len(argv) >= 2:
            self.file = argv[1]
        else:
            while True:
                self.file = input("Name of version: ")
                if len(self.file.strip()) > 0:
                    break
                print("Invalid input. Try again! (Ctrl+C to quit)")

        print("Scanning path:", self.root)
        print("Version name: ", self.file)


    def set_root(self, root):

        self.root = root


    def set_file(self, file):

        self.file = file


    def run(self):

        output_files = []
        for r in os.listdir(self.root):

            if (
                os.path.isdir(os.path.join(self.root, r))
                and os.path.basename(self.root) not in r
                and not r[0] == "."
                ):

                print("Adding outputs from:", r, end=" ")
                output_from = os.path.join(self.root, r)
                num_files = 0
            
                for f in os.listdir(output_from):

                    if "dxf" not in f:

                        num_files += 1
                        output_files.append(os.path.join(output_from, f))

                print(f"({num_files} files found)")

        print(output_files)
        project_name = os.path.basename(self.root)
        ok_if_folder_exists = False
        for file in output_files:

            copy_from = file
            copy_to = os.path.join(self.root, 
                                   ".output", 
                                   self.file,
                                   file.replace(self.root, "")[1:].replace(project_name, self.file))
            
            os.makedirs(os.path.dirname(copy_to), exist_ok=ok_if_folder_exists) # prevent overwrites
            ok_if_folder_exists = True

            print("Create:", copy_to)
            shutil.copy(copy_from, copy_to)

        output_dir = os.path.join(self.root, 
                                  ".output", 
                                  self.file)

        print("Creating ZIP archive...")
        os.chdir(output_dir)
        zip_filename = f"{output_dir}-outputs.zip"
        shutil.make_archive(zip_filename[:-4], "zip")
        os.rename(zip_filename, f"./{os.path.basename(zip_filename)}")

        print("DONE!")
        input() # pause
        


if __name__ == '__main__':

    pack_output().run()