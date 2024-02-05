import os

DST_DIRECTORY = "C:\MyStuff\Didattica\VR24\Consegne"
NUMBER_OF_GROUPS = 26
def main():
    print("started")
    # Ensure the destination directory exists
    if not os.path.exists(DST_DIRECTORY):
        os.makedirs(DST_DIRECTORY)

    # Create numbered directories
    for i in range(1, NUMBER_OF_GROUPS + 1):
        # Format the directory name with double digits
        directory_name = f"{i:02d}"
        directory_path = os.path.join(DST_DIRECTORY, directory_name)

        # Create the numbered directory
        os.makedirs(directory_path)

        # Create "Prima Consegna" and "Seconda Consegna" folders inside each numbered directory
        os.makedirs(os.path.join(directory_path, "Prima Consegna"))
        os.makedirs(os.path.join(directory_path, "Seconda Consegna"))

main()