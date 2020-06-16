import pandas as pd

df = pd.read_csv("ports_assigned.csv")

student_id = df["student_id"]
ports = df["ports"]

id2port = dict(zip(student_id, ports))

your_id = input("This is the checking script Winter 2020. What's your student ID? (enter the 9-digits number)\n")
your_ports = id2port.get(int(your_id))
if your_ports is not None:
	print("Your ports are: {}".format(your_ports))
else:
	print("There's something wrong with your ID, we couldn't find your port. Please contact the TAs for help.")
	print("Or probably you are checking it too early and we haven't assigned the ports for this quarter.")