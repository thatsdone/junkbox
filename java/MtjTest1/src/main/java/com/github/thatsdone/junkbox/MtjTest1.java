package com.github.thatsdone.junkbox;
/**
 * MtjTest1
 * 
 * Description: A test tool for
 * Author: Masanori Itoh <masanori.itoh@gmail.com>
 */

import java.util.*;
import java.io.*;

import no.uib.cipr.matrix.sparse.FlexCompRowMatrix;

public class MtjTest1
{
    public static void main(String[] args) throws Exception
    {
	FlexCompRowMatrix m = new FlexCompRowMatrix(3, 3);
	System.out.printf("m = %s\n", m);
	for (int i = 0; i < 3; i++) {
	    for (int j = 0; j < 3; j++) {
		double val =  (i + 1) * 100.0 + j;
		System.out.printf("elm: %d %d %f\n", i, j, val);
		m.set(i, j, i * 100.0 + j);
	    }
	}
	System.out.printf("m = %s\n", m);
	for (int i = 0; i < 3; i++) {
	    for (int j = 0; j < 3; j++) {
		System.out.printf("val: %d %d %f\n", i, j, m.get(i, j));
	    }
	}
	double val2[] = {1.234, 2.345, 3.456};
	//algorithmfoundry-shade-culled-1.3.jar
	m.addRow(val2);
	//group com.googlecode.matrix-toolkits-java

	System.out.printf("m = %s %d %d\n", m, m.numRows(), m.numColumns());
	for (int i = 0; i < m.numRows(); i++) {
	    for (int j = 0; j < m.numColumns(); j++) {
		System.out.printf("val: %d %d %f\n", i, j, m.get(i, j));
	    }
	}
	
    }
}
