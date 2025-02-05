# coding=UTF-8
import sys
import os
import re
import time
import io
import platform
import pandas as pd

from jira import JIRA
import json

from datetime import datetime

pwd = os.path.expanduser('~') + '/'

LJUST=12
FILE_PATH_JIRA_CERT=r"D:\work_platform\Jira\auth_telly"
FILE_PATH_MODELS_JSON=r"D:\work_platform\Github\Amt_work_platform\Jira\models_telly.json"
# For testing
# FILE_PATH_MODELS_JSON=r"D:\work_platform\Github\Amt_work_platform\Jira\models_test.json"
FILE_PATH_JIRA_CSV=r"D:\work_platform\Github\Amt_work_platform\Jira\CSV\\"


FILE_PATH_JIRA_CERT_MAC= pwd + 'Documents/CERT/auth_telly'
FILE_PATH_MODELS_JSON_MAC= pwd + 'Documents/Github/Amt_work_platform/Jira/models_telly.json'
# For testing
# FILE_PATH_MODELS_JSON_MAC= pwd + 'Documents/Github/Amt_work_platform/Jira/models_test.json'
FILE_PATH_JIRA_CSV_MAC= pwd + 'Documents/Github/Amt_work_platform/Jira/CSV/'

# JIRA Statistics 
data_ = [['Temp',10, 25, 2, 4, 1, 3, 41]]
df_jira_stat = pd.DataFrame(data_, columns=['Model','OSD','SYS', 'Audio', 'PQ', 'Video','Other', 'Total' ])

# NOTE: The parameter 'displayName' (Assignee Name) could be changed for time to time
# Just print out the fields value in order to find out what the parameter name is
#--------------------------------------------------------------
def get_assignee_name(_issue):

    if(_issue.raw['fields']['assignee'] is None):
        return "Unassigned"

    return _issue.raw['fields']['assignee']['displayName']

#--------------------------------------------------------------
def time_str_covert(time_str):

    dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    desired_format = "%m/%d/%Y %H:%M:%S"
    return dt.strftime(desired_format)


#----------------------------------------------------------------------
def jira_to_csv(search_result_, project_name_,para_):

    # data = [[issue.fields.priority,issue.key, issue.fields.status,issue.fields.assignee,time_str_covert(issue.fields.created),issue.raw['fields']['customfield_10040'],issue.fields.summary]
    data = [[issue.fields.priority,issue.key, issue.fields.status,issue.fields.assignee,time_str_covert(issue.fields.created),issue.fields.reporter,issue.fields.summary]
    for issue in search_result_]

    # for issue in search_result_:
    #     print (issue.raw['fields']['customfield_10040'])

    header = ["Priority","Key", "Status","Assignee","Created","Reporter","Summary"]
 
    df = pd.DataFrame(data, columns=header)

    # print(project_name_,df)

    # Output csv files
    if (platform.system() == 'Darwin'):
        str_ =  project_name_ + para_
        str_ = str_.replace("/", "_")
        str_ = FILE_PATH_JIRA_CSV_MAC + str_ 
        # print("output str = {} , proj = {} , para = {}".format(str_, project_name_,para_))
        df.to_csv(str_ + '_' + '.csv',index=False)
    else:
        str_ = project_name_ + para_
        str_ = str_.replace("/", "_")
        str_ = FILE_PATH_JIRA_CSV + str_
        df.to_csv(str_ +  '_' + '.csv',index=False)


#----------------------------------------------------------------------
def print_jira_status(jira, jql_open, jql_resolved, proj_name, para_,speical_word = '[XXXXX]'):

    all_proj_issues = jira.search_issues(jql_open,maxResults=0)

    # print("proj_name = {} , jira_name = {}".format(proj_name, para_))
    jira_to_csv(all_proj_issues,proj_name,para_)

    # print ("{} Opening issues:".format(proj_name))
    A_Cout = 0
    B_Cout = 0
    C_Cout = 0
    pStr = 'X'
    issue_arry = []
    print_array = []

    # jira statistics 
    OSD_count = 0
    SYS_count = 0
    Audio_count = 0
    PQ_count = 0
    Video_count = 0
    Other_count = 0
    Spec_count = 0

    # for issue in all_proj_issues:
    # # print out the raw data of the all fields
    # issue = all_proj_issues[0]
    # for field_name in issue.raw['fields']:
    #     print ("Field:", field_name, "Value:", issue.raw['fields'][field_name])

    # return

    for issue in all_proj_issues:
        pStr = str(issue.fields.priority)

        # Special Word Filter
        tmp_str = str(issue.fields.summary)
        if(tmp_str.startswith(speical_word) == False):
            if(pStr == 'Highest'):
                A_Cout = A_Cout + 1
            elif(pStr == 'High'):
                B_Cout = B_Cout + 1
            elif(pStr == 'Medium'):
                C_Cout = C_Cout + 1

            # print ("[{}] {} - {} [{}]".format(issue.fields.priority, str(issue).ljust(LJUST), issue.fields.summary,get_assignee_name(issue)))
            print_array.append("[{}] {} - {} [{}]".format(issue.fields.priority, str(issue).ljust(LJUST), issue.fields.summary,get_assignee_name(issue)))

            # jira statistics
            # if(tmp_str.startswith('[OSD]')):
            #     OSD_count = OSD_count + 1
            # elif(tmp_str.startswith('[SYS]')):
            #     SYS_count = SYS_count + 1
            # elif(tmp_str.startswith('[AUDIO]')):
            #     Audio_count = Audio_count + 1
            # elif(tmp_str.startswith('[PQ]')):
            #     PQ_count = PQ_count + 1
            # elif(tmp_str.startswith('[VIDEO]')):
            #     Video_count = Video_count + 1
            # else:
            #     Other_count = Other_count + 1
            # ===================================== jira statistics END

            # New jira statistics
            if('[OSD]' in tmp_str):
                OSD_count = OSD_count + 1
            elif('[SYS]' in tmp_str):
                SYS_count = SYS_count + 1
            elif('[AUDIO]' in tmp_str):
                Audio_count = Audio_count + 1
            elif('[PQ]' in tmp_str):
                PQ_count = PQ_count + 1
            elif('[VIDEO]' in tmp_str):
                Video_count = Video_count + 1
            else:
                Other_count = Other_count + 1

            if('[SPEC]' in tmp_str):
                Spec_count = Spec_count + 1
            # ===================================== New jira statistics END

        else:
            issue_arry.append(issue)
        # print "[%s] %s - %s" %(issue.fields.priority, issue, issue.fields.summary)


    print ("[Opening Issues] {:0>2d}A {:0>2d}B {:0>2d}C, Total = {:0>2d}".format(A_Cout, B_Cout, C_Cout, A_Cout+B_Cout+C_Cout))
    for item in print_array:
        print( item )
        # print(item.encode("utf8").decode("cp950", "ignore"))
    print(" ")


    # jira statistics
    total_c = OSD_count + SYS_count + Audio_count + PQ_count + Video_count + Other_count
    print ("{} => [JIRA Statistics] OSD = {:0>2d} , SYS = {:0>2d} , Audio = {:0>2d} , PQ = {:0>2d} , VIDEO = {:0>2d}, Other = {:0>2d} (Spec = {:0>2d}), total = {:0>2d} ".format(proj_name,OSD_count,SYS_count,Audio_count,PQ_count,Video_count,Other_count,Spec_count,total_c))
    print (" ")


    str_ =  proj_name + para_
    df_jira_stat.loc[len(df_jira_stat)] = [str_, OSD_count, SYS_count, Audio_count, PQ_count, Video_count, Other_count, total_c]

    all_proj_issues = jira.search_issues(jql_resolved,maxResults=0)

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
            if(pStr == 'Highest'):
                A_Cout = A_Cout + 1
            elif(pStr == 'High'):
                B_Cout = B_Cout + 1
            elif(pStr == 'Medium'):
                C_Cout = C_Cout + 1

            # print ("[{}] {} - {} [{}]".format(issue.fields.priority, str(issue).ljust(LJUST), issue.fields.summary, get_assignee_name(issue)))
            print_array.append("[{}] {} - {} [{}]".format(issue.fields.priority, str(issue).ljust(LJUST), issue.fields.summary, get_assignee_name(issue)))
        else:
            issue_resolved_arry.append(issue)


    print ("[Resolved Issues] {:0>2d}A {:0>2d}B {:0>2d}C, Total = {:0>2d}".format(A_Cout, B_Cout, C_Cout, A_Cout+B_Cout+C_Cout))
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
            if(pStr == 'Highest'):
                A_Cout = A_Cout + 1
            elif(pStr == 'High'):
                B_Cout = B_Cout + 1
            elif(pStr == 'Medium'):
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
    jira_options = { 'server': 'https://teevee.atlassian.net/'}

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
        # jql_open_ = 'project = ' + project_key_ + ' AND resolution = Unresolved ORDER BY priority DESC, updated DESC'
        # jql_resolved_ = 'project = ' + project_key_ + ' AND status = Resolved ORDER BY priority DESC, updated DESC' 
        jql_open_ = 'project = ' + project_key_ + ' AND status != Done ORDER BY priority DESC, updated DESC'
        jql_resolved_ = 'project = ' + project_key_ + ' AND status = Done ORDER BY priority DESC, updated DESC'
         
    elif para_ == 'ac':
        jql_open_ = 'project = ' + project_key_ + ' ORDER BY priority DESC, updated DESC'
        jql_resolved_ = 'project = ' + project_key_ + ' AND status = Resolved ORDER BY priority DESC, updated DESC' 
    elif para_ == '':
        # jql_open_ = 'project = ' + project_key_ + ' AND resolution = Unresolved AND component in (AUDIO, EE, PQ, SW, FW) ORDER BY priority DESC, updated DESC'
        # jql_resolved_ = 'project = ' + project_key_ + ' AND status = Resolved  AND component in (AUDIO, EE, PQ, SW, FW) ORDER BY priority DESC, updated DESC'
        jql_open_ = 'project = ' + project_key_ + ' AND status != Done ORDER BY priority DESC, updated DESC'
        jql_resolved_ = 'project = ' + project_key_ + ' AND status = Done ORDER BY priority DESC, updated DESC'
    else:
        # jql_open_ = 'project = ' + project_key_ + ' AND resolution = Unresolved AND component = ' + '"' + para_ + '"' + ' ORDER BY priority DESC, updated DESC'
        # jql_resolved_ = 'project = ' + project_key_ + ' AND status = Resolved  AND component = ' + '"' + para_ + '"' + ' ORDER BY priority DESC, updated DESC'
        jql_open_ = 'project = ' + project_key_ + ' AND status != Done ORDER BY priority DESC, updated DESC'
        jql_resolved_ = 'project = ' + project_key_ + ' AND status = Done ORDER BY priority DESC, updated DESC'

    # print(" jql_open_ = " + jql_open_)

    return jql_open_,jql_resolved_

#----------------------------------------------------------------------
def json_para_reader():

    if (platform.system() == 'Darwin'):
        with open(FILE_PATH_MODELS_JSON_MAC) as f:
            data = json.load(f)
    else:
        with open(FILE_PATH_MODELS_JSON) as f:
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
        elif sub_data['group'] == 'Other':
            arro.append(temp_ar)
    
    # print("Array 1 = {}".format(arr1))
    # print("Array 2 = {}".format(arr2))
    # print("Array Other = {}".format(arro))

    return arr1,arr2,arro

#----------------------------------------------------------------------
def print_group(para_in_, str_):
    print ("==============[" + str_ + "Start ] ==========================================================>")

    for sub_para_ in para_in_:
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
        print_jira_status(jira,jql_open, jql_resolved, jra.name, para)
        print ("=============================================================")
        # # ALL ============================================================= END

    print ("==============[" + str_ + "END ] =======================================================>\n\n")


#----------------------------------------------------------------------
if __name__ == "__main__":
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

    auth_data = []
    pass_data = []

    if (platform.system() == 'Darwin'):
        search_auth_file(FILE_PATH_JIRA_CERT_MAC, auth_data, pass_data)
    else:
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

    print_group(para_fw3_1,"FW3 - 1")
    print_group(para_fw3_2,"FW3 - 2")
    print_group(para_other,"FW3 - Other")

    df_jira_stat=df_jira_stat.drop(df_jira_stat.index[0])
    # print(df_jira_stat)

    # Output csv files
    if (platform.system() == 'Darwin'):
        str_ = FILE_PATH_JIRA_CSV_MAC + 'Jira_Statistic' 
        df_jira_stat.to_csv(str_ + '_' + '.csv',index=False)
    else:
        str_ = FILE_PATH_JIRA_CSV + 'Jira_Statistic'
        df_jira_stat.to_csv(str_ +  '_' + '.csv',index=False)

    