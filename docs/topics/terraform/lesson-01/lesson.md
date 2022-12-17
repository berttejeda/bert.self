# Forward

Thank you for taking the time to start reading this educational material.

I hope this hands-on, interactive lesson can reduce the startup 
cost in your journey to learning [Terraform](newtab+https://www.terraform.io).

Here's what I will cover for Lab 1 of this Terraform tutorial series:

- What is Terraform?
- How to install Terraform on Windows, Linux, and MacOS
- The basics of Terraform Inputs (variables) and Outputs

Let's begin.

## What is Terraform?

Much of the following was taken from the book 
[Terraform In Action](https://www.manning.com/books/terraform-in-action#:~:text=about%20the%20book,configure%20other%20hands%2Don%20projects.) 
from Manning Publications, authored by Scott Winkler.

Now, to understand what Terraform is, let's first go over some terminology.

### Terminology

- **Infrastructure As Code** (**IaC**): The process of managing and provisioning infrastructure 
  through machine-readable definition files. We use IaC to automate infrastructure management processes that used to be done manually.
- **Provisioning**:  The act of deploying infrastructure, as opposed to configuration management (CM), 
  which deals mostly with application delivery and desired state management,
  particularly on virtual machines (VMs). <br />
  Infrastructure Provisioning and Configuration Management are inherently **different** problem domains.
- **Declarative**: Say what you want, not how to do it.
    - Example of declarative: Terraform, Ansible
    - Example of imperative: A bash script<br />
      Even Ansible can be imperative, depending on how you employ it.
- **Mutable Infrastructure**: Means you perform software updates on **existing** servers
- **Immutable Infrastructure**: Doesn't care about existing servers -- it treats 
  infrastructure as a **disposable** commodity. <br />
  The phrase [Pets vs Cattle](https://letmegooglethat.com/?q=pets+vs+cattle+in+devops) 
  is often used as an analogy

### Ok, so what's Terraform?

Pardon the repetition, but the concept needs to be hammered in ...

- Terraform is an infrastructure provisioning tool<br />
  It is **not** a Configuration Management (CM) tool
- Provisioning tools deploy and manage infrastructure, 
  whereas CM tools like Ansible, Puppet, SaltStack, and Chef deploy 
  software and apply configurations onto **existing** servers.
- The basic principle of Terraform is that it allows you to write human-readable 
  configuration code to define your IaC. With configuration code, you can deploy repeatable, 
  ephemeral, consistent environments to vendors on the public, private, and hybrid clouds.
- Some CM tools can also perform a degree of infrastructure provisioning, 
  but not as well as Terraform, because this isn't the task they were originally designed to do. 
  The same can be said the other way around.
-  The difference between CM and provisioning tools is a matter of philosophy
    - CM tools favor mutable infrastructure, whereas Terraform and other provisioning tools favor immutable infrastructure
- The difference between the two paradigms can be summarized as a reusable versus disposable mentality
- Terraform IaC is written in HashiCorp Configuration Language (HCL)
    - HCL is fully compatible with JSON. <br />
      That is, JSON can be used as completely valid input to a system expecting HCL.

TL;DR;

- Terraform is 
    - An infrastructure provisioning tool
    - Easy to use
    - Free and open source
    - Declarative
    - Cloud-agnostic
    - Expressive and extensible

Now that you have an idea as to how Terraform is used, 
let's get into its basic concepts and run through some exercises.

## Concepts & Exercises

Before we begin, let's first install Terraform.

### Installing Terraform

#### Windows

It's easiest to install terraform via [chocolatey](https://chocolatey.org/install).

Once you have chocolatey installed, simply run `choco install terraform`

#### Linux

You can download and extract the terraform binary directly from hashicorp like so:

<pre class='clickable-code'>
export TERRAFORM_VERSION=1.2.3
curl -kO https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/bin
</pre>

Make sure to adjust the _TERRAFORM_VERSION_ string above
to reflect the latest available from the [Hashicorp website](https://www.terraform.io/downloads).

#### Mac OSX

For Mac OSX, I recommend you install terraform using [homebrew](https://docs.brew.sh/Installation).

Simply run `brew install terraform`.

Let's move on to core concepts.

## Core concepts

### Order of Operations

- The major elements of Terraform are: 
    - Input variables
    - Resources
    - Data sources (A.K.A read-only resources)
    - Providers
    - Modules
    - Output variables
- To deploy a Terraform project, you must first organize such elements in configuration code (.tf files)

That said, the order of operations for deploying infrastructure via terraform is as follows:

1. Write configuration code (again, .tf files)
1. Initialize workspace with `terraform init`
1. Invoke `terraform plan`
1. Apply the configuration with `terraform apply`

???+ note ":information_source:"
    During the plan or apply phase, terraform concatenates all the .tf files in your workspace into a 
    single HCL-formatted file, and automatically determines the correct order in which to derive settings and deploy
    infrastructure
???+ note ":information_source:" 
    From the Terraform [documentation](https://www.terraform.io/cli/commands/plan): The `terraform plan` command creates 
    an execution plan with a preview of the changes that Terraform will make to your infrastructure.<br />
    The terraform apply command executes the actions proposed in a Terraform plan.

The most straightforward way to use terraform apply is to run it without any arguments at all, in which case it will automatically create a new execution plan (as if you had run terraform plan) and then prompt you to approve that plan, before taking the indicated actions.

Let's put into practice everything discussed so far with the first piece of our configuration code -- input variables

## Excercise 1 - Variables

As with any modern programming language, variables are basically input values that can change (hence their _variable_ nature),
depending on conditions or on information passed in to the program.

Like many other approaches to this concept, Terraform employs *type constraints*,
meaning as you declare your input variables, you must also specify their data type.
Refer to the Terraform [documentation](https://www.terraform.io/language/expressions/type-constraints) for more information.


Let's begin the exercise:

1. Create your workspace: `mkdir tf_workspace`
1. Change your working directory to your workspace: `cd tf_workspace`
1. Create the variables.tf file<br />
  <pre class='clickable-code'>
  echo -e ''' variable "my_map" {
    type = map(string)
    default = {
      "mykey" = "myvar"
    }
  }
  ''' | tee variables.tf
  </pre>

As noted before, this variables file defines our inputs. 

???+ note ":information_source:"
    You don't have to name the file _variables.tf_, but it is good practice to do so.

Now that we have our variables defined, let's create our outputs file.

## Exercise 2 - Outputs

As with Input variables, Terraform outputs are conceptually the same as with any modern programming language,
where for example you may have return values from various functions and output data from
the application as a whole. 

Outputs are meant to be picked up by other Terraform code or even other automation. 

These outputs are recorded in the Terraform [state](https://www.terraform.io/language/state).

Let's begin the exercise:

1. Create the output file<br />
  <pre class='clickable-code'>
  echo -e ''' output my_map_dot_notation {
    value = var.my_map.mykey
  }
  output my_map_key_notation {
    value = var.my_map["mykey"]
  }
  ''' | tee outputs.tf
  </pre>

  Now that your outputs are defined, let's proceed to the last exercise.

## Exercise 3 - Terraform Plan & Apply

As you might have guessed, we're not actually creating any infrastructure in this lesson.

We are merely acquainting you with Terraform inputs and outputs.

Let's begin the exercise:

1. Initialize the terraform workspace: `terraform init`<br />
   During this phase, Terraform will download any externally-sourced modules<br />
   and initialize any referenced providers. It will also fail early should any<br />
   problems arise during initialization, e.g. authentication errors, syntax errors, etc.<br />
   We aren't working with anything mentioned above, so the init will pass with flying colors.
1. Generate the execution plan: `terraform plan`<br />
   Because we're only creating outputs, your execution plan should be simple, and similar to:<br />
   <pre class='non-clickable-code'>
   Changes to Outputs:
    + my_map_dot_notation = "myvar"
    + my_map_key_notation = "myvar"
   </pre>
1. Apply the execution plan: `terraform apply`<br />
   Answer 'yes' when prompted<br />
   Again, terraform didn't actually create or destroy anything.<br />
   Thus, your output should be simple, and similar to:<br />
   <pre class='non-clickable-code'>
   Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

    Outputs:

    my_map_dot_notation = "myvar"
    my_map_key_notation = "myvar"
  </pre>

Now that you've completed exercise, this concludes the lab.