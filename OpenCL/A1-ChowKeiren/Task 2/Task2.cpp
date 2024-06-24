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

int main(void) 
{
	//declaring a number of data structures and variables
	cl::Platform platform;			// device's platform
	cl::Device device;				// device used
	cl::Context context;			// context for the device
	cl::Program program;			// OpenCL program object
	cl::Kernel kernel;				// a single kernel object
	cl::CommandQueue queue;			// commandqueue for a context and device

	// declare vectors
	std::vector<unsigned char> alphabets(52);
	std::vector<unsigned char> result_char(52);
	std::vector<unsigned int> integers(1024);
	std::vector<unsigned int> result_int(1024);

	// declare data and memory objects
	cl::Buffer alphabetsBuffer;
	cl::Buffer writeBuffer;
	cl::Buffer readWriteBuffer;

	// initialize alphabets vector
	for (int i = 0; i < 26; i++) {
		alphabets[i] = 'z' - i;
		alphabets[i + 26] = 'Z' - i;
	}

	 //initialize integers vector
	for (int i = 0; i < 1024; i++) {
		integers[i] = i;
	}

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
		if(!build_program(&program, &context, "task2.cl")) 
		{
			// if OpenCL program build error
			quit_program("OpenCL program build error.");
		}

		// create a kernel
		kernel = cl::Kernel(program, "task2");

		// create command queue
		queue = cl::CommandQueue(context, device);

		//// create buffers
		
		alphabetsBuffer = cl::Buffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
			sizeof(unsigned char) * alphabets.size(), alphabets.data());

		writeBuffer = cl::Buffer(context, CL_MEM_WRITE_ONLY, sizeof(unsigned char) * 52);

		readWriteBuffer = cl::Buffer (context, CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR,
			sizeof(unsigned int) * integers.size(), integers.data());


		

		// enqueue a command to copy the content from the first buffer to the second buffer
		queue.enqueueCopyBuffer(alphabetsBuffer, writeBuffer, 0, 0, sizeof(unsigned char) * alphabets.size());

		
		// enqueue a command to write the content from the vector of 1024 integers into the third buffer
		queue.enqueueWriteBuffer(readWriteBuffer, CL_TRUE, 0, sizeof(unsigned int) * integers.size(), integers.data());

		// set kernel arguments
		float arg1 = 12.45;
		kernel.setArg(0, arg1);
		kernel.setArg(1, writeBuffer);
		kernel.setArg(2, readWriteBuffer);

		// enqueue kernel for execution
		queue.enqueueTask(kernel);

		std::cout << "Kernel enqueued." << std::endl;
		std::cout << "--------------------" << std::endl;

		// enqueue command to read from device to host memory
		queue.enqueueReadBuffer(writeBuffer, CL_TRUE, 0, sizeof(unsigned char) * 52, result_char.data());
		// display the results on screen
		std::cout << "\nContents of character result: " << std::endl;
		for (int i = 0; i < 52; i++)
		{
				std::cout << result_char[i] << " ";
				// Check if we have printed 10 values already
				if ((i + 1) % 10 == 0) {
					std::cout << std::endl;
				}
				else {
					// If we haven't printed 10 values, print a space
					std::cout << " ";
				}
		}



		//enqueue command to read from device to host memory
		queue.enqueueReadBuffer(readWriteBuffer, CL_TRUE, 0, sizeof(unsigned int) * 1024, result_int.data());
		std::cout << "\nContents of integer result : " << std::endl;
		for (int i = 0; i < 1024; i++)
		{
				std::cout << std::setw(5) << result_int[i] << " ";
				// Check if we have printed 10 values already
				if ((i + 1) % 10 == 0) {
					std::cout << std::endl;
				}
				else {
					// If we haven't printed 10 values, print a space
					std::cout << " ";
				}
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

