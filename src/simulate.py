#!/usr/bin/env python

from Mdp import *
from Parking import *
from tqdm import tqdm
from multiprocessing import Pool
import statistics as stats
import argparse as ap
import random
import csv

# Simulates a number of MDP runs for a given policy
def worker(args):
	mdp			= args['mdp']
	policy		= args['policy']
	runs		= args['runs']
	episode		= args['episode']
	discount	= args['discount']
	initial		= args['initial']
	rwds		= []
	for r in range(runs):
		ret = mdp.init_sim(discount=discount, initial=initial)
		s = initial
		for i in range(episode):
			cdf = np.cumsum(policy[s])
			a = np.searchsorted(cdf,np.random.rand())
			r,s = mdp.act(a)
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
			'-p','--policy',
			nargs='?',
			required=True,
			help='Policy file to simulate.'
		)
	parser.add_argument(
			'-r','--runs',
			nargs='?',
			type=int,
			default=10000,
			help='Number of statistical runs.'
		)
	parser.add_argument(
			'-t','--threads',
			nargs='?',
			type=int,
			default=10,
			help='Number of parallel processing threads.'
		)
	parser.add_argument(
			'-l','--length',
			nargs='?',
			type=int,
			default=100,
			help='Episode length.'
		)
	parser.add_argument(
			'-d','--discount',
			nargs='?',
			type=float,
			default=0.9,
			help='The discount value.'
		)
	parser.add_argument(
			'-s','--initial',
			nargs='?',
			type=int,
			default=0,
			help='The initial state.'
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

	# Loading stochastic policy to be simulated
	with open(args.policy,'r') as f:
		policy = [[float(e) for e in r] for r in csv.reader(f)]

	# Simulating multiple statistical runs across multiple threads
	pool = Pool(processes=args.threads)
	args = [
				{
					'mdp':		Mdp(T=mdp.T,R=mdp.R,m=mdp.m,n=mdp.n,verbose=args.verbose),
					'policy':	policy,
					'runs':		args.runs/args.threads,
					'episode':	args.length,
					'discount':	args.discount,
					'initial':	args.initial,
				} for i in range(args.threads)
			]
	rwds = [item for sublist in pool.map(worker,args) for item in sublist]


	print stats.mean(rwds),1.95*stats.stdev(rwds)/(len(rwds)**0.5)

		


if __name__ == "__main__":
	main()


