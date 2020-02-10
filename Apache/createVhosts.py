"""
################################################################
################################################################
This program is to make it it easier to create new vhosts. 

1. Accept input for primary site
2. Accept input for aliases
3. Create vhosts to redirect to ssl non-www version
        See https://bugs.chromium.org/p/chromium/issues/detail?id=883038#c114for why I selected the non-www versions
3. Create SSLHosts.
################################################################
################################################################
"""
from subprocess import Popen, PIPE
import os
import time
from os import path

def get_primaryDomain():
        primaryDomain=''
        try:
                #Keep looping until input is given
                while primaryDomain =='':
                        primaryDomain = input("What is the domain you want \n")
                return primaryDomain
        except:
                return get_primaryDomain()
        

def get_domainAliases():
        try:
                domainAliases = input("List of domainAliases sepearated by commas \n")   # takes the whole line of n numbers
                aliasArray = list(map(str,domainAliases.split(',')))
                return aliasArray
        except:
                print("something went wrong")

        print(aliasArray)

def get_configfiles():
        """"
        ###########################################################################################
        ###########################################################################################
        # We need to get all config files so it's more dynamic
        # Currently only takes two files, one for Vhosts and one for SSL HOSTS
        ###########################################################################################
        ###########################################################################################
        """"
        configArray=''
        try:
                print(len(configArray))
                while len(configArray) == 0:
                        configFiles = input("List of Configuration and Files sepearated by commas \n")   # takes the whole line of n numbers
                        configArray = list(map(str,configFiles.split(',')))
                      #  print("config array 0" + configArray[0])
                       # print("config array 1" + configArray[1])
                        print("config array 0" + configArray[0])
                        if configArray[0] == '':
                                print("config array has no input")
                                del configArray[:]
                        print(len(configArray))
                        #print(configArray[0])
                return configArray[0], configArray[1]
        except:
                print("something went wrong")

def createVhostEntry(primaryDomain, aliasArray):
        try:
                ### TODO ###
                ### ACCEPT APACHE IP ###
                ### ACCEPT VHOST FILE LOCATION ###
                ## /TODO ###
                vhostString = "\n <VirtualHost *:80> \n ServerName " + primaryDomain + "\n RedirectPermanent / https://"+ primaryDomain +"\n </VirtualHost> \n"
                print(vhostString)
                vhostFile = open('Vhosts.conf', "a+")
                vhostFile.write(vhostString)
        
        except exception as error:
                print(error)
def createSSLHostEntry(primaryDomain, aliasArray):
        """
        ### TODO ###
                ### ACCEPT APACHE IP ###
                ### ACCEPT VHOST FILE LOCATION ###
        ### /TODO ###

        """"
        try:
               
                SSlString = "\n <VirtualHost *:443> \n ServerName " + primaryDomain + "\n DocumentRoot /var/www/html/"+ primaryDomain +"\n ErrorLog /var/log/apache/" + primaryDomain + "-error_log \n TransferLog /var/log/apache" + primaryDomain + "-access_log \n SSLProxyEngine On \n SSLCertificateFile /etc/letsencrypt/live/" + primaryDomain + "/fullchain.pem \n SSLCertificateKeyFile /etc/letsencrypt/live/" + primaryDomain + "/privkey.pem \n SSLCipherSuite EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA !RC4 !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS \n</VirtualHost> \n"
                print(SSlString)
                vhostFile = open('SSLHosts.conf', "a+")
                vhostFile.write(SSlString)
        
        except exception as error:
                print(error)
def checkapacheconfig(configfile1):
        
        """
        Temporarily write the config file location in the main apache config so we can do a config check. Then remove the line so we don't create uneccessary lines.

        
        """
        
        configPath=os.path.abspath(configfile1)
        apachefile= '/etc/apache2/apache2.conf'
        configFile = open(apachefile, "a+")
        insertedLine="\nInclude " + "\"" + configPath + "\""
        configFile.write(insertedLine)
        
        # https://stackoverflow.com/questions/7257442/test-apache-config-file-from-python
        args = ['/usr/sbin/apachectl','configtest']

        result = Popen(args,stdout=PIPE,stderr=PIPE,stdin=PIPE).communicate()
        # Delete the added include line
        message=b'Syntax OK\n'
        if  result[1]==message:
                print("syntax is great")
        else:
                print("Can't move forward please view syntax\n")
                print(result[1])
        #delete_line_by_full_match(apachefile,insertedLine)
        # result[0] will be the standard output, result[1] will be the stderr output
# https://thispointer.com/python-how-to-delete-specific-lines-in-a-file-in-a-memory-efficient-way/
def delete_line_by_full_match(original_file, line_to_delete):
    """ In a file, delete the lines at line number in given list"""
    is_skipped = False
    dummy_file = original_file + '.bak'
    # Open original file in read only mode and dummy file in write mode
    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Line by line copy data from original file to dummy file
        for line in read_obj:
            line_to_match = line
            if line[-1] == '\n' | line[-1]=='\r\n':
                line_to_match = line[:-1]
            # if current line matches with the given line then skip that line
            if line_to_match != line_to_delete:
                write_obj.write(line)
            else:
                is_skipped = True
 
    # If any line is skipped then rename dummy file as original file
    if is_skipped:
        os.remove(original_file)
        os.rename(dummy_file, original_file)
    else:
        os.remove(dummy_file)
def checkDocumentRoot(DocumentRoot):
                """"
        ###########################################################################################
        ###########################################################################################
        # 1. Get Document roots
        # 2. Check if the folder exists
        # 3. If it doesn't create it.
        ### TODO ###
        1. Call other function to create users and permissions for fpm
        ###########################################################################################
        ############################
                """
        if path.exists(DocumentRoot):
                if (path.isdir(DocumentRoot)):
                        print("Document Root already Exists")
                else:
                        print("there was a file with the same name I moved it to .bak")
                        os.rename(DocumentRoot, DocumentRoot + ".bak")
                        os.mkdir(DocumentRoot)
                        print("Directory is now created ")
        else:
                os.rename(DocumentRoot, DocumentRoot + ".bak")
                os.mkdir(DocumentRoot)
                print("created the Document root")
if __name__ == "__main__":
    primaryDomain=get_primaryDomain()
    aliasArray=get_domainAliases()
    config1, config2=configFiles=get_configfiles()
    createVhostEntry(primaryDomain, aliasArray)
    createSSLHostEntry(primaryDomain, aliasArray)
    checkDocumentRoot(DocumentRoot)
    checkapacheconfig(configfile1="Vhosts.conf")
    checkapacheconfig(configfile1="SSLHosts.conf")
