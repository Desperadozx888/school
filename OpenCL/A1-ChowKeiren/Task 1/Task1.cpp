#define CL_USE_DEPRECATED_OPENCL_2_0_APIS	// using OpenCL 1.2, some functions deprecated in OpenCL 2.0
#define __CL_ENABLE_EXCEPTIONS				// enable OpenCL exemptions

// C++ standard library and STL headers
#include <iostream>
#include <vector>
#include <sstream>
#include <fstream>

// OpenCL header, depending on OS
#ifdef __APPLE__
#include <OpenCL/cl.hpp>
#else
#include <CL/cl.hpp>
#endif

#include "common.h"

int main(void)
{
	cl::Platform platform;		// device's platform
	cl::Device device;			// device used
	cl::Context context;		// context for the device
	cl::CommandQueue commandQueue; // Command Queue
	std::string outputString;	// string for output
	cl::Program program;			// OpenCL program object
	cl::Kernel kernel;				// a single kernel object
	unsigned int i;				// counter

	try {
		// select an OpenCL device
		if (!select_one_device(&platform, &device))
		{
			// if no device selected
			quit_program("Device not selected.");
		}

		context = cl::Context(device);

		std::vector<cl::Device> contextDevices = context.getInfo<CL_CONTEXT_DEVICES>();

		std::cout << "\nDevices in the context:" << std::endl;

		for (i = 0; i < contextDevices.size(); i++)
		{
			std::cout << "\nSelected device information: " << std::endl;
			cl::Platform platform = contextDevices[i].getInfo<CL_DEVICE_PLATFORM>();
			std::string platformName = platform.getInfo<CL_PLATFORM_NAME>();
			std::cout << "Platform: "<< platformName << std::endl;

			cl_device_type deviceType = contextDevices[i].getInfo<CL_DEVICE_TYPE>();
			std::cout << "Device type: " << (deviceType == CL_DEVICE_TYPE_CPU ? "CPU" : "GPU") << std::endl;

			outputString = contextDevices[i].getInfo<CL_DEVICE_NAME>();
			std::cout << "Device name: " << outputString << std::endl;

			cl_uint numComputeUnits = contextDevices[i].getInfo<CL_DEVICE_MAX_COMPUTE_UNITS>();
			std::cout << "Number of computing units: " << numComputeUnits << std::endl;

			size_t maxWorkGroupSize = contextDevices[i].getInfo<CL_DEVICE_MAX_WORK_GROUP_SIZE>();
			std::cout << "Maximum work group size: " << maxWorkGroupSize << std::endl;

			cl_uint maxWorkItemDimensions = contextDevices[i].getInfo<CL_DEVICE_MAX_WORK_ITEM_DIMENSIONS>();
			std::cout << "Maximum number of work item dimensions: " << maxWorkItemDimensions << std::endl;

			std::vector<size_t> maxWorkItemSizes = contextDevices[i].getInfo<CL_DEVICE_MAX_WORK_ITEM_SIZES>();
			std::cout << "Maximum work item sizes: ";
			for (size_t i = 0; i < maxWorkItemDimensions; i++) {
				std::cout << maxWorkItemSizes[i] << " ";
			}
			std::cout << std::endl;

			cl_uint preferredVectorWidth = contextDevices[i].getInfo<CL_DEVICE_PREFERRED_VECTOR_WIDTH_INT>();
			std::cout << "Preferred vector width for integers: " << preferredVectorWidth << std::endl;

			cl_ulong localMemSize = contextDevices[i].getInfo<CL_DEVICE_LOCAL_MEM_SIZE>();
			std::cout << "Local memory size: " << localMemSize << std::endl;

			std::string extensionsString = contextDevices[i].getInfo<CL_DEVICE_EXTENSIONS>();
			std::istringstream iss(extensionsString);
			std::vector<std::string> extensions(std::istream_iterator<std::string>{iss}, std::istream_iterator<std::string>());
			bool fp16Supported = false, fp64Supported = false, icdSupported = false;

			for (const auto& extension : extensions) {
				if (extension == "cl_khr_fp16") {
					fp16Supported = true;
				}
				else if (extension == "cl_khr_fp64") {
					fp64Supported = true;
				}
				else if (extension == "cl_khr_icd") {
					icdSupported = true;
				}
			}
			std::cout << "\nSelected device extension support:" << std::endl;
			std::cout << "cl_khr_fp16: " << (fp16Supported ? "Supported" : "Not supported") << std::endl;
			std::cout << "cl_khr_fp64: " << (fp64Supported ? "Supported" : "Not supported") << std::endl;
			std::cout << "cl_khr_icd: " << (icdSupported ? "Supported" : "Not supported") << std::endl;
			std::cout << "--------------------" << std::endl;
		}
		std::cout << "--------------------" << std::endl;

		// create command queue
		commandQueue = cl::CommandQueue(context, device);

		std::cout << "Command queue created." << std::endl;

		// build the program
		if (!build_program(&program, &context, "task1.cl"))
		{
			// if OpenCL program build error
			quit_program("OpenCL program build error.");
		}

		std::vector<cl::Kernel> allKernels;		// all kernels
		// create all kernels in the program
		program.createKernels(&allKernels);

		std::cout << "--------------------" << std::endl;
		std::cout << "Kernel names" << std::endl;

		// output kernel name for each index
		for (i = 0; i < allKernels.size(); i++) {
			outputString = allKernels[i].getInfo<CL_KERNEL_FUNCTION_NAME>();
			std::cout << "Kernel " << i << ": " << outputString << std::endl;
		}

		std::cout << "--------------------" << std::endl;
		
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