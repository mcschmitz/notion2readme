# Creating Clusters

## EKS

Deploying Kubenetes cluster and deploying Kubeflow

- Please note the minimum requirements when deploying cluster, this is what we have used. The config files can be found in the kubeflow repo under the cluster dir.

- When preparing the env, use the AWS setup without authentication

- When configuring Kubeflow, use IAM for Service Account option

[Install Kubeflow](https://www.kubeflow.org/docs/aws/deploy/install-kubeflow/)

## Kubeflow

Please install:

- kubectl

- aws-iam-authenticator

To get access to Kubeflow dashboard. Please run the following command:

kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80

``` yaml
username: admin@kubeflow.org
password: 12341234
namespace: ebot7
```

## Granting Access

Cluster User

1.    To see the configuration of your AWS CLI user or role, run the following command:



The output returns the Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) user or role. See the following example:

``` javascript
{
    "UserId": "XXXXXXXXXXXXXXXXXXXXX",
    "Account": "XXXXXXXXXXXX",
    "Arn": "arn:aws:iam::XXXXXXXXXXXX:user/testuser"

```

2.    Confirm that the ARN matches the cluster creator.

3.    Update or generate the 

As the IAM user, run the following command:



Note:

Cluster Creator

1. Run the following command 

``` javascript
apiVersion: v1
data:
  mapRoles: |
    - rolearn: arn:aws:iam::555555555555:role/devel-worker-nodes-NodeInstanceRole-74RF4UBDUKL6
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes
  mapUsers: |
    - userarn: arn:aws:iam::111122223333:user/ops-user
      username: ops-user
      groups:
        - system:masters
  mapAccounts: |
    - "111122223333"
```

Mind the mapUsers where you're adding ops-user together with mapAccounts label which maps the AWS user account with a username on Kubernetes cluster

2. Then run 

# KF Components

## Handling inputs and outputs

KF components have a few rules that need to be followed, we will need to follow these rules to ensure that pipelines work.

- To output any piece of data, the component must write the output data to some location and inform the system: This allows the output to be passed between steps
	- The program should accept the paths for the output data as a command-line arg
	
	- The program receives the local path of the output file and the data should be written to that path. The output should be treated as a file path. Please ensure to create the parent directories, this code is provided in 

- Consuming data:
	- Small data: can be passed as command-line arg
	- Large data or Binary data: Passed as file



Next, in order for kubeflow to know what the parameters for the component are, we need to create a component definition file. This is a simple file which defines the inputs and outputs, and it also specifies the containers location in ECR.

``` yaml
name: S3 List Object TO Limit
description: List only param number of S3 objects
inputs:
- {name: Input 1, type: GCSPath, description: 'S3 list data'}
- {name: Parameter 1, type: Integer, default: '100', description: 'Number of lines to output'} # The default values must be specified as YAML strings.
outputs:
- {name: Output 1, description: 'Output 1 data'}
  
implementation:
  container:
    image: 690379044785.dkr.ecr.eu-central-1.amazonaws.com/list_file_lim:latest
    command: [
      python3, /kfp/component/src/main.py,
      --input1-path, {inputPath: Input 1},
      --param1, {inputValue: Parameter 1},
      --output1-path, {outputPath: Output 1},
    ]
```

This is an example of the component definition file, this can be found in the samples directory. In this example, we have specified 2 types of inputs, a file and a command-line arg, and for the output, a file. The implementation specifies the image uri and the command required to run the application in the docker image, 

Also, please note how the 

## Docker Setup

To simplify the development of our components docker image, a python script is provided. This file resides in the root of the components directory. The script can be used to either create an new image or update an existing image. It builds the docker image and then automatically uploads the image to ECR. To images are uploaded on every instance, once tagged with the timestamp and another with the tag 

The 

This is the command to run the script:

python update_image.py --file-path ./samples/[docker app dir name]

Before running this command, please ensure to login to ecr via console using the following command:

aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 

## File structure

This is the directory structure, we have followed the recommendations by kf and also adapted it to our general Microservice development standards to make it easier for us to develop. 

``` json
├── component.yaml
├── Dockerfile
├── src
│   ├── config
│   │   ├── default.yaml
│   │   └── __init__.py
│   ├── ls_operations.py
│   ├── main.py
│   └── requirements.txt
└── ssh
    ├── config
    ├── id_rsa_macgyver
    └── id_rsa_ml_utils
```

## KF Pipeline

Pipeline can be executed directly from you local machine. But due to AWS complications, this process is not straight forward. There for the 

This application basically extracts the required cookies from the application to allow the client to communicate with Kubeflow. 

A sample pipeline can be found in the samples folder, this pipeline calls the components in the components sample directory. This is a very simple pipeline, the first component list all the buckets in our S3 bucket, and the second component filters our 

- Accessing S3: Please note that we need to apply 

- File inputs and command-line arg inputs

- Passing data between components: As it can be seen, the file generated by 

- Passing default arguments to the application. As it can be seen, 

- Finally, the application compiles the pipeline and exports a compressed file. This file is then uploaded to the pipeline which is then accessible via the dashboard. But it is also possible to execute the pipeline directly from this script, just need to use the correct client method for this which can be found in the documentation.
	The pipeline can then be found in the pipeline page of KF dashboard and you can run a simple experiment to test the pipeline or you can directly create a run.

``` python
import kfp
from kfp import components
from kfp import dsl
from kfp.aws import use_aws_secret
from kfp_client import client

s3_component= components.load_component_from_file(
    "../components/s3_component/component.yaml"
)
ls_component=components.load_component_from_file("../components/list_file_lim/component.yaml")


@dsl.pipeline(name="List S3 Objects", description="List a limited number of S3 objects")
def my_pipeline(
    parameter_1="2",
):
    s3_listing = s3_component().apply(
        use_aws_secret()
    )
    lim_listing = ls_component(input_1=s3_listing.output, parameter_1=parameter_1)


package_name = "s3_lim_bucket_listing.zip"
kfp.compiler.Compiler().compile(my_pipeline, package_name)
client.upload_pipeline(package_name, pipeline_name="s3_lim_bucket_listing")
```

The # notion2readme
