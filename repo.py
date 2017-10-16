import re
import tempfile
import datetime
import re
import subprocess
import os


class Repository(object):
    

    def __init__(self,host,port,database,schema,repository,user,password):
        self.geogigPath = '/opt/geogig/bin/geogig'  
        self.repoUrl = "postgresql://{}:{}/{}/{}/{}?user={}&password={}".format(host,port,database,schema,repository,user,password)
        self.branches = {}
        try:
            result = subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'branch'])
            branch_names = [x.strip().replace('* ', '') for x in result.split('\n')][:-1]
            
            for b in branch_names:
                self.branches[b] = Branch(b,self.geogigPath,self.repoUrl)
        except Exception as e:
            #print e
            pass     

 
    def config(self,username,email):
        try:
            subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'config','--global','user.name',username])
            subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'config','--global','user.email',email])
            
        except Exception as e:
            return e
            
    def init(self):
        try:
            result = subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'init'])
            self.branches['master'] = Branch('master',self.geogigPath,self.repoUrl)
            return result
        except Exception as e:
            return e

    def clone(self,host,port,database,schema,repository,user,password):
        try:
            dest = "postgresql://{}:{}/{}/{}/{}?user={}&password={}".format(host,port,database,schema,repository,user,password)
            result = subprocess.check_output([self.geogigPath,'clone',self.repoUrl,dest])
            return result
        except Exception as e:
            return e



    def add_branch(self,branchName):
        try:
            result = subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'branch',branchName])
            msg = subprocess.STDOUT
            print msg

            self.branches[branchName] = Branch(branchName,self.geogigPath,self.repoUrl)
            return result
        except Exception as e:
            print e
            return e
        

    def del_branch(self,branchName):
        try:
            result = subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'branch','--delete',branchName])
            self.branches[branchName]
        except Exception as e:
            return e


class Branch(object):
    def __init__(self,branchName, geogigPath, repoUrl):
        self.name = branchName
        self.geogigPath = geogigPath
        self.repoUrl = repoUrl

    def __checkout(self):
        result =  subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'status']).split('\n')[0]
        active_branch = result.replace('# On branch ','')
        if active_branch != self.name:
            try:
                subprocess.call([self.geogigPath,'--repo',self.repoUrl,'checkout',self.name])
            except Exception as e:
                print e
                return e

    def add(self,layer=None):
        self.__checkout()
        if layer == None:
            result =  subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'add'])
        return result

    def push(self,branchName):
        self.__checkout()
        try:
            result=subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'push','origin',branchName])
            print result
            return result
        except Exception as e:
            return e
    
    def pull(self,branchName):
        self.__checkout()
        try:
            result = subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'pull','origin',branchName])
            print result
            return result
        except Exception as e:
            return e
        
    
    def merge(self,branchName):
        self.__checkout()
        try:
            result = subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'merge',branchName])
            print result
            return result
            
        except Exception as e:
            return e
    
    def pg_import_schema(self,host,port,database,schema,user,password):
        self.__checkout()
        result = subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'pg','list','--host',host,'--port',port,'--database',database,'--schema',schema,'--user',user,'--password',password])
        layers = [x.replace('-', '').strip() for x in result.split('\n') if x.strip() != ''][1:]
        for layer in layers:
            result = subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'pg','import','--table', layer, '-d', schema+'/'+layer,'--schema',schema,'--host',host,'--port',port,'--database',database,'--user',user,'--password',password,'--force-featuretype'])
            print "layer: " + layer + " ok!"
        print "ok!"

    def pg_export_schema(self,host,port,database,schema,user,password):
        self.__checkout()
        layers = []
        try:
            result = subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'ls',schema])
            layers = [x.replace('/', '').strip() for x in result.split('\n') if x.strip() != ''][1:]
            for layer in layers:
                
                result = subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'pg','export','--host',host,'--port',port,'--database',database,'--user',user,'--password',password,'--schema',schema,'HEAD:'+schema+'/'+layer, layer,'--overwrite'])
                
                print "layer: " + layer + " ok!"
            print "fim do processo"
        except subprocess.CalledProcessError as e:
            print e
            return e

            
    
    def log(self):
        
        self.__checkout()
        result =  subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'log'])
        logs = []
        aux = {}
        for line in [x for x in result.split('\n') if x.strip()!= '']:
            if line.find('Commit') > -1:
                if 'commit' in aux:
                    logs.append(aux)
                    aux = {}
                aux['commit'] = line.split(':')[1].strip()

            if line.find('Author') > -1:
                    aux['author'] = line.split(':')[1].strip()
            if line.find('Subject') > -1:
                    aux['subject'] = line.split(':')[1].strip()
            if line.find('Date') > -1:
                    aux['date'] = ':'.join(line.split(':')[1:]).strip()
            if line.find('Merge') > -1:
                    aux['Merge'] = line.split(':')[1].strip()

        logs.append(aux)
        return logs
        
    
    def status(self):
        self.__checkout()
        result =  subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'status'])
        print result
    
    def commit(self,msg):
        self.__checkout()
        result = subprocess.check_output([self.geogigPath,'--repo',self.repoUrl,'commit','-m',msg])
        return result
    