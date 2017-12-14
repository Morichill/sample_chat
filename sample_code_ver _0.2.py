
from socket import *

#main class of the chat
class ChatClass:

	#default constructor
	def __init__ ( self, address ):
		self.messages = []
		self.users = []
		self.listener = socket( AF_INET, SOCK_STREAM )
		self.listener.bind( address )
		self.listener.listen(3)
		
	def findUserByIP( self, ip ):
		if( len( self.users ) == 0 ):
			return -1
		for i in range( len( self.users ) ):
			if( self.users[i][0] == ip ):
				return i
		return -1
		
	def findUserByName( self, name ):
		if( len( self.users ) == 0 ):
			return -1
		for i in range( len( self.users ) ):
			if( self.users[i][1] == name ):
				return i
		return -1
		
	def loggedIn( self, ip ):
		if( self.findUserByIP( ip ) != -1 ):
			return 1
		return 0
		
	def main_loop(self):
		while(1):
			conn, addr = self.listener.accept()
			print "Connection form ", addr
			temp = conn.recv( 100 )
				
			#login
			if( temp.find( "<login>" ) == 0 ):
				if( self.loggedIn( str(addr[0]) ) == 0 ):
					self.users.append( (str(addr[0]), str(addr[0])) )
					conn.send( "1" )
				else:
					print "User already logged in"
					conn.send( "0" )
				
			#if a user isn't logged in then all actions aren't available for him
			if( self.loggedIn( str(addr[0]) ) == 0 ):
				print "Error! User is not logged in"
				conn.send( "0" )
				conn.close()
				continue
			
			#get user's num and nick
			num = self.findUserByIP( str(addr[0]) )
			name = self.users[num][1]
			
			#if we have a new message
			if( temp.find( "<message>" ) == 0 ):
				#add user's message to messages array
				self.messages.append( name + ": " + temp.replace( "<message>", "", 1 ) )
				
				#print all messages (this is a test action)
				print ""
				for mes in self.messages:
					print mes
				conn.send( "1" )
					
			#if we have a request for messages
			if( temp.find( "<get messages>" ) == 0 ):
				number = 0;
				
				#check if a user wants to get only last messages
				if ( temp.replace( "<get messages>", "", 1 ) != "" ):
					number = int(temp.replace( "<get messages>", "", 1 ))
				
				#check message num
				if( len(self.messages) - number <= 0 ):
					print "Cann't send messages: out of bounds"
					conn.send( "0" )
					conn.close()
					continue
				
				#send messages to user
				conn.send( "1" )
				conn.send( str(len(self.messages) - number) )
				for i in range( len(self.messages) - number ):
					conn.send( self.messages[i+number] )
					print self.messages[i+number]
					
			#if user wants to change his nick
			if( temp.find( "<switch>" ) == 0 ):
			
				#get new user's nick
				newName = temp.replace( "<switch>", "", 1 )
				if( newName == "" ):
					newName = name
				print "newName = " + newName
				
				#check if there is a user with such nick
				if( self.findUserByName( newName ) != -1 ):
					print "Cann't change user's nick"
					conn.send( "0" )
					conn.close()
					continue
				
				#remove old user's nick
				self.users.remove( self.users[num] )
				
				#insert new user's nick
				self.users.append( (str(addr[0]), newName ) )
				
				#print debug message
				self.messages.append( "---" + str(addr[0]) + " now known as " + newName + "---" )
				conn.send( "1" )
				
			#if user wants to terminate server
			if( temp.find( "<server terminate>" ) == 0 ):
				#only admin can terminate server
				if( name == "admin" ):
					print "server terminates"
					conn.close()
					break;
				else:
					print "Error: only admin can terminate server"
					
			#logout
			if( temp.find( "<logout>" ) == 0 ):
				print "User " + name + " has logged out"
				self.users.remove( self.users[num] )
				
			#bot sample_#0001 - I'm too lazy to fix this shit
			if (temp.find ( "<get_bot>" ) == 0 ):
			  print "bot here"
			  print "bitches."
			  
			  if (temp.find ("<bot_play>"> == 0):
			   print "start music from YouTube"
			   
			   # На данный момент вырезал к чертям ибо проблем уйма, мб потом когшда-нибудь допилить"
			  
		  
			  
			  
			conn.close()
		self.listener.close()
		
chat = ChatClass( ("127.0.0.1", 11111 ) )
chat.main_loop()
