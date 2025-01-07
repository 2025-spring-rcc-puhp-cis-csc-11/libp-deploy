#!/usr/bin/env python3
import os.path

from domain.Deployer import Deployer


import argparse
import os


def main():
	
	parser = argparse.ArgumentParser(
		prog="libPuhfessorP Deploy Script, woot"
	)
	parser.add_argument(
		"--working-directory", "--working-dir",
		dest="working_directory",
		required=False,
		default=None,
		help="Specify working directory",
	)
	parser.add_argument(
		"--lib", "--library", "--lib-dir", "--library-directory",
		dest="library_directory",
		required=True,
		help="Specify the directory where the library resides"
	)
	parser.add_argument(
		"--build", "--build-dir", "--build-directory",
		dest="build_directory",
		required=True,
		help="Directory for temporary build files"
	)
	parser.add_argument(
		"--deploy", "--deploy-dir", "--deploy-directory",
		dest="deploy_directory",
		required=True,
		help="Directory to deploy to"
	)
	parser.add_argument(
		"--file-so", "--so",
		dest="shared_object_file_name",
		default="libPuhfessorP.asm.so",
		help="File name that the shared object will build"
	)
	parser.add_argument(
		"--info", "--info-file", "--info-file-name",
		dest="info_file_name",
		default="info.txt",
		help="Name of the info file to generate"
	)
	
	args = parser.parse_args()
	
	if args.working_directory is not None:
		os.chdir(args.working_directory)
	
	repo_dir = os.path.dirname(__file__)
	
	deployer = Deployer(
		library_directory=args.library_directory,
		build_directory=args.build_directory,
		deploy_repo_directory=repo_dir,
		deploy_directory=args.deploy_directory,
		shared_object_file_name=args.shared_object_file_name,
		info_file_name=args.info_file_name
	)
	deployer.run()


if __name__ == "__main__":
	main()


