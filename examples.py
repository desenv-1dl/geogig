from repo import Repository


#---------------------------REPOSITORIO SERVIDOR-----------------------------------------------------
#repositorio = Repository('10.25.163.18','5432','repositorio','repositorios','cl_rincao','cesar','senha')

#---------------------------REPOSITORIO CLIENTE-----------------------------------------------------
repositorio = Repository('localhost','5432','repositorio','repositorios','cl_rincao','cesar','senha')


#----------------CRIANDO REPOSITORIO-----------------------

#repositorio.init()
repositorio.config('cesar','cesar@dsg.eb.mil.br')

#---------------CRIANDO REPOSITORIO - IMPORTANDO DADOS DO BANCO------------------
#repositorio.branches['master'].pg_import_schema('10.25.163.18','5432','cl_rincao','dominios','cesar','senha')
#repositorio.branches['master'].add()
#repositorio.branches['master'].commit('inicio de projeto')
#print repositorio.branches['cesar'].log()
#print  repositorio.branches['master'].merge('cesar')

#---------------NOVO BRANCH--------------------------------------------
#repositorio.add_branch('cesar')
#print repositorio.branches['cesar'].log()

#---------------CLONANDO O REPOSITORIO---------------------------------
#repositorio.clone('localhost','5432','repositorio','repositorios','cl_rincao','cesar','senha')
#repositorio.config('cesar','cesar@dsg.eb.mil.br')
#---------------PUSH PULL --------------------------
#repositorio.branches['cesar'].pull('cesar')
#repositorio.branches['cesar'].push('cesar')



#print repositorio.branches['master'].log()[0]['author']
#destino = "postgresql://localhost:5432/repositorio/public/repositorio?user=cesar&password=senha"
#print repositorio.repo
#repositorio.init()
#print repositorio.branches
#print repositorio.branches
#print repositorio.branches['master'].log()[0]['author']
#print repositorio.branches['alves'].add()

#repositorio.init()
#host,port,database,schema,repository,user,password
#repositorio.clone('localhost','5432','repositorio','repositorios','cl_rincao','gg_cesar','senha')

#repositorio.branches['cesar'].pg_import_schema('localhost','5432','cl_rincao','dominios','cesar','senha')




#repositorio.branches['cesar'].status()
#repositorio.branches['master'].pg_export_schema('10.25.163.18','5432','teste_merge','public','cesar','senha')
#print "dominios ok"
#repositorio.branches['master'].pg_export_schema('localhost','5432','cl_rincao','dominios ','cesar','senha')

#print repositorio.branches['cesar'].log()
#print repositorio.branches

#repositorio.branches['cesar'].push('cesar')

#---------------------MERGE--------------------
#repositorio.branches['master'].merge('cesar')