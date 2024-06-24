#define CL_USE_DEPRECATED_OPENCL_2_0_APIS	// using OpenCL 1.2, some functions deprecated in OpenCL 2.0
#define __CL_ENABLE_EXCEPTIONS				// enable OpenCL exemptions

// C++ standard library and STL headers
#include <iostream>
#include <vector>
#include <fstream>
#include <iomanip>

// OpenCL header, depending on OS
#ifdef __APPLE__
#include <OpenCL/cl.hpp>
#else
#include <CL/cl.hpp>
#endif

#include "common.h"

void printArray(int[], int);

//fixed size for array1 and array2 and output
const int ARRAY_SIZE = 8;
const int ARRAY_SIZE2 = 16;
const int OUTPUT_SIZE = 32;


int main(void)
{
	//declaring a number of data structures and variables
	cl::Platform platform;			// device's platform
	cl::Device device;				// device used
	cl::Context context;			// context for the device
	cl::Program program;			// OpenCL program object
	cl::Kernel kernel;				// a single kernel object
	cl::CommandQueue queue;			// commandqueue for a context and device

	//Create and initialize the arrays
	cl_int vec1[ARRAY_SIZE];
	cl_int vec2[ARRAY_SIZE2];
	std::vector<cl_int> output(OUTPUT_SIZE);
	cl::Buffer bufVec1, bufVec2, bufResult;

	// Seed the random number generator
	srand(time(NULL));

	for (int i = 0; i < ARRAY_SIZE; i++) {
		vec1[i] = rand() % 11 + 10; // Random values between 10 and 20
	}

	for (int i = 0; i < ARRAY_SIZE2; i++) {
		if (i < ARRAY_SIZE2 / 2) {
			vec2[i] = i; // Values from 0 to 7
		}
		else {
			vec2[i] = -8 + (i - ARRAY_SIZE2 / 2); // Values from -8 to -1
		}
	}

	//printing array1 and array2
	std::cout << "Vec 1: ";
	printArray(vec1, ARRAY_SIZE);
	std::cout << "Vec 2: ";
	printArray(vec2, ARRAY_SIZE2);
	std::cout << std::endl;

	try {
		// select an OpenCL device
		if (!select_one_device(&platform, &device))
		{
			// if no device selected
			quit_program("Device not selected.");
		}

		// create a context from device
		context = cl::Context(device);

		// build the program
		if (!build_program(&program, &context, "task1.cl"))
		{
			// if OpenCL program build error
			quit_program("OpenCL program build error.");
		}

		// create a kernel
		kernel = cl::Kernel(program, "task1");

		// create command queue
		queue = cl::CommandQueue(context, device);

		// create buffers
		bufVec1 = cl::Buffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(cl_int) * ARRAY_SIZE, &vec1[0]);
		bufVec2 = cl::Buffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(cl_int) *  ARRAY_SIZE2,&vec2[0]);
		bufResult = cl::Buffer(context, CL_MEM_WRITE_ONLY, sizeof(cl_int) * OUTPUT_SIZE);

		// set kernel arguments
		kernel.setArg(0, bufVec1);
		kernel.setArg(1, bufVec2);
		kernel.setArg(2, bufResult);

		//enqueue command to write from host to device memory
		queue.enqueueWriteBuffer(bufResult, CL_TRUE, 0, sizeof(cl_int) * OUTPUT_SIZE, &output[0]);

		//enqueue kernel for execution
		queue.enqueueTask(kernel);

		std::cout << "Kernel enqueued." << std::endl;
		std::cout << "--------------------" << std::endl;

		// enqueue command to read from device to host memory
		queue.enqueueReadBuffer(bufResult, CL_TRUE, 0, sizeof(cl_int) * OUTPUT_SIZE, &output[0]);

		// check the results
		// Display contents of host-side array
		for (int i = 0; i < 32; i++) {
			std::cout << std::setw(6) << output[i];

			// Check if we have printed 10 values already
			if ((i + 1) % 8 == 0) {
				std::cout << std::endl;
			}
		}

		// Add an extra newline after the final line, if needed
		if (ARRAY_SIZE2 % 8 != 0) {
			std::cout << std::endl;
		}
	}
	// catch any OpenCL function errors
	catch (cl::Error e) {
		// call function to handle errors
		handle_error(e);
	}

#ifdef _WIN32
	// wait for a keypress on Windows OS before exiting
	std::cout << "\npress a key to quit...";
	std::cin.ignore();
#endif

	return 0;
}

void printArray(int array[], int size) {
	for (unsigned int i = 0; i < size; i++) {
		std::cout << array[i] << " ";
	}
	std::cout << std::endl;
}
