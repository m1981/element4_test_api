import os

def concatenate_files(directory, output_file):
    with open(output_file, "w") as output:
        for subdir, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith(".py"):
                    filepath = subdir + os.sep + filename

                    output.write(f'{filepath}\n')
                    output.write("```\n")
                    with open(filepath, "r") as file:
                        content = file.read()
                    output.write(f'{content}\n')
                    output.write("```\n\n")

# Specify the directory of your project and the output file
directory_path = "modules"
output_file = "proj.txt"
concatenate_files(directory_path, output_file)
