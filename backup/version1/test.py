from py4j.java_gateway import JavaGateway                 
gateway = JavaGateway()                                   
entrypt = gateway.entry_point.getMove()             
result = entrypt.myMove()
for r in result:
	print r