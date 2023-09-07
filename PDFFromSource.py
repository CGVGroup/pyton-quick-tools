from fpdf import FPDF
import os
import glob

SOURCE_EXTENSIONS = [".cpp", ".h"]
#SOURCE_EXTENSIONS = [".cs"]

def addFile(pdf, fileName, root):
    try:
        file = open(fileName, 'r')

        paragraph = file.readlines()
        pdf.add_page()
        size = 10
        pdf.set_font('Courier', size = size)
        line = 1

        header = fileName.replace(root, '')
        pdf.cell(200,int(size/2), txt = 'File: ' + header + '\n', ln = line, align = 'L')
        line += 1


        for para in paragraph:
            para = para.rstrip()
            para = para.encode('utf-8').decode('latin-1')
            # changing disclaimer in our code...
            para = para.replace('SYCO', 'CGVG')
            pdf.cell(200,int(size/2), txt = para, ln = line, align = 'L')
            line += 1
    except Exception as e:
        print('Error in', fileName, e)

def recurseDir(pdf, root):
    files = glob.iglob(root + '/**', recursive=True)

    for filename in files:
        if any(filename.lower().endswith(ext) for ext in SOURCE_EXTENSIONS):
            #print(filename)
            addFile(pdf, filename, root)


def main():
    #ROOT = 'C:\\MyStuff\\Projects\\Holo-BLSD\\HoloBlsd-2.0\\Holo-BLSD\\Assets\\Scripts'
    ROOT = 'C:\MyStuff\Poli\Bandi\Poc-Transition\sorgenti\HoloBLSD-Player-main\HoloBLSD-DebriefTool\V2\HoloBLSD-DebriefVideoPlayer'


    pdf = FPDF()
    recurseDir(pdf, ROOT)

    pdf.output('holo-blsd-debrief-source.pdf')


main()
