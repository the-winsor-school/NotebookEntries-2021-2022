import csv
import itertools
import os
import subprocess
import calendar

import style20409, style13620

def readCSV():
    # Read in each CSV file and create a list of dictionaries
    with open("data/business.csv") as afile:
        businessFile = csv.DictReader(afile)
        businessData = list(businessFile)

    with open("data/building.csv") as bfile:
        buildFile = csv.DictReader(bfile)
        buildData = list(buildFile)

    with open("data/coding.csv") as cfile:
        codingFile = csv.DictReader(cfile)
        codingData = list(codingFile)

    with open("data/wholeTeam.csv") as wfile:
        wholeFile = csv.DictReader(wfile)
        wholeData = list(wholeFile)

    return (businessData, buildData, codingData, wholeData)

def computeDateList(businessData, buildData, codingData, wholeData): 
    # Gather up a master list of all of dates of meetings by reading through every entry
    aDates = [businessData[i]['Date'].split(" ")[0] for i in xrange(len(businessData))]
    bDates = [buildData[i]['Date'].split(" ")[0] for i in xrange(len(buildData))] 
    cDates = [codingData[i]['Date'].split(" ")[0] for i in xrange(len(codingData))]
    wDates = [wholeData[i]['Date'].split(" ")[0] for i in xrange(len(wholeData))]
    # Taking the set removes duplicates. Then return an unsorted list
    allDates = list(set(aDates + bDates + cDates + wDates))
    return allDates

def findIndicesForDateAndTeam(allData, date, teamNumber):
    # For a given date, find all of the entries in allData that correspond to that date. 
    # For a given team, find all of the entries in allData that correspond to that team
    matching = []
    for i in xrange(len(allData)):
        rawDay = allData[i]['Date'].split(" ")[0]
        rawTeam = allData[i]['Team'].split(" ")[0]
        if rawDay == date and ((str(teamNumber) in rawTeam) or ('Both' in rawTeam) or ('Fill' in rawTeam)):
            matching.append(i)
    return matching  

def displayDate(date):
    # Convert the date format. i.e. "12/7/2020" -> December 7, 2020
    [m, d, y] = date.split("/")
    return calendar.month_name[int(m)] + ' ' + d + ', ' + y

def generateLatex20409(style, businessData, buildData, codingData, wholeData, meeting_date):
    # For a particular meeting_data, generate the corresponding LaTeX page and write to meeting_date.tex
    # There is a lot of list comprehension because each subteam may have multiple entries per date

    # Find the list indices for all the entries corresponding to this date
    aidx = findIndicesForDateAndTeam(businessData, meeting_date, style.teamNumber)
    bidx = findIndicesForDateAndTeam(buildData, meeting_date, style.teamNumber)
    cidx = findIndicesForDateAndTeam(codingData, meeting_date, style.teamNumber)
    widx = findIndicesForDateAndTeam(wholeData, meeting_date, style.teamNumber)
    # Create boolean flag for if this subteam has any entries for this date
    aIs = (len(aidx) > 0)
    bIs = (len(bidx) > 0)
    cIs = (len(cidx) > 0)
    wIs = (len(widx) > 0)
    
    # Gather the members listed for any of the entries for this date
    apeople = list(itertools.chain(*[businessData[pa]['Members'].split(', ') for pa in aidx]))
    bpeople = list(itertools.chain(*[buildData[pb]['Members'].split(', ') for pb in bidx]))
    cpeople = list(itertools.chain(*[codingData[pc]['Members'].split(', ') for pc in cidx]))
    wpeople = list(itertools.chain(*[wholeData[pw]['Members'].split(', ') for pw in widx]))
    # By creating a set, this removes duplicates. Then create a writeable list, comma separated
    people =  ", ".join(list(set(apeople + bpeople + cpeople + wpeople)))

    # Crate a nicely formatted date
    date_pretty = displayDate(meeting_date)
    # Generate the header block with the date and members list
    date = style.formatDate(date_pretty, people) 

    ###################################
    # For each of our three headers, write the header (including the dotted line)
    # Then, within each header, if that subteam has entries, generate the color box for each entry
    focus = style.focusHeader
    summary = style.summaryHeader
    challenges = style.challengesHeader
    nextSteps = style.nextStepsHeader 

    if bIs:
        focus += " ".join([style.buildBlock(buildData[bidx[f]]['Focus'], f) for f in xrange(len(bidx))])
        summary += " ".join([style.buildBlock(buildData[bidx[s]]['Summary'], s) for s in xrange(len(bidx))])
        challenges += " ".join([style.buildBlock(buildData[bidx[c]]['Challenges/Problems'], c) for c in xrange(len(bidx))])
        nextSteps += " ".join([style.buildBlock(buildData[bidx[n]]['Next Steps'], n) for n in xrange(len(bidx))])

    if cIs:
        focus += " ".join([style.codingBlock(codingData[cidx[f]]['Focus'], f) for f in xrange(len(cidx))])
        summary += " ".join([style.codingBlock(codingData[cidx[s]]['Summary'], s) for s in xrange(len(cidx))])
        challenges += " ".join([style.codingBlock(codingData[cidx[c]]['Challenges/Problems'], c) for c in xrange(len(cidx))])
        nextSteps += " ".join([style.codingBlock(codingData[cidx[n]]['Next Steps'], n) for n in xrange(len(cidx))])

    if aIs:
        focus += " ".join([style.businessBlock(businessData[aidx[f]]['Focus'], f) for f in xrange(len(aidx))])
        summary += " ".join([style.businessBlock(businessData[aidx[s]]['Summary'], s) for s in xrange(len(aidx))])
        challenges += " ".join([style.businessBlock(businessData[aidx[c]]['Challenges/Problems'], c) for c in xrange(len(aidx))])
        nextSteps += " ".join([style.businessBlock(businessData[aidx[n]]['Next Steps'], n) for n in xrange(len(aidx))])

    if wIs:
        focus += " ".join([style.wholeBlock(wholeData[widx[f]]['Focus'], f) for f in xrange(len(widx))])
        summary += " ".join([style.wholeBlock(wholeData[widx[s]]['Summary'], s) for s in xrange(len(widx))])
        challenges += " ".join([style.wholeBlock(wholeData[widx[c]]['Challenges/Problems'], c) for c in xrange(len(widx))])
        nextSteps += " ".join([style.wholeBlock(wholeData[widx[n]]['Next Steps'], n) for n in xrange(len(widx))])


    # Gather all of the material in order. "material" is a string file that contains the entire LaTeX document
    material = style.header + date + focus + summary + challenges + nextSteps + style.footer
    ###################################

    # Need to reformat date to not use backslashes in the filename
    save_date = meeting_date.replace('/', '_')
    fileName = 'pages/{}/{}.tex'.format(style.teamNumber, save_date)

    # Write LaTex 
    f = open(fileName, 'a')
    f.write(material)
    f.close()

    return save_date

def generateLatex13620(style, businessData, buildData, codingData, wholeData, meeting_date):
    # For a particular meeting_data, generate the corresponding LaTeX page and write to meeting_date.tex
    # There is a lot of list comprehension because each subteam may have multiple entries per date

    # Find the list indices for all the entries corresponding to this date
    aidx = findIndicesForDateAndTeam(businessData, meeting_date, style.teamNumber)
    bidx = findIndicesForDateAndTeam(buildData, meeting_date, style.teamNumber)
    cidx = findIndicesForDateAndTeam(codingData, meeting_date, style.teamNumber)
    widx = findIndicesForDateAndTeam(wholeData, meeting_date, style.teamNumber)
    # Create boolean flag for if this subteam has any entries for this date
    aIs = (len(aidx) > 0)
    bIs = (len(bidx) > 0)
    cIs = (len(cidx) > 0)
    wIs = (len(widx) > 0)
    
    # Gather the members listed for any of the entries for this date
    apeople = list(itertools.chain(*[businessData[pa]['Members'].split(', ') for pa in aidx]))
    bpeople = list(itertools.chain(*[buildData[pb]['Members'].split(', ') for pb in bidx]))
    cpeople = list(itertools.chain(*[codingData[pc]['Members'].split(', ') for pc in cidx]))
    wpeople = list(itertools.chain(*[wholeData[pw]['Members'].split(', ') for pw in widx]))
    # By creating a set, this removes duplicates. Then create a writeable list, comma separated
    people =  ", ".join(list(set(apeople + bpeople + cpeople + wpeople)))

    # Crate a nicely formatted date
    date_pretty = displayDate(meeting_date)
    # Generate the header block with the date and members list
    date = style.formatDate(date_pretty, people) 

    ###################################
    # For each of our three headers, write the header (including the dotted line)
    # Then, within each header, if that subteam has entries, generate the color box for each entry
    building = style.buildingHeader
    coding = style.codingHeader
    business = style.businessHeader
    
    if bIs: building += "".join([style.buildBlock(buildData[bidx[f]], f) for f in xrange(len(bidx))])
    if cIs: coding += " ".join([style.codingBlock(codingData[cidx[f]], f) for f in xrange(len(cidx))])
    if aIs: business += " ".join([style.businessBlock(businessData[aidx[f]], f) for f in xrange(len(aidx))])
    # if wIs: whole += " ".join([style.wholeBlock(wholeData[widx[f]], f) for f in xrange(len(widx))])

    # Gather all of the material in order. "material" is a string file that contains the entire LaTeX document
    material = style.header + date + building + coding + business + style.footer
    ###################################

    # Need to reformat date to not use backslashes in the filename
    save_date = meeting_date.replace('/', '_')
    fileName = 'pages/{}/{}.tex'.format(style.teamNumber, save_date)

    # Write LaTex 
    f = open(fileName, 'a')
    f.write(material)
    f.close()

    return save_date

def generatePDF(fileName, teamNumber):
    # Generate PDF
    # Use subprocess instead of os.system so that we can operate in different directory
    p = subprocess.Popen(['pdflatex', '{}.tex'.format(fileName)], cwd='pages/{}'.format(teamNumber))
    p.wait()

    # Command to convert to pngs: pdftoppm 9_26_2020.pdf 9_26_2020 -png
    p = subprocess.Popen(['pdftoppm', '{}.pdf'.format(fileName), fileName, '-png'], cwd='pages/{}'.format(teamNumber))

if __name__ == '__main__':
    # Read in the data
    aData, bData, cData, wData = readCSV()
    # Create the master date list
    dateList = computeDateList(aData, bData, cData, wData)

    spec20409 = style20409.Team20409()
    spec13620 = style13620.Team13620()

    # For each date, create the file
    for i in xrange(len(dateList)):
        print('DATE {}'.format(dateList[i]))
        # Generate LaTeX file. Then PDF, then PNG
        fileName13620 = generateLatex13620(spec13620, aData, bData, cData, wData, dateList[i])
        generatePDF(fileName13620, spec13620.teamNumber)

        fileName20409 = generateLatex20409(spec20409, aData, bData, cData, wData, dateList[i])
        generatePDF(fileName20409, spec20409.teamNumber)

