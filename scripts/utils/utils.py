import rospy
import socket, os, time

# Makes a service call to the server
def service_call(serviceName, service, arguments):
	rospy.wait_for_service(serviceName)
	try:
		function = rospy.ServiceProxy(serviceName, service)
		state = function(*arguments)
		return state
	except rospy.ServiceException, e:
		print("Service call failed: %s" % e)
		return None

# Print out the help text for all valid commands
def useage(validCommands):
	print("Valid Commands:")
	for c in validCommands:
		print(validCommands[c][2])

# Runs an API function using sys arguments from command line. See any client file for format of validCommands
def commandToFunction(sysargs, validCommands, debug=False):

	state = None
	start = time.time()

	# if no command is given, print out valid commands and return none
	if len(sysargs) < 2:
		useage(validCommands)
		return state

	# first argument is command
	command = str(sysargs[1]).lower()

	# is a valid command
	if command in validCommands:
		function, argumentTypes, helpStr = validCommands[command][0], validCommands[command][1], validCommands[command][2]

		# correct number of arguments         + 2 for file name and command name
		if len(sysargs) == len(argumentTypes) + 2:

			# convert arguments to correct types
			arguments = []
			for i in range(len(argumentTypes)):
				try:
					arguments.append(argumentTypes[i](sysargs[i+2]))
				except:
					print("Invalid Arguments! Use: " + helpStr)
					break

			# if all converted correctly, call the function with new arguments
			if len(arguments) == len(argumentTypes):
				state = function(*arguments, debug=debug)

		else:
			print("Invalid Arguments! Use: " + helpStr)

	# invalid command -> print help for all valid commands
	else:
		useage(validCommands)		


	end = time.time()
	#print(end - start)

	# return state of called function
	return state

def help(my_location, help_file, debug = False):
	helpFile = open(os.path.join(my_location, help_file))
	helpStr = helpFile.read()
	print(helpStr)
	helpFile.close()
	return helpStr