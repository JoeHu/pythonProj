# -*- coding:utf-8 -*-
"""
处理redmine的脚本
"""

import ConfigParser
import os
import re

from WorkTools import SvnProcesser as Svn
from WorkTools.RedmineProcesser import RedmineProcesser as Redmine

if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')
    print 'please input redmine number:'
    issueNumber = raw_input()

    redmineRoot = Redmine('/issues/'+str(issueNumber))
    redmineList = []
    revisionList = []
    for issueLocate in redmineRoot.sub_issue_list():
        print issueLocate
        redmine = Redmine(issueLocate)
        # 此处判断redmine中的版本号列表不为空,才加入操作的列表中
        if redmine.svn_revision_list():
            redmineList.append(redmine)
            for revision in redmine.svn_revision_list():
                if revision not in revisionList:
                    revisionList.append(revision)

    print 'revision numbers:'

    for revision in revisionList:
        print revision,

    print '\nupdate the files'

    Svn.update_all_files()

    print 'merge the files'

    print revisionList

    print 'some of the revision maybe not correct'
    print 'do you want to remove some of the revision?'
    remove_revision = raw_input()
    remove_list = re.findall(r'\d{3},?\d{3}', remove_revision)
    for revision in remove_list:
        if revision in revisionList:
            revisionList.remove(revision)

    print revisionList

    print 'please check the files manually'

    for revision in revisionList:
        Svn.copy_file_to_online(revision)

    print 'commit or not?(y/n)'
    commit = raw_input()

    if commit == 'y':
        commit_revision = Svn.commit_online_files(redmineRoot.get_svn_note())
        if commit_revision is None:
            commit_revision = ''
        note = commit_revision + '已合并'

        for redmine in redmineList:
            redmine.change_issue_to_qa_and_state_feedback(note)
