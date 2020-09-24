#!/bin/python

import matplotlib.pyplot as plt
import sys, math

class gulp_to_slam:

	def __init__(self,*IN):

		self.__tol__ = 0.0001

		self.gulp_res_file = IN[0]
		self.slam_res_file = IN[1]
		self.slam_top_list = IN[2]

		self.gulp_rank_list = []
		self.gulp_rank_dic  = {}

		self.slam_rank_list = []
		self.slam_rank_dic  = {}

		self.slam_target_list = []
		
		# READ GULP / SLAM OUTPUT ... BEWARE ABOUT THE FORMAT

		try:
			with open(self.gulp_res_file,"r") as f:

				rl = f.readline()
				spl= rl.split()
				mx = int(spl[0])
			
				self.gulp_mx = 0				

				for i in range(mx):

					rl = f.readline()
					spl= rl.split()
	
					if spl[1] != 'x':		# if structure exists

						self.gulp_rank_list.append(spl[1])		# save structure code e.g., 'B1231'
						self.gulp_rank_dic[ spl[1] ] = float(spl[2])
						self.gulp_mx += 1


		except FileNotFoundError:
			print(FileNotFoundError)
		# GULP READ DONE

		try:
			with open(self.slam_res_file,"r") as f:

				rl = f.readline()
				spl= rl.split()
				mx = int(spl[0])

				for i in range(mx):

					rl = f.readline()
					spl= rl.split()
	
					self.slam_rank_list.append(spl[0])		# save structure code e.g., 'B1231'
					self.slam_rank_dic[ spl[0] ] = float(spl[1])

			self.slam_rank_list.reverse()
			self.slam_mx = mx

		except FileNotFoundError:
			print(FileNotFoundError)
		# SLAM READ DONE

		try:
			with open(self.slam_top_list,"r") as f:

				rl = f.readline()
				spl= rl.split()
				mx = int(spl[0])

				for i in range(mx):
				
					rl = f.readline()
					spl= rl.split()

					self.slam_target_list.append(spl[0])

		except FileNotFoundError:
			print(FileNotFoundError)
		# SLAM TARGET READ DONE

	def find_similar_structures_with_target(self):

		'''
			find energetically (structurally similar structures with 'slam' targets 
		'''
	
		number_of_targets = len(self.slam_target_list)
		self.slam_duplicates = [ [] for i in range(number_of_targets) ]		# Note that the order of stride is same with input slam target 'list'

		for i in range(self.slam_mx):

			for j in range(number_of_targets):

				diff = math.fabs( self.slam_rank_dic[ self.slam_target_list[j] ] - self.slam_rank_dic[ self.slam_rank_list[i] ] )

				if diff <= self.__tol__:
					self.slam_duplicates[j].append(self.slam_rank_list[i])

		# all target duplicates are saved in 'self.slam_duplicates'
		
	def create_nodes(self):

		self.__node_distance__ = 0.5
		self.__lhs_node_x = 1
		self.__rhs_node_x = 1 + self.__node_distance__

		# total number of movements from LHS -> RHS
		self.lhs_node_number = []
		for i in range(len(self.slam_target_list)):
			self.lhs_node_number.append( len(self.slam_duplicates[i]) )
		# end cnting
		
		self.lhs_node_set = [ [] for i in range(len(self.slam_target_list)) ]
		
		for i in range(len(self.slam_target_list)):
			for j in range(self.lhs_node_number[i]):
				self.lhs_node_set[i].append([ self.__lhs_node_x, self.gulp_rank_dic[self.slam_duplicates[i][j]] ])
		# LHS NODE DONE

		self.rhs_node_set = []

		for i in range(len(self.slam_target_list)):
			self.rhs_node_set.append( [ self.__rhs_node_x, self.slam_rank_dic[ self.slam_target_list[i]] ])
		# RHS NODE DONE

		# LHS lhs_node_set[i] ... linked to ... rhs_node_set[i]
		#print(self.slam_duplicates[0])					# order of struc code are same with
		#print(self.lhs_node_set[0],self.rhs_node_set[0])		# the order of gulp energy (lhs) to slam energy (rhs)

	def pre_plot(self):

		self.slam_gm = self.slam_rank_dic[ self.slam_rank_list[0] ]
		self.gulp_gm = self.gulp_rank_dic[ self.gulp_rank_list[0] ]

		#linestyles = ['-', '--', '-.', ':', '-']
		colours = ['black','red','blue','green','magenta']
		number_of_set = len(self.slam_target_list)

		for i in range(number_of_set):
			for j in range(self.lhs_node_number[i]):

				xvals = [ self.lhs_node_set[i][j][0], self.rhs_node_set[i][0] ]
				#yvals = [ self.lhs_node_set[i][j][1], self.rhs_node_set[i][1] ]
				yvals = [ self.lhs_node_set[i][j][1] - self.gulp_gm , self.rhs_node_set[i][1] - self.slam_gm ]
				#ls = linestyles[i]
				if i < len(colours):
					c = colours[i]
					plt.plot(xvals, yvals, color=c)
				else:
					plt.plot(xvals, yvals, linestyle='-')

		plt.xlabel("< GULP    SLAM >")
		plt.ylabel("$\Delta \mathcal{E}$ (eV)",size=12)
		plt.xlim(self.__lhs_node_x,self.__rhs_node_x)
		plt.ylim(0,3.)

		plt.show()

if __name__ == '__main__':


	inst = gulp_to_slam(sys.argv[1],sys.argv[2],sys.argv[3])
	inst.find_similar_structures_with_target()
	inst.create_nodes()
	inst.pre_plot()
