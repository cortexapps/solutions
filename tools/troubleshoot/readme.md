## Troubleshooting Cortex 

For instances of Cortex running on Kubernetes clusters, you can use this tool to not only collect information but also provide a quick diagnostics that may help find the issue.

### About Troubleshoot

For this we are using an open source project from Replicated called Troubleshoot. This project provides the ability to specify in a YAML file what to collect and analyze. The results from the analyzers are displayed to the user as well as included in the resulting tar ball that contains everything that was collected.

#### How Are We Using It

In order to make this as simple as possible we have create scripts that automate this entire process. To better understand the process, let's outline all the steps (please note that these have to be peformed on a machine with `kubectl` access to the cluster hosting Cortex):

- Download the `support-bundle` binary
- - You can download it as a `kubectl` plugin using `krew`
- - You can download the binary and run it by itself

- Download/find/create a Support Bundle spec that outlines everyhing to collect & analyze based on what is available 

- Run the command 
- - 'kubectl support-bundle spec.yaml
- - or
- - 'support-bundle spec.yaml`
