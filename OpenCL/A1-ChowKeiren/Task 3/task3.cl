__kernel void task3(__global int* array, const int num) {
   
   int i = get_global_id(0);
   array[i] = 3 + (num * i);
}

