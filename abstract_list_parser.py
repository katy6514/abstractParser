#!/usr/bin/python

# this script is meant to be used with the form data returned by the 
# abstract submission forms for the Chandra Xgal14 workshop, and the 
# Chandra 15Y symposium (among others). If you edit the forms to add 
# more fields, you need to edit the "for line in file" loop below.

# add functionality to forms to accept an abstract_status which will be 
# set to "submitted" intitially but then manually changed to "accepted_oral,"  
# "accepted_poster," or "accepted_invited" when the program for the event 
# has been settled. This manual flag editing will quickly allow for the list of  
# submitted abstracts to be parsed for email lists of:
#      all accepted: accepted*
#      all oral: accepted_oral
#      all posters: accepted_poster
#      all submitted: *
#      all invited: accepted_invited
# or possibly other things.


# KATY TO-DO:
#      For "accepted" status lists, call the same functions but with a
#      shorted "sorted_submissions" object?
#
#      Add a function for parsing the list and preparing presentations 
#      for ADS abstract submission. FOrmat as follows:
#          %T Title
#          %A Autho
#          %F Institution
#          %I PDF: (url to talk)
#          %B Abstract
#     Print them out line by line, or save to .txt file and send to 
#     Carolyn Grant in ADS (refence email from evan, subject: 
#     "Fwd: 2012 Chandra Newsletter Articles")
#
#     Add functionality to get email lists for:
#           - poster submitters
#           - oral submitters
#           - all accepted and seperately:
#               - accepted oral
#               - accepted posters
#
#     Add a count everytime the script is run, before/after it generates 
#     the lists that displays a count of all categories:
#        - all submitted oral
#        - all submitted poster
#            - and total
#        - all accepted oral
#        - all accepted poster
#            - and total


import re
import os
from subprocess import call

working_directory = raw_input("Directory containing the list?: ")
write_directory = working_directory+"/parsed_submissions"
#check to see if directory exists. if not, create it
directory_exists = os.path.isdir(write_directory)
if directory_exists != True:
    call(["mkdir", write_directory])


abstract_list = raw_input("Abstract List Filename?: ")
#abstract_list = "abstract_list_post_oral_deadline.txt"
abstract_list = working_directory+"/"+abstract_list



FILE = open(abstract_list,'r')

i=0
submissions=[]


for line in FILE:
    line=line.replace("\n","")
    #print line
    if 'First Name:' in line:
        #start a new row in "submissions"
        submissions.append([])
        submissions[i].append(line.split("First Name: ",1)[1])#0
    if 'Last Name:' in line:
        #print line.split("Last Name: ",1)[1]
        submissions[i].append(line.split("Last Name: ",1)[1])#1
    if 'Co-Authors:' in line:
        submissions[i].append(line.split("Co-Authors: ",1)[1])#2
    if 'Email Address:' in line:
        submissions[i].append(line.split("Email Address: ",1)[1])#3
    if 'Institution:' in line:
        submissions[i].append(line.split("Institution: ",1)[1])#4
    if 'Presentation:' in line:
        submissions[i].append(line.split("Presentation: ",1)[1])#5
    if 'Title:' in line:
        submissions[i].append(line.split("Title: ",1)[1])#6
    if 'Abstract:' in line:
        submissions[i].append(line.split("Abstract: ",1)[1])#7
    if 'Comments:' in line:
        submissions[i].append(line.split("Comments: ",1)[1])#8
        #i+=1
    if 'Status:' in line:
        #print "yey status"
        submissions[i].append(line.split("Status: ",1)[1])#9  
        #close the row in "submissions"
        #print i
        i+=1
        #print "i = "+ str(i)
        #print len(submissions)

for i in range(len(submissions)):
    #print len(submissions[i])
    if len(submissions[i]) == 0:
        submissions.remove(submissions[i])

#for i in range(len(submissions)):
   ### print len(submissions[i])

# get rid of lame last entry?
#submissions.pop()

#print len(submissions)

#submissions.sort(key=lambda i: i[1])

sorted_submissions = sorted(submissions, key=lambda submission: submission[1])



# ------------------------------------------------------------------------------------
#   Function Time!!
# ------------------------------------------------------------------------------------


#if directory does not exist, create it
directory_exists = os.path.isdir(write_directory)
if directory_exists != True:
    make_directory_cmd = "mkdir "+write_directory
    os.system(make_directory_cmd)




# ------------------------------------------------------------------
#   Line Prepending Function
#       Useful for adding counts to the beginings of files
# ------------------------------------------------------------------

def line_prepender(filename, line):
    with open(filename.name, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n\n' + content)


# -----------------------------------------------------------------------------------
#   Function to generate two title lists of all submitted posters and talks
#       Useful for when the SOC is picking which submissions to include
# -----------------------------------------------------------------------------------

def all_submissions_title_list(sort_sub):

    #sort_sub = sorted_submissions
    poster_list = open(write_directory+"/all_submitted_poster_titles.txt","w+")
    talk_list = open(write_directory+"/all_submitted_talk_titles.txt","w+")

    total_count = 0
    poster_count = 0
    talk_count = 0

    # writes LastName, FirstName, Institution, and Title to file
    for x in range(len(sort_sub)):
        total_count += 1
        #print sort_sub[x][4]
        if (sort_sub[x][4]).lower() == "poster" or (sort_sub[x][4]).lower() == "oral-turned-poster":
            poster_count += 1
            poster_list.write(sort_sub[x][1]+", "+
                              sort_sub[x][0]+", "+
                              sort_sub[x][3]+", "+
                              sort_sub[x][5]+"\n")
        elif (sort_sub[x][4]).lower() == "oral":
            talk_count += 1
            talk_list.write(sort_sub[x][1]+", "+
                            sort_sub[x][0]+", "+
                            sort_sub[x][3]+", "+
                            sort_sub[x][5]+"\n")
        else:
            print "title list error!"

    poster_list.close()
    talk_list.close()
    print "All submission titles list files placed in "+write_directory

    # write counts to the beginning of each file 
    line_prepender(poster_list, "Submitted Poster Count: "+str(poster_count))
    line_prepender(poster_list, "Submitted Total (poster+oral) Count: "+str(total_count))
    line_prepender(talk_list, "Submitted Oral Count: "+str(talk_count))
    line_prepender(talk_list, "Submitted Total (poster+oral) Count: "+str(total_count))

    return poster_list, talk_list


# ------------------------------------------------------------------------------------------------
#   Function to generate two lists of all submitted posters and talks and associated info
#       Useful for lots of things.
# ------------------------------------------------------------------------------------------------

def all_submissions_list(sort_sub):

    #sort_sub = sorted_submissions
    poster_list = open(write_directory+"/all_submitted_posters.txt","w")
    talk_list = open(write_directory+"/all_submitted_talks.txt","w")

    total_count = 0
    poster_count = 0
    talk_count = 0

    # writes all information associated with each submission to file
    # these for loops are repeatable (same as following function), make a sub-function??
    for x in range(len(sort_sub)):
        total_count += 1
        if (sort_sub[x][4]).lower() == "poster" or (sort_sub[x][4]).lower() == "oral-turned-poster":
            poster_count += 1
            poster_list.write("Name: "+sort_sub[x][0]+" "+sort_sub[x][1]+
                              "\nE-mail: "+sort_sub[x][2]+
                              "\nInstitution: "+sort_sub[x][3]+
                              "\nPresentation Type: "+sort_sub[x][4]+
                              "\nTitle: "+sort_sub[x][5]+
                              "\nAbstract: "+sort_sub[x][6]+
                              "\nComments: "+sort_sub[x][7]+
                              "\nStatus: "+sort_sub[x][8]+"\n\n\n")
        elif (sort_sub[x][4]).lower() == "oral":
            talk_count += 1
            talk_list.write("Name: "+sort_sub[x][0]+" "+sort_sub[x][1]+
                            "\nE-mail: "+sort_sub[x][2]+
                            "\nInstitution: "+sort_sub[x][3]+
                            "\nPresentation Type: "+sort_sub[x][4]+
                            "\nTitle: "+sort_sub[x][5]+
                            "\nAbstract: "+sort_sub[x][6]+
                            "\nComments: "+sort_sub[x][7]+
                            "\nStatus: "+sort_sub[x][8]+"\n\n\n")
        else:
            print "all submissions error!"

    poster_list.close()
    talk_list.close()
    print "All submission list files placed in "+write_directory

    # write counts to the beginning of each file 
    line_prepender(poster_list, "Submitted Poster Count: "+str(poster_count))
    line_prepender(poster_list, "Submitted Total (poster+oral) Count: "+str(total_count))
    line_prepender(talk_list, "Submitted Oral Count: "+str(talk_count))
    line_prepender(talk_list, "Submitted Total (poster+oral) Count: "+str(total_count))

    return poster_list, talk_list

# ------------------------------------------------------------------------------------------------
#   Function to generate two lists of all accepted posters and talks and associated info
#       Useful for lots of things.
# ------------------------------------------------------------------------------------------------

def all_accepted_list(sort_sub): #use different data structure?

    #sort_sub = sorted_submissions
    poster_list = open(write_directory+"/all_accepted_posters.txt","w")
    talk_list = open(write_directory+"/all_accepted_talks.txt","w")

    total_count = 0
    poster_count = 0
    talk_count = 0

    # writes all information associated with each submission to file
    # these for loops are repeatable (same as preceeding function), make a sub-function??
    for x in range(len(sort_sub)):
        total_count += 1
        if (sort_sub[x][4]).lower() == "poster" or (sort_sub[x][4]).lower() == "oral-turned-poster":
            poster_count += 1
            poster_list.write("Name: "+sort_sub[x][0]+" "+sort_sub[x][1]+"\n"+
                              "Co-Authors: "+sort_sub[x][2]+"\n"+
                              "E-mail: "+sort_sub[x][3]+"\n"+
                              "Institution: "+sort_sub[x][4]+"\n"+
                              "Presentation Type: "+sort_sub[x][5]+"\n"+
                              "Title: "+sort_sub[x][6]+"\n"+
                              "Abstract: "+sort_sub[x][7]+"\n"+
                              "Comments: "+sort_sub[x][8]+"\n\n\n")
        elif (sort_sub[x][4]).lower() == "oral" and (sort_sub[x][8]).lower() == "accepted":
            talk_count += 1
            talk_list.write("Name: "+sort_sub[x][0]+" "+sort_sub[x][1]+"\n"+
                            "Co-Authors: "+sort_sub[x][2]+"\n"+
                            "E-mail: "+sort_sub[x][3]+"\n"+
                            "Institution: "+sort_sub[x][4]+"\n"+
                            "Presentation Type: "+sort_sub[x][5]+"\n"+
                            "Title: "+sort_sub[x][6]+"\n"+
                            "Abstract: "+sort_sub[x][7]+"\n"+
                            "Comments: "+sort_sub[x][8]+"\n\n\n")
        else:
            print "all accepted error!"

    poster_list.close()
    talk_list.close()

    # write counts to the beginning of each file 
    line_prepender(poster_list, "Accepted Poster Count: "+str(poster_count))
    line_prepender(poster_list, "Accepted Total (poster+oral) Count: "+str(total_count))
    line_prepender(talk_list, "Accepted Oral Count: "+str(talk_count))
    line_prepender(talk_list, "Accepted Total (poster+oral) Count: "+str(total_count))

    return poster_list, talk_list




# ----------------------------------------------------------------------
#   Function to generate various email lists for all submitters
#       Useful for when the organizers need to contact people
# ----------------------------------------------------------------------

def get_emails(sort_sub):

    poster_emails = open(write_directory+"/emails_submitted_poster.txt","w")
    talk_emails = open(write_directory+"/emails_submitted_talk.txt","w")
    all_emails = open(write_directory+"/emails_submitted_all.txt","w")

    total_count = 0
    poster_count = 0
    talk_count = 0

    # writes email to file
    for x in range(len(sort_sub)):
        total_count += 1
        all_emails.write(sort_sub[x][3]+", ")
        if (sort_sub[x][5]) == "poster":
            poster_count += 1
            poster_emails.write(sort_sub[x][3]+", ")
        elif (sort_sub[x][5]) == "oral":
            talk_count += 1
            talk_emails.write(sort_sub[x][3]+", ")
        else:
            print "get emails error!"

    poster_emails.close()
    talk_emails.close()
    all_emails.close()

    # write counts to the beginning of each file 
    line_prepender(poster_emails, "Number of Poster Submitters: "+str(poster_count))
    line_prepender(poster_emails, "Number of Total (poster+oral) submitters: "+str(total_count))
    line_prepender(talk_emails, "Number of Oral Submitters: "+str(talk_count))
    line_prepender(talk_emails, "Number of Total (poster+oral) submitters: "+str(total_count))
    line_prepender(all_emails, "Number of Total (poster+oral) submitters: "+str(total_count))

    return poster_emails, talk_emails, all_emails


# ------------------------------------------------------------------
#   HTML Formatting Function
#       Useful when you need to make big edits to the website
# ------------------------------------------------------------------

def html_formatter(sort_sub):

    poster_html = open(write_directory+"/html_accepted_posters.html","w")
    talk_html = open(write_directory+"/html_accepted_talks.html","w")

    total_count = 0
    poster_count = 0
    talk_count = 0

    # writes all information associated with each submission to file
    # these for loops are repeatable (same as preceeding function), make a sub-function??
    for x in range(len(sort_sub)):
        #print (sort_sub[x][4]).lower()
        total_count += 1
        if (sort_sub[x][4]).lower() == "poster" or (sort_sub[x][4]).lower() == "oral-turned-poster":
            poster_count += 1
            poster_html.write("<li class=\"poster_num\">"+str(poster_count) +"</li>"+ "\n"+
                              "<li class=\"poster_author\">"+sort_sub[x][0]+" "+sort_sub[x][1]+"</li>"+ "\n"+
                              "<li class=\"postertitle\"><h3>"+sort_sub[x][5]+"</h3>"+"\n"+
                                 "<div>"+"\n"+
                                    "<p>"+sort_sub[x][6]+" <br /><br /></p>"+"\n"+
                                 "</div>"+"\n"+
                              "</li>"+"\n\n\n")
        elif (sort_sub[x][4]).lower() == "oral" and (sort_sub[x][8]).lower() == "approved":
            talk_count += 1
            talk_html.write("<li class=\"time\">TIME</li>"+ "\n"+
                            "<li class=\"author\">"+sort_sub[x][0]+" "+sort_sub[x][1]+"</li>"+ "\n"+
                            "<li class=\"talktitle\"><h3>"+sort_sub[x][5]+"</h3>"+"\n"+
                               "<div>"+"\n"+
                                  "<p>"+sort_sub[x][6]+" <br /><br /></p>"+"\n"+
                               "</div>"+"\n"+
                            "</li>"+"\n\n\n")
        elif (sort_sub[x][4]).lower() == "oral" and (sort_sub[x][8]).lower() == "invited":
            talk_count += 1
            talk_html.write("<li class=\"time\">TIME</li>"+ "\n"+
                            "<li class=\"author\"><span class=\"invited\">"+sort_sub[x][0]+" "+sort_sub[x][1]+"</span></li>"+ "\n"+
                            "<li class=\"talktitle\"><h3><span class=\"invited\">"+sort_sub[x][5]+"</span></h3>"+"\n"+
                               "<div>"+"\n"+
                                  "<p>"+sort_sub[x][6]+" <br /><br /></p>"+"\n"+
                               "</div>"+"\n"+
                            "</li>"+"\n\n\n")
        else:
            print "html "+sort_sub[x][1]+" "+sort_sub[x][8].lower()+" "+sort_sub[x][4].lower()

    poster_html.close()
    talk_html.close()

    copy_file_cmd = "cp "+write_directory+"/html_accepted_posters.html /data/cdoweb/wymanRep/cdo/hrxs2015/include/"
    copy_prev_cmd = "cp "+write_directory+"/html_accepted_posters.html /proj/web-cxc-dmz-prev/htdocs/cdo/hrxs2015/include/"
    copy_live_cmd = "cp "+write_directory+"/html_accepted_posters.html /proj/web-cxc-dmz/htdocs/cdo/hrxs2015/include/"

    #os.system(copy_file_cmd)
    #os.system(copy_prev_cmd)
    #os.system(copy_live_cmd)

    #print "HTML files placed in "+write_directory




# ------------------------------------------------------------------
#   LaTeX Formatting Function
#       Useful when you need to make an abstract handbook
# ------------------------------------------------------------------

def latex_formatter(sort_sub):

    poster_list = open(write_directory+"/latex_accepted_posters.tex","w")
    talk_list = open(write_directory+"/latex_accepted_talks.tex","w")

    total_count = 0
    poster_count = 0
    talk_count = 0

    for x in range(len(sort_sub)):
        total_count += 1
        if (sort_sub[x][4]).lower() == "poster" or (sort_sub[x][4]).lower() == "oral-turned-poster":
            poster_count += 1
            poster_list.write(str(poster_count)+" & "+    #"\\normalsize \n"+
                              "\\textit{"+sort_sub[x][0]+" "+sort_sub[x][1]+"}\\\\"+
                              "\\vspace{0.15in} & "+
                              "\\footnotesize "+sort_sub[x][5]+"\\\\ \n")
        elif (sort_sub[x][4]).lower() == "oral" and (sort_sub[x][8]).lower() == "approved":
            talk_count += 1
            talk_list.write("   & "+ 
                              "\\textit{"+sort_sub[x][0]+" "+sort_sub[x][1]+"}\\\\"+
                              "\\vspace{0.15in} & "+
                              "\\footnotesize "+sort_sub[x][5]+"\\\\ \n")
        elif (sort_sub[x][4]).lower() == "oral" and (sort_sub[x][8]).lower() == "invited":
            talk_count += 1
            talk_list.write("   & "+
                            "\\textit{\\textbf{"+sort_sub[x][0]+" "+sort_sub[x][1]+" - Invited}}\\\\ "+
                            "\\vspace{0.15in} & "+
                            "\\footnotesize "+sort_sub[x][5]+"\\\\ \n")
        else:
            print "latex "+sort_sub[x][8].lower()+" "+sort_sub[x][4].lower()

    return poster_list, talk_list



# --------------------------------------------------------------------------------------------------------------
#   ADS Formatter
#       Useful when you need to send a list of abstract meta-data to ADS (after everything else is over)
# --------------------------------------------------------------------------------------------------------------

def ads_formatter(sort_sub):

    poster_list = open(write_directory+"/ads_accepted_posters.txt","w")
    talk_list = open(write_directory+"/ads_accepted_talks.txt","w")

    total_count = 0
    poster_count = 0
    talk_count = 0

    for x in range(len(sort_sub)):
        total_count += 1
        if (sort_sub[x][5]) == "poster":
            poster_count += 1
            poster_list.write("%T "+sort_sub[x][6]+"\n"+
                              "%A "+sort_sub[x][0]+" "+sort_sub[x][1]+"\n"+
                              "%F "+sort_sub[x][4]+"\n"+
                              "%I PDF: \n%B "+sort_sub[x][7]+"\n\n")
        elif (sort_sub[x][5]) == "oral":
            talk_count += 1
            talk_list.write("%T "+sort_sub[x][6]+"\n"+
                            "%A "+sort_sub[x][0]+" "+sort_sub[x][1]+"\n"+
                            "%F "+sort_sub[x][4]+"\n"+
                            "%I PDF: \n%B "+sort_sub[x][7]+"\n\n")
        else:
            print "ads error!"

    return poster_list, talk_list


# ----------------------------------------------------------------------------------------------
#   Function to make a new sorted_submissions object containing only accepted abstracts, and one containing rejected abstracts
# ----------------------------------------------------------------------------------------------

#def get_accepted(sort_sub):





# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------

#   Ladies and gentlmen, call your functions!!!

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------


#------------------------------------
# Functions for use on initial lists
#------------------------------------

#all_submissions_title_list(sorted_submissions)

#all_submissions_list(sorted_submissions)



#------------------------------------
# Functions for making HTML and Latex
#------------------------------------

#html_formatter(sorted_submissions)

fellows_html_formatter(sorted_submissions)

#latex_formatter(sorted_submissions)



#------------------------------------
# Misc Functions
#------------------------------------

#get_emails(sorted_submissions)





#ideas for future functions, either didn't have the need or found another way

# ------------------------------------
# Run this function to seperate the accepted ones ?? - not completed
# ------------------------------------
#get_accepted(sorted_submissions)



# ------------------------------------
# Functions for use on accepted lists ?? - not completed
# ------------------------------------

#latex_formatter(sorted_submissions)
#ads_formatter(sorted_submissions)











