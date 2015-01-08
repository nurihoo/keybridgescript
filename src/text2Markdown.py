__author__ = 'nuri'

import getopt,sys, os, re

def parseFolder(input_dir, output_dir):
    for file in os.listdir(input_dir):
        f = open(os.path.join(input_dir, file))
        text = f.read()
        text = convert2Markdown(text)
        f.close()

        f = open(os.path.join(output_dir, file), 'w')
        f.write(text)
        f.close()

def convert2Markdown(text):
    script_dir = os.path.dirname(__file__)
    #
    # f = open (os.path.join(script_dir, "util/markdown.txt"), 'r')
    # template = f.read()
    text = text.replace('\r', '\n')
    lines = iter(text.split('\n'))

    template = ''
    temp = ''
    once = False
    # for line in lines:
    line = lines.next()
    while True:

        try:
            if line == "SECTION TITLE":
                line = lines.next()
                while line.__len__() == 0:
                    line = lines.next()
                template += "\n#" + line + "\n"
            if line == "FRAME NUMBER":
                line = lines.next()
                while line.__len__() == 0:
                    line = lines.next()
                temp = '@id ' + line+ "\n\n"
                # template = template.replace("[FRAME NUMBER]", line)
            if line == "FRAME TITLE":
                line = lines.next()
                while line.__len__() == 0:
                    line = lines.next()
                template += "\n##" + line+ "\n"
                template += temp
                # template = template.replace("[FRAME TITLE]", line)
            if line == "SCREEN TEXT":
                line = lines.next()
                while line != "AUDIO SCRIPT":
                    template += line
                    if (line.__len__() != 0):
                        template += '\n'
                    line = lines.next()

            if line == "AUDIO SCRIPT":
                line = lines.next()
                template += "\n```audio-script\n"
                while (line != "SPECIAL NOTES OR REFERENCES" and line != "IMAGE ALT TEXT"):
                    # if (line.__len__() != 0):
                    template += line
                    # if (line.__len__() == 0):
                    #     template += '\n'
                    line = lines.next()
                template += "\n```\n\n"

                # template = template.replace("[AUDIO]", line)
            if line == "IMAGE ALT TEXT":
                line = lines.next()
                while line != "SPECIAL NOTES OR REFERENCES":
                    if (line.__len__() != 0):
                        template += "@image -a " + line+ "\n"
                    line = lines.next()
                # template = template.replace("[ALT TEXT]", line)
            if line == "SPECIAL NOTES OR REFERENCES":
                # if once:
                line = lines.next()
                temp = ''
                while (line != 'FRAME NUMBER' and line != "SPECIAL NOTES OR REFERENCES"
                       and line != "IMAGE ALT TEXT" and line != "SECTION TITLE"
                        and line != "SCREEN TEXT"):

                    # if line.__len__() != 0:
                    temp += line

                        #template += "<!-- " + line + "-->"+ "\n"
                    line = lines.next()
                if temp.__len__() != 0:
                    template += "\n<!-- " + temp + "-->"+ "\n\n"

            if (line != 'FRAME NUMBER' and line != "SPECIAL NOTES OR REFERENCES"
                       and line != "IMAGE ALT TEXT" and line != "SECTION TITLE"
                        and line != "SCREEN TEXT"):
                line = lines.next()
        except Exception:
            break

    return template

def main(argv):
    input = ''
    output = ''
    try:
        opts,args = getopt.getopt(argv, "hi:o:", ["input=","output="])
    except getopt.GetoptError:
        print 'text2Markdown.py -i <input> -o <output> '
        print 'input : input file'
        print 'output : output file'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'text2Markdown.py -i <input> -o <output>'
            sys.exit()
        elif opt in ("-i", "--input"):
            input = arg
        elif opt in ("-o", "--output"):
            output = arg
    parseFolder(input, output)

if __name__ == '__main__':
    main(sys.argv[1:])