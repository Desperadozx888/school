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

	// declare data and memory objects
	std::vector<int> array(512);
	cl::Buffer arrayBuffer;

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
		if(!build_program(&program, &context, "task3.cl")) 
		{
			// if OpenCL program build error
			quit_program("OpenCL program build error.");
		}

		int num;
		std::cout << "Enter a number between 2 and 99: ";
		std::cin >> num;

		// Check if input is valid
		if (num < 2 || num > 99) {
			// if valid number was not entered
			quit_program("Invalid Number.");
		}

		// create a kernel
		kernel = cl::Kernel(program, "task3");

		// create command queue
		queue = cl::CommandQueue(context, device);

		// create buffers
		arrayBuffer = cl::Buffer(context, CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR,sizeof(int) * array.size(), array.data());

		// set kernel arguments
		kernel.setArg(0, arrayBuffer);
		kernel.setArg(1, num);

		cl::NDRange offset(0);
		cl::NDRange globalSize(array.size());	// work-units per kernel based on array size

		queue.enqueueNDRangeKernel(kernel, offset, globalSize);
			   
		std::cout << "Kernel enqueued." << std::endl;
		std::cout << "--------------------" << std::endl;

		// enqueue command to read from device to host memory
		queue.enqueueReadBuffer(arrayBuffer, CL_TRUE, 0, sizeof(int) * array.size(), array.data());

		// check the results
		// Display contents of host-side array
		for (int i = 0; i < array.size(); i++) {
			std::cout << std::setw(6) << array[i];

			// Check if we have printed 10 values already
			if ((i + 1) % 10 == 0) {
				std::cout << std::endl;
			}
		}

		// Add an extra newline after the final line, if needed
		if (array.size() % 10 != 0) {
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
