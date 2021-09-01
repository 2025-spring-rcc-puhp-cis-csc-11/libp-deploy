#!/usr/bin/env python3


from Deployer import Deployer

import argparse


def main():
	
	parser = argparse.ArgumentParser(
		prog="libPuhfessorP Deploy Script, woot"
	)
	parser.add_argument(
		"--lib", "--lib-dir", "--library-directory",
		dest="library_directory",
		required=True,
		help="Specify the directory where the library resides"
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
	
	deployer = Deployer(
		library_directory=args.library_directory,
		deploy_directory=args.deploy_directory,
		shared_object_file_name=args.shared_object_file_name,
		info_file_name=args.info_file_name
	)
	deployer.run()


if __name__ == "__main__":
	main()


