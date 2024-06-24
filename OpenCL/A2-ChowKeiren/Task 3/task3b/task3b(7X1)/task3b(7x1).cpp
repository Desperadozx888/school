#define CL_USE_DEPRECATED_OPENCL_2_0_APIS	// using OpenCL 1.2, some functions deprecated in OpenCL 2.0
#define __CL_ENABLE_EXCEPTIONS				// enable OpenCL exemptions

// C++ standard library and STL headers
#include <iostream>
#include <vector>
#include <fstream>

// OpenCL header, depending on OS
#ifdef __APPLE__
#include <OpenCL/cl.hpp>
#else
#include <CL/cl.hpp>
#endif

#include "common.h"
#include "bmpfuncs.h"

int main(void) 
{
	cl::Platform platform;			// device's platform
	cl::Device device;				// device used
	cl::Context context;			// context for the device
	cl::Program program;			// OpenCL program object
	cl::Kernel kernel;				// a single kernel object
	cl::CommandQueue queue;			// commandqueue for a context and device

	// declare data and memory objects
	unsigned char* inputImage;
	unsigned char* outputImage;
	unsigned char* tempImage;
	int imgWidth, imgHeight, imageSize;

	cl::ImageFormat imgFormat;
	cl::Image2D inputImgBuffer, outputImgBuffer, temp_buffer;

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
		if(!build_program(&program, &context, "task3b(7x1).cl")) 
		{
			// if OpenCL program build error
			quit_program("OpenCL program build error.");
		}

		// create a kernel
		kernel = cl::Kernel(program, "gaussian_Blurring");

		// create command queue
		queue = cl::CommandQueue(context, device);
		
		// read input image
		inputImage = read_BMP_RGB_to_RGBA("mandrill.bmp", &imgWidth, &imgHeight);

		// allocate memory for output image
		imageSize = imgWidth * imgHeight * 4;
		outputImage = new unsigned char[imageSize];
		tempImage = new unsigned char[imageSize];

		// image format
		imgFormat = cl::ImageFormat(CL_RGBA, CL_UNORM_INT8);

		// create image objects
		inputImgBuffer = cl::Image2D(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)inputImage);
		temp_buffer = cl::Image2D(context, CL_MEM_WRITE_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)tempImage);
		outputImgBuffer = cl::Image2D(context, CL_MEM_WRITE_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)outputImage);

		// enqueue command to read image from device to host memory
		cl::size_t<3> origin, region;
		origin[0] = origin[1] = origin[2] = 0;
		region[0] = imgWidth;
		region[1] = imgHeight;
		region[2] = 1;

		// set kernel arguments
		kernel.setArg(0, inputImgBuffer);
		kernel.setArg(1, temp_buffer);
		kernel.setArg(2, 1);
		
		// enqueue kernel
		cl::NDRange offset(0, 0);
		cl::NDRange globalSize(imgWidth, imgHeight);

		queue.enqueueNDRangeKernel(kernel, offset, globalSize);
		queue.enqueueReadImage(temp_buffer, CL_TRUE, origin, region, 0, 0, tempImage);
		std::cout << "Kernel enqueued & read." << std::endl;
		std::cout << "--------------------" << std::endl;

		// output results to image file
		write_BMP_RGBA_to_RGB("task3b(horizontal).bmp", tempImage, imgWidth, imgHeight);
		std::cout << "task3b(horizontal).bmp generated." << std::endl;
		std::cout << "--------------------" << std::endl;

		temp_buffer = cl::Image2D(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)tempImage);
		kernel.setArg(0, temp_buffer);
		kernel.setArg(1, outputImgBuffer);
		kernel.setArg(2, 0);
		queue.enqueueNDRangeKernel(kernel, offset, globalSize);
		queue.enqueueReadImage(outputImgBuffer, CL_TRUE, origin, region, 0, 0, outputImage);

		std::cout << "Kernel enqueued & read." << std::endl;
		std::cout << "--------------------" << std::endl;

		// output results to image file
		write_BMP_RGBA_to_RGB("task3b(horizontal&vertical).bmp", outputImage, imgWidth, imgHeight);
		std::cout << "task3b(horizontal&vertical).bmp generated." << std::endl;
		std::cout << "--------------------" << std::endl;

		std::cout << "Done." << std::endl;

		// deallocate memory
		free(inputImage);
		free(tempImage);
		free(outputImage);
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
