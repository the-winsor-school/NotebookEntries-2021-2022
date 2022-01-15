import csv
import itertools
import os
import subprocess
import calendar

class Team13620(object):
    def __init__(self):
        self.teamNumber = 13620

        self.header = "\documentclass[16pt]{extarticle}"
        self.header += "\usepackage[margin=0.6in]{geometry}"
        self.header += "\usepackage{tikz,lipsum, dashrule, comment, eso-pic, ifthen, changepage, xcolor, graphicx, marginnote}"
        self.header += "\usepackage[most]{tcolorbox} \\tcbuselibrary{listings,breakable}"
        self.header += "\usepackage{lmodern} \usepackage[default]{lato} \usepackage[T1]{fontenc}" # Fonts technically its \usepackage{mlmodern}
        #self.header += "\\reversemarginpar"

        colors = "\definecolor{textGrey}{RGB}{0, 0, 0}" 
        colors += "\definecolor{buildBlue}{RGB}{212, 217, 222}"
        colors += "\definecolor{codeBlue}{RGB}{214, 223, 222}"
        colors += "\definecolor{businessBlue}{RGB}{222, 217, 227}" 
        colors += "\definecolor{wholeBlue}{RGB}{220, 220, 220}" #TODO change
        colors += "\definecolor{backgroundColor}{RGB}{85, 102, 115}"

        self.header += colors
        self.header += "\color{white} \\renewcommand{\\baselinestretch}{1.3} \\pagestyle{empty} \\begin{document}"
        self.header += "\pagecolor{backgroundColor}" 
        self.footer = "\end{document}"

        self.wholeHeader = "\marginnote{\\begin{tcolorbox}[colback=wholeBlue,colframe=white,coltext=textGrey] {\Large \\rotatebox{90}{\\textbf{whole team}}} \end{tcolorbox}}"
        self.buildingHeader = "\marginnote{\\begin{tcolorbox}[colback=buildBlue,colframe=white,coltext=textGrey] {\Large \\rotatebox{90}{\\textbf{building}}} \end{tcolorbox}}"
        self.codingHeader = "\marginnote{\\begin{tcolorbox}[colback=codeBlue,colframe=white,coltext=textGrey] {\Large \\rotatebox{90}{\\textbf{coding}}} \end{tcolorbox}}"
        self.businessHeader = "\marginnote{\\begin{tcolorbox}[colback=businessBlue,colframe=white,coltext=textGrey] {\Large \\rotatebox{90}{\\textbf{business}}} \end{tcolorbox}}"


    def formatDate(self, date_pretty):
        return "{\Huge " + date_pretty + " } \\\\ " 

    def buildBlock(self, data, i):
        # "data" is the text, "i" is index. +1 to make it one indexed instead of zero indexed
        txt = "\\begin{tcolorbox}[colback=buildBlue,colframe=white,coltext=textGrey, breakable]"
        txt += "\\textit{\\textbf{focus: }} \\\\" + data['Focus'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{summary: }} \\\\" + data['Summary'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{challenges: }} \\\\" + data['Challenges/Problems'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{next steps: }} \\\\" + data['Next Steps']
        txt += "\end{tcolorbox}"
        return txt

    def codingBlock(self, data, i):
        # "data" is the text, "i" is "Afternoon" or "Morning". 
        txt = "\\begin{tcolorbox}[colback=codeBlue,colframe=white,coltext=textGrey, breakable]"
        txt += "\\textit{\\textbf{focus: }} \\\\" + data['Focus'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{summary: }} \\\\" + data['Summary'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{challenges: }} \\\\" + data['Challenges/Problems'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{next steps: }} \\\\" + data['Next Steps'] 
        txt += "\end{tcolorbox}"
        return txt

    def businessBlock(self, data, i):
        # "data" is the text, "i" is "Afternoon" or "Morning". 
        txt = "\\begin{tcolorbox}[colback=businessBlue,colframe=white,coltext=textGrey, breakable]"
        txt += "\\textit{\\textbf{focus: }} \\\\" + data['Focus'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{summary: }} \\\\" + data['Summary'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{challenges: }} \\\\" + data['Challenges/Problems'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{next steps: }} \\\\" + data['Next Steps'] 
        txt += "\end{tcolorbox}"
        return txt

    def wholeBlock(style, data, i):
        # "data" is the text, "i" is "Afternoon" or "Morning". 
        txt = "\\begin{tcolorbox}[colback=wholeBlue,colframe=white,coltext=textGrey, breakable]"
        txt += "\\textit{\\textbf{focus: }} \\\\" + data['Focus'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{summary: }} \\\\" + data['Summary'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{challenges: }} \\\\" + data['Challenges/Problems'] + "\\\\ \\\\"
        txt += "\\textit{\\textbf{next steps: }} \\\\" + data['Next Steps']
        txt += "\end{tcolorbox}"
        return txt
