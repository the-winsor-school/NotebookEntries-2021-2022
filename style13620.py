import csv
import itertools
import os
import subprocess
import calendar

class Team13620(object):
    def __init__(self):
        self.teamNumber = 13620

        self.header = "\documentclass[16pt]{extarticle}"
        self.header += "\usepackage[margin=0.6in]{geometry} \usepackage{tikz,lipsum,lmodern} \usepackage[most]{tcolorbox} \\tcbuselibrary{listings,breakable} \usepackage[default]{lato} \usepackage[T1]{fontenc} \usepackage{tikz} \usepackage{dashrule} \usepackage{comment} \usepackage{eso-pic} \usepackage{ifthen} \usepackage{changepage} \usepackage{xcolor} \usepackage{paracol}"
        self.header += "\definecolor{textGrey}{RGB}{0, 0, 0} \definecolor{buildBlue}{RGB}{209, 218, 219} \definecolor{codeBlue}{RGB}{211,223,223} \definecolor{businessBlue}{RGB}{223, 217, 227} \definecolor{backgroundColor}{RGB}{80, 102, 114}"
        self.header += "\color{white} \\renewcommand{\\baselinestretch}{1.3} \\pagestyle{empty} \\begin{document}"
        self.header += "\pagecolor{backgroundColor}" 
        self.footer = "\end{paracol}\end{document}"

        self.buildingHeader = "\\begin{paracol}{3} \\begin{tcolorbox}[colback=buildBlue,colframe=white,coltext=textGrey] {\Large \\textbf{building}} \end{tcolorbox}"
        self.codingHeader = "\switchcolumn \\begin{tcolorbox}[colback=codeBlue,colframe=white,coltext=textGrey] {\Large \\textbf{coding}} \end{tcolorbox}"
        self.businessHeader = "\switchcolumn \\begin{tcolorbox}[colback=businessBlue,colframe=white,coltext=textGrey] {\Large \\textbf{business}} \end{tcolorbox}"


    def formatDate(self, date_pretty, people):
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
        return None
