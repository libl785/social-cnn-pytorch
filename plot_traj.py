
import pickle
import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt


# test_results.pkl format: input, target and pred pair in a tuple: [(2m X T, 2m X T, 2m X T), (2m X T, 2m X T, 2m X T),...]


def plot_traj(args, traj_file):
	print('Number of examples in '+args.train_or_dev_or_test+' set is {}'.format(len(traj_file)))
	try:
		one_example = traj_file[args.example_num] # (2m X T, 2m X T)
	except:
		sys.exit('Execution stopped: '+args.train_or_dev_or_test+' set does not contain Example '+str(args.example_num)+'. Please choose another example.')


	m = int(one_example[0].shape[0]/2) # pedestrian number

	col_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	inp = one_example[0]; target = one_example[1]; pred = one_example[2] # 2m X T

	inp_x = inp[::2]*args.x_scaling_factor; inp_y = inp[1::2]*args.y_scaling_factor
	pred_x = pred[::2]*args.x_scaling_factor; pred_y = pred[1::2]*args.y_scaling_factor
	targ_x = target[::2]*args.x_scaling_factor; targ_y = target[1::2]*args.y_scaling_factor


	for i in range(m):
		col = col_list[i%len(col_list)]
		ax.plot(inp_x[i,:], inp_y[i,:], col+':', label='input '+str(i))
		ax.plot(pred_x[i,:], pred_y[i,:], col+'o', label='pred '+str(i))
		print('pred:')
		print(pred_x[i,:])
		print(pred_y[i,:])
		ax.plot(targ_x[i,:], targ_y[i,:], col+'--', label='target '+str(i))
		print('target:')
		print(targ_x[i,:])
		print(targ_y[i,:])
		print(' ')

	ax.grid(True)
	ax.legend()
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	plt.show()



def main():
	parser = argparse.ArgumentParser(description='PyTorch CNNTrajNet')
	parser.add_argument('--example_num', type=int, default=0, help='the example number to be plotted')
	parser.add_argument('--x_scaling_factor', type=float, default=0.36883, help='true x = current_x * x_scaling_factor')
	parser.add_argument('--y_scaling_factor', type=float, default=0.459005, help='true y = current_y * y_scaling_factor')
	parser.add_argument('--train_or_dev_or_test', type=str, default='test', help='choose among train, dev, and test')
	plot_traj_args = parser.parse_args()

	save_directory = 'save/'
	with open(os.path.join(save_directory, 'train_config.pkl'), 'rb') as f:
	    saved_args = pickle.load(f)

	if plot_traj_args.train_or_dev_or_test == 'test':
		print('For test set: {},'.format(saved_args.testset))
		traj_log_filename = 'log/test_results_wi_testset_'+str(saved_args.testset)+'.pkl'
	elif plot_traj_args.train_or_dev_or_test == 'train':
		traj_log_filename = 'save/final_train_results_wi_testset_'+str(saved_args.testset)+'.pkl'
	elif plot_traj_args.train_or_dev_or_test == 'dev':
		traj_log_filename = 'save/final_dev_results_wi_testset_'+str(saved_args.testset)+'.pkl'
	else:
		sys.exit('Please write down in string either train, dev, or test')

	traj_file = pickle.load(open(traj_log_filename, "rb" ) )


	plot_traj(plot_traj_args, traj_file)



if __name__ == '__main__':
	main()

