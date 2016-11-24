# -*- coding:utf-8 -*-
import commands
import ConfigParser
import re
import os


class SvnProcesser:
    """处理svn版本的类"""
    __config = ConfigParser.ConfigParser()
    __trunk_path = ''
    __online_path = ''

    def __init__(self):
        self.__config.read('config.ini')
        self.__trunk_path = self.__config.get('local_file_system', 'trunk_path')
        self.__online_path = self.__config.get('local_file_system', 'online_path')

    def __get_modified_files(self, revision):
        svn_log = commands.getoutput('svn log -v -r ' + str(revision) + ' ' + self.__config.get('local_file_system', 'trunk_path'))
        file_dictionary = {}
        p = re.finditer(r'((?<=  )\w)( )(\S*)((?<=/mobile/CardPirate/trunk/cocos2d-x-2.2.3/projects/CardPirate/)\S*(?=\n| ))', svn_log)
        for i in p:
            file_dictionary[i.group(4)] = i.group(1)

        return file_dictionary

    def __run_command_by_status(self, file_name, status):
        file_path = self.__trunk_path + file_name
        des_path = self.__online_path + file_name
        if status == 'M':
            if os.path.isfile(file_path):
                print commands.getoutput('cp' + ' ' + file_path + ' ' + des_path)
        elif status == 'D':
            if os.path.isfile(file_path):
                print commands.getoutput('svn rm' + ' ' + des_path)
            elif os.path.isdir(file_path):
                print commands.getoutput('svn rm -r' + ' ' + des_path)
        elif status == 'A':
            if os.path.isfile(file_path):
                print commands.getoutput('cp' + ' ' + file_path + ' ' + des_path)
            elif os.path.isdir(file_path):
                print commands.getoutput('cp -r' + ' ' + file_path + ' ' + os.path.dirname(des_path))
            if filter(str.isupper, commands.getoutput('svn st ' + des_path + ' | ' + "awk '{print $1}'")) == 'M':
                print commands.getoutput('svn add' + ' ' + des_path)
        else:
            print '--------------------------'
            print "No such status:" + status
            print file_name
            print '--------------------------'

    def copy_file_to_online(self, revision):
        file_dict = self.__get_modified_files(revision)
        for file_name in file_dict:
            print file_name + "  " + file_dict[file_name]
            self.__run_command_by_status(file_name, file_dict[file_name])

    def commit_online_files(self, commit_notes):
        print commands.getoutput('svn commit -m "' + commit_notes + '" ' + self.__online_path)

    def update_all_files(self):
        print commands.getoutput('svn up ' + self.__trunk_path)
        print commands.getoutput('svn up ' + self.__online_path)

if __name__ == "__main__":
    svnProcesser = SvnProcesser()
    svnProcesser.copy_file_to_online(193917)