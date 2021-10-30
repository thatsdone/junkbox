package com.github.thatsdone.junkbox;
/**
 * Nd4jTest1
 * 
 * Description: A test tool for Nd4j behavior
 * Author: Masanori Itoh <masanori.itoh@gmail.com>
 */

import java.util.*;
import java.io.*;

import org.nd4j.linalg.api.ndarray.BaseNDArray;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.factory.Nd4j;
import java.util.Arrays;

public class Nd4jTest1
{
    public static void main(String[] args) throws Exception
    {
	INDArray m = Nd4j.zeros(3, 3);

	System.out.printf("m:\n%s\n", m);
	for (int i = 0; i < 3; i++) {
	    for (int j = 0; j < 3; j++) {
		double val =  (i + 1) * 100.0 + j;
		//System.out.printf("elm: %d %d %f\n", i, j, val);
		m.putScalar(i, j, val);
	    }
	}
	System.out.printf("m:\n%s\n", m);
	//old mtj
	//double val2[] = {1.234, 2.345, 3.456};
	//m.addRow(val2);
	
	m.putRow(m.rows() + 1, Nd4j.create(new double[] {1.234, 2.345, 3.456} ));
	//INDArray v = Nd4j.vstack(m, Nd4j.create(new double[] {1.234, 2.345, 3.456})); //, new int[]{3, 1}));
	//m.addRowVector(Nd4j.create(new double[] {1.234, 2.345, 3.456})); //, new int[]{3, 1}));
	//INDArray c = Nd4j.concat(0, m, Nd4j.create(new double[] {1.234, 2.345, 3.456}));
	System.out.printf("m:\n%s\n", m);
    }
}
