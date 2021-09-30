

# Stuff handled by pipenv
from git import Repo


#
from datetime import datetime
import os
import re
import shutil
import subprocess


#
class Deployer:
	
	__EXTRA_COPY_FILE_NAMES = [
		"FUNCTIONS.md"
	]
	
	def __init__(self, library_directory, deploy_directory, shared_object_file_name, info_file_name):
		
		self.__library_directory = library_directory
		self.__deploy_directory = deploy_directory
		self.__shared_object_file_name = shared_object_file_name
		self.__info_file_name = info_file_name
		
		self.__deployed_shared_object_file_name: str = None
		self._compute_deployed_shared_object_file_name()
	
	def _compute_deployed_shared_object_file_name(self):
		
		tag = self._get_library_latest_tag()
		
		file_name = re.sub("\\.so$", ".{}.so".format(tag), self.__shared_object_file_name)
		file_name = re.sub("\\.asm", "", file_name)
		
		self.__deployed_shared_object_file_name = file_name
	
	def run(self):
	
		self._demand_dirs()
		self._pull_library()
		self._build_library()
		self._copy_elements()
		self._generate_info_file()
		self._clean_library()
		self._push_deploy()
		print("Deploy seems to have been successful")
	
	def _get_library_repo(self):
		
		repo = Repo(self.__library_directory)
		
		return repo
	
	def _get_library_latest_tag(self):
		
		tags = self._get_sorted_tags()
		latest_tag = tags[-1]
		
		return latest_tag
	
	def _get_sorted_tags(self):
		
		repo = self._get_library_repo()
		
		tags_str = repo.git.tag(sort='creatordate')
		tags = tags_str.split("\n")
		
		def ensure_three_digits(v: str):
			v = ("0" * (3 - len(v))) + v
			return v
		
		def sort_lambda(semver: list):
			s = ensure_three_digits(semver[0]) + "-" + ensure_three_digits(semver[1]) + "-" + ensure_three_digits(semver[2])
			return s
		
		tags_semver = []
		for tag in tags:
			match = re.match("^v(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9]+)$", tag)
			assert match, "Unable to parse semver for tag: {}".format(tag)
			tag_semver = [match.group("major"), match.group("minor"), match.group("patch")]
			tags_semver.append(tag_semver)
		
		tags_semver_sorted = sorted(tags_semver, key=sort_lambda)
		
		tags_sorted = []
		for tag_semver in tags_semver_sorted:
			tags_sorted.append("v" + ".".join(tag_semver))
		
		return tags_sorted
	
	def _get_deploy_repo(self):
		
		repo = Repo(self.__deploy_directory)
		
		return repo
	
	def _demand_dirs(self):
		
		assert os.path.isdir(self.__library_directory), "Library directory must be a directory"
		assert os.path.isdir(self.__deploy_directory), "Deploy directory must be a directory"
		
		assert self.__shared_object_file_name, "Shared object file name must be set"
		assert self.__info_file_name, "Shared object file name must be set"
	
	def _pull_library(self):
		
		repo = self._get_library_repo()
		repo.heads.master.checkout()
		repo.remotes.origin.pull()
	
	def _build_library(self):
		
		stdout, stderr = self._execute_command(
			args=[
				"make", "build"
			],
			env={
				"BUILD_DIR": self.__library_directory
			},
			working_directory=self.__library_directory
		)
	
	def _clean_library(self):
		
		stdout, stderr = self._execute_command(
			args=[
				"make", "clean"
			],
			env={
				"BUILD_DIR": self.__library_directory
			},
			working_directory=self.__library_directory
		)
	
	def _copy_elements(self):
		
		# Copy the shared object
		library_source = os.path.join(
			self.__library_directory,
			self.__shared_object_file_name
		)
		library_dest = os.path.join(
			self.__deploy_directory,
			self.__deployed_shared_object_file_name
		)
		shutil.copy(library_source, library_dest)
		
		# Copy the extra files
		for file_name in self.__EXTRA_COPY_FILE_NAMES:
			functions_source = os.path.join(
				self.__library_directory,
				file_name
			)
			functions_dest = os.path.join(
				self.__deploy_directory,
				file_name
			)
			shutil.copy(functions_source, functions_dest)
	
	def _generate_info_file(self):
		
		s = ""
		
		# Repo tag
		tag = self._get_library_latest_tag()
		s += "Generated from repository tag: {}\n".format(tag)
		
		# Operating system
		with open("/etc/os-release", "rt") as f:
			os_release_file = f.read()
			os_release = re.search("VERSION=\\\"(?P<os_name>[^\\\"]+)\\\"", os_release_file)
			os_release = os_release.group("os_name")
		s += "Built for OS: {}\n".format(os_release)
		
		# Datetime
		now = datetime.now()
		s += "Built on: {}\n".format(now.strftime("%a %B %d, %Y %H:%M%p and %Ss"))
		
		# Shared object file name
		s += "Shared object file name: {}\n\n".format(self.__deployed_shared_object_file_name)
		
		# Write the file
		info_file_path = os.path.join(
			self.__deploy_directory,
			self.__info_file_name
		)
		with open(info_file_path, "wt") as f:
			f.write(s)
	
	def _push_deploy(self):
		
		repo = self._get_deploy_repo()
		
		repo.git.add(self.__deployed_shared_object_file_name)
		repo.git.add(self.__info_file_name)
		
		for file_name in self.__EXTRA_COPY_FILE_NAMES:
			repo.git.add(file_name)
		
		repo.git.commit(m="Commit new version of {}".format(self.__deployed_shared_object_file_name))
		repo.git.push()
		
	def _execute_command(self, args, env=None, working_directory=None):
		
		if env is not None:
			env = { **os.environ, **env }
		
		print("\n\n***** Executing:", args)
		
		process = subprocess.Popen(
			args=args,
			env=env,
			#stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			cwd=working_directory,
		)
		
		stdout, stderr = process.communicate()
		
		stdout = self._decode_execution_output(stdout)
		stderr = self._decode_execution_output(stderr)
		
		exit_code = process.returncode
		
		if stdout:
			print("STDOUT:", stdout)
		if stderr:
			print("STDERR:", stderr)
		
		assert exit_code == 0, "Unexpected exit code {} after execution".format(exit_code)
		
		print("\n\n***** Execution success")
		
		return stdout, stderr
	
	def _decode_execution_output(self, output):
		
		if output:
			output = output.decode()
		else:
			output = ""
		
		return output




