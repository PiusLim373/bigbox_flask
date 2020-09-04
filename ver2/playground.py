#!/usr/bin/env python

def main():
	a = 1
	b = 2
	c = 10
	for i in range(3):
		if i==1:
			print("run if")
			c = 3
			z = 100
			
		else:
			print("run else")
			print(z)

if __name__ == "__main__":
	main()