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
	unsigned char* noiseImage;
	unsigned char* outputImage;
	unsigned char* tempImage;
	unsigned char* outputLuminance;
	unsigned char* outputBlur;
	unsigned char* outputThres;
	unsigned char* outputAdd;
	unsigned char* outputMulti;

	int imgWidth, imgHeight, imageSize;

	cl::ImageFormat imgFormat;
	cl::Image2D inputImgBuffer, inputImgBuffer2, outputImgBuffer, temp_buffer;

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
		if(!build_program(&program, &context, "task3c.cl")) 
		{
			// if OpenCL program build error
			quit_program("OpenCL program build error.");
		}

		

		// create command queue
		queue = cl::CommandQueue(context, device);
		
		// read input image
		inputImage = read_BMP_RGB_to_RGBA("mandrill.bmp", &imgWidth, &imgHeight);
		noiseImage = read_BMP_RGB_to_RGBA("noise.bmp", &imgWidth, &imgHeight);

		// allocate memory for output image
		imageSize = imgWidth * imgHeight * 4;
		outputImage = new unsigned char[imageSize];
		tempImage = new unsigned char[imageSize];
		outputLuminance = new unsigned char[imageSize];
		outputBlur = new unsigned char[imageSize];
		outputThres = new unsigned char[imageSize];
		outputAdd = new unsigned char[imageSize];
		outputMulti = new unsigned char[imageSize];

		// image format
		imgFormat = cl::ImageFormat(CL_RGBA, CL_UNORM_INT8);


		// set offset and globalsize
		cl::NDRange offset(0, 0);
		cl::NDRange globalSize(imgWidth, imgHeight);

		// enqueue command to read image from device to host memory
		cl::size_t<3> origin, region;
		origin[0] = origin[1] = origin[2] = 0;
		region[0] = imgWidth;
		region[1] = imgHeight;
		region[2] = 1;


		//Task3c1
		// reset/create image buffer
		inputImgBuffer = cl::Image2D(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)inputImage);
		outputImgBuffer = cl::Image2D(context, CL_MEM_WRITE_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)outputLuminance);


		//set kernel and arg
		kernel = cl::Kernel(program, "luminance");
		kernel.setArg(0, inputImgBuffer);
		kernel.setArg(1, outputImgBuffer);
		
		//enqueue kernel & read for image
		queue.enqueueNDRangeKernel(kernel, offset, globalSize);
		queue.enqueueReadImage(outputImgBuffer, CL_TRUE, origin, region, 0, 0, outputLuminance);
		std::cout << "Kernel enqueued & read." << std::endl;
		std::cout << "--------------------" << std::endl;

		// output results to image file
		write_BMP_RGBA_to_RGB("Task3c.bmp", outputLuminance, imgWidth, imgHeight);
		std::cout << "Task3c1.bmp.bmp generated." << std::endl;
		std::cout << "--------------------" << std::endl;
		

		

		//Task3c2&3
		// reset/create image buffer
		inputImgBuffer = cl::Image2D(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)outputLuminance);
		temp_buffer = cl::Image2D(context, CL_MEM_WRITE_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)tempImage);
		outputImgBuffer = cl::Image2D(context, CL_MEM_WRITE_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)outputBlur);

		
		
		//set kernel and arg
		kernel = cl::Kernel(program, "gaussian_Blurring");
		kernel.setArg(0, inputImgBuffer);
		kernel.setArg(1, temp_buffer);
		kernel.setArg(2, 1);


		//enqueue kernel & read for image
		queue.enqueueNDRangeKernel(kernel, offset, globalSize);
		queue.enqueueReadImage(temp_buffer, CL_TRUE, origin, region, 0, 0, tempImage);
		std::cout << "Kernel enqueued & read." << std::endl;
		std::cout << "--------------------" << std::endl;

		// output results to image file
		write_BMP_RGBA_to_RGB("Task3c2.bmp", tempImage, imgWidth, imgHeight);
		std::cout << "Task3c2.bmp generated." << std::endl;
		std::cout << "--------------------" << std::endl;

		// read temp buffer
		temp_buffer = cl::Image2D(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)tempImage);

		kernel.setArg(0, temp_buffer);
		kernel.setArg(1, outputImgBuffer);
		kernel.setArg(2, 1);
		queue.enqueueNDRangeKernel(kernel, offset, globalSize);
		queue.enqueueReadImage(outputImgBuffer, CL_TRUE, origin, region, 0, 0, outputBlur);
		std::cout << "Kernel enqueued & read." << std::endl;
		std::cout << "--------------------" << std::endl;
		

		// output results to image file
		write_BMP_RGBA_to_RGB("Task3c3.bmp", outputBlur, imgWidth, imgHeight);
		std::cout << "Task3c3.bmp generated." << std::endl;
		std::cout << "--------------------" << std::endl;



		//Task3c4
		//declare lumi
		float lumi = 0.0;
		while (true) {
			std::cout << "Please enter the average lumi you want (range 0- 255): ";
			std::cin >> lumi;
			if (lumi <= 255 && lumi >= 0) {
				lumi /= 255;
				break;
			}
			else {
				std::cout << "Please enter a value between 0 ~ 255" << std::endl;
			}
		}

		
		std::cin.clear();
		std::cin.ignore(1000, '\n');
		
		
		// reset/create image buffer
		inputImgBuffer = cl::Image2D(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)outputLuminance);
		outputImgBuffer = cl::Image2D(context, CL_MEM_WRITE_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)outputThres);

		//set kernel and arg
		kernel = cl::Kernel(program, "blacken");
		kernel.setArg(0, inputImgBuffer);
		kernel.setArg(1, outputImgBuffer);
		kernel.setArg(2, lumi);

		queue.enqueueNDRangeKernel(kernel, offset, globalSize);
		queue.enqueueReadImage(outputImgBuffer, CL_TRUE, origin, region, 0, 0, outputThres);
		std::cout << "Kernel enqueued & read." << std::endl;
		std::cout << "--------------------" << std::endl;

		// output results to image file
		write_BMP_RGBA_to_RGB("Task3c4.bmp", outputThres, imgWidth, imgHeight);
		std::cout << "Task3c4.bmp generated." << std::endl;
		std::cout << "--------------------" << std::endl;

		//Task3c5
		// reset/create image buffer
		inputImgBuffer = cl::Image2D(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)outputBlur);
		inputImgBuffer2 = cl::Image2D(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)outputThres);
		outputImgBuffer = cl::Image2D(context, CL_MEM_WRITE_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)outputAdd);

		//set kernel and arg
		kernel = cl::Kernel(program, "combine_images");
		kernel.setArg(0, inputImgBuffer);
		kernel.setArg(1, inputImgBuffer2);
		kernel.setArg(2, outputImgBuffer);

		queue.enqueueNDRangeKernel(kernel, offset, globalSize);
		queue.enqueueReadImage(outputImgBuffer, CL_TRUE, origin, region, 0, 0, outputAdd);
		std::cout << "Kernel enqueued & read." << std::endl;
		std::cout << "--------------------" << std::endl;

		// output results to image file
		write_BMP_RGBA_to_RGB("Task3c5.bmp", outputAdd, imgWidth, imgHeight);
		std::cout << "Task3c5.bmp generated." << std::endl;
		std::cout << "--------------------" << std::endl;


		//Task3c6
		// reset/create image buffer
		inputImgBuffer = cl::Image2D(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)outputAdd);
		inputImgBuffer2 = cl::Image2D(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)noiseImage);
		outputImgBuffer = cl::Image2D(context, CL_MEM_WRITE_ONLY | CL_MEM_COPY_HOST_PTR, imgFormat, imgWidth, imgHeight, 0, (void*)outputMulti);

		//set kernel and arg
		kernel = cl::Kernel(program, "combine_images2");
		kernel.setArg(0, inputImgBuffer);
		kernel.setArg(1, inputImgBuffer2);
		kernel.setArg(2, outputImgBuffer);

		queue.enqueueNDRangeKernel(kernel, offset, globalSize);
		queue.enqueueReadImage(outputImgBuffer, CL_TRUE, origin, region, 0, 0, outputMulti);
		std::cout << "Kernel enqueued & read." << std::endl;
		std::cout << "--------------------" << std::endl;

		// output results to image file
		write_BMP_RGBA_to_RGB("Task3c6.bmp", outputMulti, imgWidth, imgHeight);
		std::cout << "Task3c6.bmp generated." << std::endl;
		std::cout << "--------------------" << std::endl;

		std::cout << "Done." << std::endl;

		// deallocate memory
		free(inputImage);
		free(noiseImage);
		free(tempImage);
		free(outputImage);
		free(outputLuminance);
		free(outputBlur);
		free(outputThres);
		free(outputAdd);
		free(outputMulti);
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
