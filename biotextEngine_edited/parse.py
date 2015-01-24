import os
import sys

def main():
  root = '/mnt/data01/Data/medline2015/'

  # remove the first 370 files
  sorted_files = sorted(os.listdir(root))

  for file in sorted_files:
    if file.endswith('.xml'):
      if (os.system('java -jar MedlineParser.jar ' + root + file) != 0):
        print(file)
        sys.exit(1)
      # print(root + file)

if __name__ == '__main__':
  main()