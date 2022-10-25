# coding=UTF-8
import sys
import os
import re
import time
import io

from jira import JIRA
import json


LJUST=12
FILE_PATH_JIRA_CERT=r"D:\work_platform\Jira\auth_amt"

# NOTE: The parameter 'displayName' (Assignee Name) could be changed for time to time
# Just print out the fields value in order to find out what the parameter name is
#--------------------------------------------------------------
def get_assignee_name(_issue):

    if(_issue.raw['fields']['assignee'] is None):
        return "Unassigned"

    return _issue.raw['fields']['assignee']['displayName']

#----------------------------------------------------------------------
def print_jira_status(jira, jql_open, jql_resolved, proj_name, speical_word = '[XXXXX]'):

    all_proj_issues = jira.search_issues(jql_open,maxResults=1000)

    # print ("{} Opening issues:".format(proj_name))
    A_Cout = 0
    B_Cout = 0
    C_Cout = 0
    pStr = 'X'
    issue_arry = []
    print_array = []

    # for issue in all_proj_issues:
    # # print out the raw data of the all fields
    #     for field_name in issue.raw['fields']:
    #         print ("Field:", field_name, "Value:", issue.raw['fields'][field_name])

    # return

    for issue in all_proj_issues:
        pStr = str(issue.fields.priority)

        # Special Word Filter
        tmp_str = str(issue.fields.summary)
        if(tmp_str.startswith(speical_word) == False):
            if(pStr == 'A'):
                A_Cout = A_Cout + 1
            elif(pStr == 'B'):
                B_Cout = B_Cout + 1
            elif(pStr == 'C'):
                C_Cout = C_Cout + 1

            # print ("[{}] {} - {} [{}]".format(issue.fields.priority, str(issue).ljust(LJUST), issue.fields.summary,get_assignee_name(issue)))
            print_array.append("[{}] {} - {} [{}]".format(issue.fields.priority, str(issue).ljust(LJUST), issue.fields.summary,get_assignee_name(issue)))
        else:
            issue_arry.append(issue)
        # print "[%s] %s - %s" %(issue.fields.priority, issue, issue.fields.summary)


    print ("[Opening Issues] {}A {}B {}C, Total = {}".format(A_Cout, B_Cout, C_Cout, A_Cout+B_Cout+C_Cout))
    for item in print_array:
        print( item )
        # print(item.encode("utf8").decode("cp950", "ignore"))
    print(" ")


    all_proj_issues = jira.search_issues(jql_resolved,maxResults=1000)

    # print ("\n{} Resolved issues:".format(proj_name))
    A_Cout = 0
    B_Cout = 0
    C_Cout = 0
    pStr = 'X'
    issue_resolved_arry = []
    print_array = []

    for issue in all_proj_issues:
        pStr = str(issue.fields.priority)

        # Special Word Filter
        tmp_str = str(issue.fields.summary)
        if(tmp_str.startswith(speical_word) == False):
            if(pStr == 'A'):
                A_Cout = A_Cout + 1
            elif(pStr == 'B'):
                B_Cout = B_Cout + 1
            elif(pStr == 'C'):
                C_Cout = C_Cout + 1

            # print ("[{}] {} - {} [{}]".format(issue.fields.priority, str(issue).ljust(LJUST), issue.fields.summary, get_assignee_name(issue)))
            print_array.append("[{}] {} - {} [{}]".format(issue.fields.priority, str(issue).ljust(LJUST), issue.fields.summary, get_assignee_name(issue)))
        else:
            issue_resolved_arry.append(issue)


    print ("[Resolved Issues] {}A {}B {}C, Total = {}".format(A_Cout, B_Cout, C_Cout, A_Cout+B_Cout+C_Cout))
    for item in print_array:
        print( item )
        # print(item.encode("utf8").decode("cp950", "ignore"))
    print(" ")

    # Special Word Filter
    if(speical_word != '[XXXXX]'):
        print ("\n Special WORD File = {}".format(speical_word))
        A_Cout = 0
        B_Cout = 0
        C_Cout = 0
        pStr = 'X'

        for issue in issue_arry:
            pStr = str(issue.fields.priority)
            if(pStr == 'A'):
                A_Cout = A_Cout + 1
            elif(pStr == 'B'):
                B_Cout = B_Cout + 1
            elif(pStr == 'C'):
                C_Cout = C_Cout + 1

            print ("[{}] {} - {} [{}]".format(issue.fields.priority, str(issue).ljust(LJUST), issue.fields.summary, get_assignee_name(issue)))


        print ("[{} - Opening Issues] {}A {}B {}C ".format(speical_word, A_Cout, B_Cout, C_Cout))

        A_Cout = 0
        B_Cout = 0
        C_Cout = 0
        pStr = 'X'

        for issue in issue_resolved_arry:
            pStr = str(issue.fields.priority)
            if(pStr == 'A'):
                A_Cout = A_Cout + 1
            elif(pStr == 'B'):
                B_Cout = B_Cout + 1
            elif(pStr == 'C'):
                C_Cout = C_Cout + 1
            print ("[{}] {} - {} [{}]".format(issue.fields.priority, str(issue).ljust(LJUST), issue.fields.summary, get_assignee_name(issue)))


        print ("[{} - Resolved Issues] {}A {}B {}C, Total = {}".format(speical_word, A_Cout, B_Cout, C_Cout, A_Cout+B_Cout+C_Cout))
    # END


#----------------------------------------------------------------------
def search_auth_file(folder, auth_data, pass_data):
    # print ("Target Path = {}".format(folder))
    p = re.compile(r'\[pass\]', re.IGNORECASE)
    a = re.compile(r'\[account\]', re.IGNORECASE)

    fp = open(folder,"r")
    zops = fp.readlines()
    for lineStr in zops:
        if(p.match(lineStr)):
            lineStr = lineStr.strip()
            pass_data.append(re.sub(p,r'',lineStr))

        if(a.match(lineStr)):
            lineStr = lineStr.strip()
            auth_data.append(re.sub(a,r'',lineStr))

    # print "pass = %s, account = %s" %(pass_data[0],auth_data[0])
#----------------------------------------------------------------------

#----------------------------------------------------------------------
def connect_to_jira(auth, passw):
    jira_options = { 'server': 'https://amtran.atlassian.net/'}

    try:
        jira = JIRA(options=jira_options, basic_auth=(auth, passw))
    except Exception as e:
        jira = None

    return jira

#----------------------------------------------------------------------
def jql_string_process(para_, project_key_):

    jql_open_ = ''
    jql_resolved_ = ''

    if para_ == 'a':
        jql_open_ = 'project = ' + project_key_ + ' AND resolution = Unresolved ORDER BY priority DESC, updated DESC'
        jql_resolved_ = 'project = ' + project_key_ + ' AND status = Resolved ORDER BY priority DESC, updated DESC'  
    elif para_ == '':
        jql_open_ = 'project = ' + project_key_ + ' AND resolution = Unresolved AND component in (AUDIO, EE, PQ, SW, FW, PANEL) ORDER BY priority DESC, updated DESC'
        jql_resolved_ = 'project = ' + project_key_ + ' AND status = Resolved  AND component in (AUDIO, EE, PQ, SW, FW, PANEL) ORDER BY priority DESC, updated DESC'
    else:
        jql_open_ = 'project = ' + project_key_ + ' AND resolution = Unresolved AND component in (' + para_ + ') ORDER BY priority DESC, updated DESC'
        jql_resolved_ = 'project = ' + project_key_ + ' AND status = Resolved  AND component in (' + para_ + ') ORDER BY priority DESC, updated DESC'

    return jql_open_,jql_resolved_

#----------------------------------------------------------------------
def json_para_reader():
    with open('models.json') as f:
        data = json.load(f)

    # print(data)
    # print(" length of data = {}, data 0 = {}".format(len(data),type(data)))

    data_a = data['models']
    # print("Length of data = {} , data 0 = {} , data 0 type = {}".format(len(data_a),data_a[0],type(data_a[0])))

    arr1 = []
    arr2 = []
    arro = []

    for sub_data in data_a:
        temp_ar = []
        temp_ar.append(sub_data['name'])
        temp_ar.append(int(sub_data['space']))
        temp_ar.append(sub_data['subg'])

        if sub_data['group'] == 'FW3_1':
            arr1.append(temp_ar)
        elif sub_data['group'] == 'FW3_2':
            arr2.append(temp_ar)
        elif sub_data['group'] == 'FW3_2':
            arr2.append(temp_ar)
        elif sub_data['group'] == 'Other':
            arro.append(temp_ar)
    
    # print("Array 1 = {}".format(arr1))
    # print("Array 2 = {}".format(arr2))
    # print("Array Other = {}".format(arro))

    return arr1,arr2,arro



#----------------------------------------------------------------------
if __name__ == "__main__":
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

    pwd = os.path.expanduser('~') + '/'
    auth_data = []
    pass_data = []

    search_auth_file(FILE_PATH_JIRA_CERT, auth_data, pass_data)
    

    jira = connect_to_jira(auth_data[0], pass_data[0])
    projects = jira.projects()

    print ("Current date & time " + time.strftime("%c"))

    if len(sys.argv) > 1:
        para = sys.argv[1]
    else:
        para = ''


    # Gaming Monitor NPI
    # para_fw3_1 = [['ASUSPG48UQ',14,'']]
    # para_fw3_2 = [['TWJVC50G22',16,''],['TWJVC65G22',16,''],['TWJVC75G22',16,''],['TWJVC32G22',16,'']]
    # para_other = [['NOVATEK',12,'PG48UQ'],['NOVATEK',12,'VG32UQA1A']]

    para_fw3_1,para_fw3_2,para_other = json_para_reader()
    


    print ("==============[FW3 - 1 Start ] ==========================================================>")

    for sub_para_ in para_fw3_1:
        project_key = sub_para_[0]
        LJUST = sub_para_[1]
        para = sub_para_[2]

        # # ALL =============================================================
        print ("=============================================================")
        jra = jira.project(project_key)
        print ("Project name = " + (jra.name))                 # 'JIRA'
        
        # print ("Project leader = " + (jra.lead._session['displayName']))
     
        jql_open,jql_resolved = jql_string_process(para, project_key)

        # print(" jql_open = {} , jql_resolved = {} \n".format(jql_open, jql_resolved)) 
        print_jira_status(jira,jql_open, jql_resolved, jra.name)
        print ("=============================================================")
        # # ALL ============================================================= END

    print ("==============[FW3 - 1 END ] =======================================================>\n\n")

    print ("==============[FW3 - 2 Start ] =====================================================>")

    for sub_para_ in para_fw3_2:
        project_key = sub_para_[0]
        LJUST = sub_para_[1]
        para = sub_para_[2]

        # # ALL =============================================================
        print ("=============================================================")
        jra = jira.project(project_key)
        print ("Project name = " + (jra.name))                 # 'JIRA'
        
        # print ("Project leader = " + (jra.lead._session['displayName']))
     
        jql_open,jql_resolved = jql_string_process(para, project_key)

        # print(" jql_open = {} , jql_resolved = {} \n".format(jql_open, jql_resolved)) 
        print_jira_status(jira,jql_open, jql_resolved, jra.name)
        print ("=============================================================")
        # # ALL ============================================================= END

    print ("==============[FW3 - 2 END ] ==========================================================>\n\n")

    print ("==============[FW3 - Other Start ] =====================================================>")

    for sub_para_ in para_other:
        project_key = sub_para_[0]
        LJUST = sub_para_[1]
        para = sub_para_[2]

        # # ALL =============================================================
        print ("=============================================================")
        jra = jira.project(project_key)
        print ("Project name = " + (jra.name))                 # 'JIRA'
        
        # print ("Project leader = " + (jra.lead._session['displayName']))
     
        jql_open,jql_resolved = jql_string_process(para, project_key)

        # print(" jql_open = {} , jql_resolved = {} \n".format(jql_open, jql_resolved)) 
        print_jira_status(jira,jql_open, jql_resolved, jra.name)
        print ("=============================================================")
        # # ALL ============================================================= END

    print ("==============[FW3 - Other END ] =========================================================>\n\n")






