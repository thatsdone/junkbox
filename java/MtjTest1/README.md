# Description

This test program is intended for checking interface and behavior of
an old and lost implementation of Java Matrix Toolkit.

Here, the main target is 'no.uib.cipr.matrix.sparse.FlexCompRowMatrix' which is used in:
https://github.com/numenta/htm.java/blob/master/src/main/java/org/numenta/nupic/algorithms/SDRClassifier.java

Especially, 'addRow()' at:

https://github.com/numenta/htm.java/blob/master/src/main/java/org/numenta/nupic/algorithms/SDRClassifier.java#L304


```java
    293                 //------------------------------------------------------------------------
    294                 //Learning:
    295                 if(learn && classification.get("bucketIdx") != null) {
    296                         // Get classification info
    297                         int bucketIdx = (int)classification.get("bucketIdx");
    298                         Object actValue = classification.get("actValue");
    299
    300                         // Update maxBucketIndex and augment weight matrix with zero padding
    301                         if(bucketIdx > maxBucketIdx) {
    302                                 for(int nSteps : steps.toArray()) {
    303                                         for(int i = maxBucketIdx; i < bucketIdx; i++) {
    304                                                 weightMatrix.get(nSteps).addRow(new double[maxInputIdx + 1]);
    305                                         }
    306                                 }
    307                                 maxBucketIdx = bucketIdx;
    308                         }
```


Now, addRow() cannot be found in:

https://javadoc.io/doc/com.googlecode.matrix-toolkits-java/mtj/latest/no/uib/cipr/matrix/sparse/FlexCompRowMatrix.html

Actually, 'htm.java' mainteners resolve this problem by holding a copy of the old/lost Matrix Tool Kit for Java
jar file in the repository. No source, AFAIK.

This is an insane situation, and the code should be rewritten to use an appropriate interface.

Here, the problem is that documentation of the old library was also lost, and it's not clear the original method interface.

Thus, I wrote this small program to see the original interface and behavior.

As a result, addRow() turned out to be a method adding a row to a matrix vertically. This is similar
to vstack() of python numpy ndarray, IMHO.


# HOW TO BUILD

1. Prepare JDK and Maven available environment.
2. Clone this repository and go to the directory.
3. Execute `getdep.sh` to download 'algorithmfoundry-shade-culled-1.3.jar' from https://github.com/numenta/htm.java into 'lib'.
4. Execute `$ mvn clean package`
5. Execute `run.sh`

# References
* https://javadoc.io/doc/com.googlecode.matrix-toolkits-java/mtj/latest/no/uib/cipr/matrix/sparse/FlexCompRowMatrix.html
* https://github.com/fommil/matrix-toolkits-java
* https://javadoc.io/doc/ai.djl/api/latest/ai/djl/ndarray/NDArray.html
* https://deeplearning4j.org/api/latest/org/nd4j/linalg/factory/Nd4j.html
* https://github.com/numenta/htm.java-examples/raw/master/libs/algorithmfoundry/algorithmfoundry-shade-culled/1.3/algorithmfoundry-shade-culled-1.3.jar
