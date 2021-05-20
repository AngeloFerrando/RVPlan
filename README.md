# RVPlan

## How to install

- Download and Install DEJAVU (https://github.com/havelund/dejavu) and be sure it works.

## Property synthesis

To synthesise a Past LTL property (i.e. to create an instantiated monitor):
```bash
-$ python3 translator.py <domain_file.pddl> <plan_file>
```
To test, try to synthesise the Past LTL property for the sample domain and plan files.
```bash
-$ python3 translator.py domain.pddl plan.txt
```
This will generate the prop.qtl file inside the out folder. This is the Past LTL corresponding to the preconditions for the actions used in the given plan.

To synthesise a Past FO-LTL property (i.e. to create a parameterised monitor):
```bash
-$ python3 translator.py <domain_file.pddl>
```
To test, try to synthesise the Past FO-LTL property for the sample domain file (the plan is not necessary, since only domain actions are needed).
```bash
-$ python3 translator.py domain.pddl
```
This will generate the prop.qtl file inside the out folder. This is the Past FO-LTL corresponding to the preconditions for the domain actions.

## Monitor synthesis

To compile the property obtained at the previous step, simply use DEJAVU (<dejavu_home> is the folder where you installed DEJAVU).
```bash
java -cp <dejavu_home>/out/artifacts/dejavu_jar/dejavu.jar dejavu.Verify ./out/prop.qtl | grep -v "Elapsed total"
```
This will generate the TraceMonitor.scala file in your folder. This represents the monitor corresponding to the prop.qtl property.

## Runtime Verification

In the previous step, we obtained the monitor, now we can use it to verify a trace (offline for now).

First, we compile the scala monitor we obtained at previous step.
```bash
-$  scalac -cp .:<dejavu_home>/out/artifacts/dejavu_jar/dejavu.jar TraceMonitor.scala 2>&1 | grep -v "warning"
```
This will generate the .class files. Next, we can run the compiled monitor passing a CSV file containing an execution trace.
```bash
-$ scala -J-Xmx32g -cp .:<dejavu_home>/out/artifacts/dejavu_jar/dejavu.jar TraceMonitor <trace_to_analyse> 20  2>&1  | grep -v "Resizing" | grep -v "load BDD package" | grep -v "Garbage collection"
```
To test, try to verify the trace stored in trace.csv file.
```bash
-$ scala -J-Xmx32g -cp .:<dejavu_home>/out/artifacts/dejavu_jar/dejavu.jar TraceMonitor ./trace.csv 20  2>&1  | grep -v "Resizing" | grep -v "load BDD package" | grep -v "Garbage collection"
```
