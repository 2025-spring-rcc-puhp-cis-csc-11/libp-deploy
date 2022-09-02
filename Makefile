define say
	$(info [libP Deploy] $1)
endef


#
SHELL := /bin/bash


#
REPO_PATH := $(abspath .)
$(call say,REPO_PATH: $(REPO_PATH))


#
LIBP_DIR := ../libp
LIBP_DIR_ABS := $(abspath $(LIBP_DIR))
$(call say,Using hacky hard-coded path to libP: $(LIBP_DIR_ABS))


DEPLOY_DIR := .
DEPLOY_DIR_ABS := $(abspath $(DEPLOY_DIR))
$(call say,Using deploy dir: $(DEPLOY_DIR_ABS))


# Build dir will be relative to the libP repo
BUILD_DIR_NAME := _build
BUILD_DIR_FOR_LIBP := ./$(BUILD_DIR_NAME)
BUILD_DIR_FOR_LOCAL := $(LIBP_DIR)/$(BUILD_DIR_NAME)
$(call say,Using BUILD_DIR_FOR_LIBP: $(BUILD_DIR_FOR_LIBP))
$(call say,Using BUILD_DIR_FOR_LOCAL: $(BUILD_DIR_FOR_LOCAL))


#
default: help
.PHONY: default


#
help:
	@echo "***** Lib PuhfessorP - Deploy *****"
	@echo
	@echo "make build            ==> Build libP"
	@echo
.PHONY: help


#
build:	| $(BUILD_DIR_FOR_LOCAL) $(DEPLOY_DIR)
	pipenv run python ./main.py \
		--lib '$(LIBP_DIR_ABS)' \
		--build '$(BUILD_DIR_FOR_LIBP)' `# Give a libp-relative path here` \
		--deploy '$(DEPLOY_DIR_ABS)' \
	&& rm -rfv $(BUILD_DIR_FOR_LOCAL)


#
$(BUILD_DIR_FOR_LOCAL):
	-mkdir --parents $(BUILD_DIR_FOR_LOCAL)


#
$(DEPLOY_DIR):
	-mkdir --parents $(DEPLOY_DIR)



