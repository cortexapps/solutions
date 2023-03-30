## Instructions for Troubleshooting Cortex On Premise

If you have issues with your Cortex On Premise instance, including a Support Bundle when you initially open a ticket will greatly decrease the time to resolution.

This document covers how you can generate one.

## Download & Install The Troubleshoot Framework

To help us collect all the information we need, we are leveraging the [Troubleshoot](https://troubleshoot.sh/) open source project. To create a support bundle we'll need to download and install the binary along with a yaml spec that includes what to collect.

The binary can be run in two different ways:

1. Running it as a Kubectl plugin
2. Running it as a stand alone binary

### Running it as a Kubectl plugins

To run it as a kubectl plugin, you can install using `krew` which is basically similar to `brew` for Mac OSs. Instructions on how to install `krew` can be found here: https://krew.sigs.k8s.io/docs/user-guide/setup/install/

To install the plugin run this command:

`kubectl krew install support-bundle`

### Running it as a stand alone binary

The binaries are included in the Assets section for each [release](https://github.com/replicatedhq/troubleshoot/releases/tag/v0.57.1) from this project. From there, download the right binary for your Operating System and CPU architecture. For example, to run this on an M1 Mac, we would download the `support-bundle_darwin_arm64.tar.gz` file (https://github.com/replicatedhq/troubleshoot/releases/download/v0.57.1/support-bundle_darwin_arm64.tar.gz)

It is strongly recommended that you download the binary to a path already in your $PATH. Otherwise, make sure to add the downloaded binary path to your $PATH. This will allow you to run the command from any directory.

## Download the spec

You can locate the spec in this same repository in the [/specs folder](./specs/spec.yaml).

## Generating the Bundle

To generate the Support Bundle, run the following command:

`kubectl support-bundle spec.yaml`

or

`support-bundle spec.yaml`

The output will be one line stating `Collecting support bundle` and then output the path of the Support Bundle.

**Important** the command will try to collect information from the namespace that is the default in the current context. If you would like to collect from a different namespace, edit the spec.yaml file and uncomment the `namespace` field and provide your namespace.



Please attach the output file to your ticket.
