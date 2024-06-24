__kernel void task1(__global int *input1,
                            __global int *input2,
                            __global int *output) {
    
    // Local memory to store input1 and input2
    __local int8 v1;
    __local int8 v2;
    __local int8 v;

    int index = get_global_id(0);


    // Copy vA & vB to int8 vector v
    int4 vA = vload4(index, input1);
    int4 vB = vload4(index, input1+4);
    v = (int8)(vA.s0123, vB.s0123);
	
	// Copy localInput2 to int8 vectors v1 and v2
	v1 = vload8(index, input2);
    v2 = vload8(index, input2 + 8);

    // Create results vector in private memory
    __private int8 results;

   // Check if any element in v is greater than 16
    if (any(v > 16)) {
     
            // For elements greater than 16, copy from v1
            results = select(v2, v1, v > 16);
            
    } else {
        // Fill the first 4 elements of results with v1
        results.s0123 = v1.s0123;

        // Fill the next 4 elements of results with v2
        results.s4567 = v2.s0123;
    }


  // Stores the contents of v, v1, v2 and results in the output array
    vstore8(v, index , output);
    vstore8(v1, index, output + 8);
    vstore8(v2, index, output + 16);
    vstore8(results, index, output + 24);

}