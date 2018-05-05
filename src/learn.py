#!/usr/bin/env python

from Mdp import *
from Parking import *
from tqdm import tqdm
from multiprocessing import Pool
import statistics as stats
import argparse as ap
import random as rnd
import matplotlib.pyplot as plt
import csv

class Learner:

	def __init__(self,m,n,discount,lrate):
		self.m = m
		self.n = n
		self.discount = discount
		self.lrate = lrate
		self.Q = [[0.0 for a in range(self.m)] for s in range(self.n)]
		self.R = {(s,a):[] for a in range(self.m) for s in range(self.n)}
		self.history = []

	def __exit__(self):
		pass

	def observe(self, sn, rnet=None):
		if rnet is None:
			self.history = []
		else:
			self.history.append({
				's': self.s,
				'a': self.a,
				'rnet': rnet,
			})
		self.s = sn

	def greedy(self,epsilon=0.0):
		self.a = np.argmax(self.Q[self.s]) if(np.random.rand() >= epsilon) else rnd.randint(0,self.m-1)

	def learn(self,r,sn,epsilon=0.0):
		an = np.argmax(self.Q[sn]) if(np.random.rand() >= epsilon) else rnd.randint(0,self.m-1)
		self.Q[self.s][self.a] += self.lrate*(r + self.discount*self.Q[sn][an] - self.Q[self.s][self.a])

	def mc(self):
		appeared = set()
		for h in reversed(self.history):
			s = h['s']
			a = h['a']
			rnet = h['rnet']
			if (s,a) not in appeared:
				self.R[(s,a)].append(rnet)
				self.Q[s][a] = stats.mean(self.R[(s,a)]) if len(self.R[(s,a)]) > 0 else 0.0
				appeared.add((s,a))
		self.history = []

# Simulates a number of MDP epochs for a given policy
def worker(args):
	mdp			= args['mdp']
	initial		= args['initial']
	discount	= args['discount']
	episode		= args['episode']
	method		= args['method']
	epochs		= args['epochs']
	lrate		= args['lrate']
	epsilon		= args['greedy']
	rwds		= []
	agent = Learner(m=mdp.m, n=mdp.n, discount=discount, lrate=lrate)
	for epoch in range(epochs):

		# Learning
		mdp.init_sim(discount=discount, initial=initial)
		agent.observe(initial)
		for i in range(episode):
			agent.greedy(epsilon)
			r,sn = mdp.act(agent.a)
			if method == 'Q':
				agent.learn(r,sn)
			if method == 'SARSA':
				agent.learn(r,sn,epsilon=epsilon)
			agent.observe(sn,mdp.get_net_reward())
		if method == 'MC':
			agent.mc()

		# Evaluating
		if epoch%10 == 0:
			mdp.init_sim(discount=discount, initial=initial)
			agent.observe(initial)
			for i in range(episode):
				agent.greedy()
				r,sn = mdp.act(agent.a)
				agent.observe(sn)
			rwds.append(mdp.get_net_reward())

	return rwds

# Main
def main():

	# Parsing user input
	parser = ap.ArgumentParser()
	parser.add_argument(
			'-i','--input',
			nargs='?',
			required=True,
			help='Input MDP file name.'
		)
	parser.add_argument(
			'-p','--plot',
			nargs='?',
			required=True,
			help='Plot output file name.'
		)
	parser.add_argument(
			'-o','--initial',
			nargs='?',
			type=int,
			default=0,
			help='The initial state.'
		)
	parser.add_argument(
			'-d','--discount',
			nargs='?',
			type=float,
			default=0.9,
			help='The discount value.'
		)
	parser.add_argument(
			'-e','--episode',
			nargs='?',
			type=int,
			default=20,
			help='Episode episode length.'
		)
	parser.add_argument(
			'-s','--epochs',
			nargs='?',
			type=int,
			default=100,
			help='Number of learning epochs (number of espisodes).'
		)
	parser.add_argument(
			'-l','--lrate',
			nargs='?',
			type=float,
			default=0.01,
			help='The learning rate.'
		)
	parser.add_argument(
			'-t','--threads',
			nargs='?',
			type=int,
			default=100,
			help='Number of parallel processing threads for statistical runs.'
		)
	parser.add_argument(
			'-v','--verbose',
			action='count',
			help='Verbose mode.'
		)
	args = parser.parse_args()

	# Loading and checking MDP
	mdp = Mdp(args.input,verbose=args.verbose)
	error_code = mdp.validate_model()
	if error_code:
		Mdp.print_format_error(error_code=error_code)

	METHODS = [(0.30,'Q'),(0.30,'SARSA'),(0.30,'MC'),(0.05,'Q'),(0.05,'SARSA'),(0.05,'MC')]

	for method in METHODS:

		# Simulating multiple statistical epochs across multiple threads
		pool = Pool(processes=args.threads)
		worker_args = [
					{
						'mdp':		Mdp(T=mdp.T,R=mdp.R,m=mdp.m,n=mdp.n,verbose=args.verbose),
						'initial':	args.initial,
						'discount':	args.discount,
						'episode':	args.episode,
						'method':	method[1],
						'epochs':	args.epochs,
						'lrate':	args.lrate,
						'greedy':	method[0],
					} for i in range(args.threads)
				]
		rwds = pool.map(worker,worker_args)
		rwds = map(list,zip(*rwds))

		val = [stats.mean(r) for r in rwds]
		err = [1.95*stats.stdev(r)/(len(r)**0.5) for r in rwds]

		plt.errorbar([10*r for r in range(len(val))], val, yerr=err)

	plt.xlabel('Epoch')
	plt.ylabel('Total Accumulated Discounted Rewards')
	plt.legend(['%.2f-greedy %s'%m for m in METHODS], loc='best')
	plt.savefig(args.plot, bbox_inches='tight')


if __name__ == "__main__":
	main()


