#define CL_USE_DEPRECATED_OPENCL_2_0_APIS	// using OpenCL 1.2, some functions deprecated in OpenCL 2.0
#define __CL_ENABLE_EXCEPTIONS				// enable OpenCL exemptions

// C++ standard library and STL headers
#include <iostream>
#include <vector>
#include <cctype>
#include <fstream>
#include <iomanip>

// OpenCL header, depending on OS
#ifdef __APPLE__
#include <OpenCL/cl.hpp>
#else
#include <CL/cl.hpp>
#endif

#include "common.h"

char shift(char c, int n) {
	if (std::isalpha(c)) {
		char a = std::isupper(c) ? 'A' : 'a';
		return (c - a + n + 26) % 26 + a;
	}
	else {
		return c;
	}
}

// Function to encrypt a string
std::string encrypt(const std::string& plaintext, int n) {
	std::string ciphertext;
	for (char c : plaintext) {
		ciphertext += shift(c, n);
	}
	return ciphertext;
}

// Function to decrypt a string
std::string decrypt(const std::string& ciphertext, int n) {
	return encrypt(ciphertext, -n);
}

//task2a
void task2a(){
	std::ifstream inputFile("plaintext.txt");
	std::ofstream encryptedFile("task2a_ciphertext.txt");
	std::ofstream decryptedFile("task2a_decrypted.txt");

	if (!inputFile || !encryptedFile || !decryptedFile) {
		std::cerr << "Error opening files" << std::endl;
		return;
	}

	int n;
	while (true) {
		std::cout << "Task2A: Enter the shift value between 0 ~ 26: ";
		std::cin >> n;
		if (n <= 26 && n >= 0) {
			break;
		}
		else {
			std::cout << "Please enter a value between 0 ~ 26" << std::endl;
		}
	}
	std::cin.clear();
	std::cin.ignore(1000, '\n');

	std::string line;
	while (std::getline(inputFile, line)) {
		std::string encryptedLine = encrypt(line, n);
		encryptedFile << encryptedLine << "\n";

		std::string decryptedLine = decrypt(encryptedLine, n);
		decryptedFile << decryptedLine << "\n";
	}

	inputFile.close();
	encryptedFile.close();
	decryptedFile.close();

	std::cout << "task2a_ciphertext.txt generated." << std::endl;
	std::cout << "--------------------" << std::endl;

	std::cout << "task2a_decrypted.txt generated." << std::endl;
	std::cout << "--------------------" << std::endl;
}

int main(void)
{
	
	//declaring a number of data structures and variables
	cl::Platform platform;			// device's platform
	cl::Device device;				// device used
	cl::Context context;			// context for the device
	cl::Program program;			// OpenCL program object
	cl::Kernel encryptKernel, decryptKernel, encryptKernel2, decryptKernel2;				//4 kernel object
	cl::CommandQueue queue;			// commandqueue for a context and device

	// declare data and memory objects
	cl::Buffer inputBuffer, encryptedBuffer, decryptedBuffer;

	
	//task2a
	task2a();


	
	//Declare files
	std::ifstream inputFile("plaintext.txt");
	std::ofstream encryptedFile("task2b_ciphertext.txt");
	std::ofstream decryptedFile("task2b_decrypted.txt");
	std::ofstream encryptedFile2("task2c_ciphertext.txt");
	std::ofstream decryptedFile2("task2c_decrypted.txt");

	if (!inputFile || !encryptedFile || !decryptedFile) {
		std::cerr << "Error opening files" << std::endl;
		return 1;
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
		if (!build_program(&program, &context, "task2.cl"))
		{
			// if OpenCL program build error
			quit_program("OpenCL program build error.");
		}


		//Task2B
		int n;
		while (true) {
			std::cout << "Task2B: Enter the shift value between 0 ~ 26: ";
			std::cin >> n;
			if (n <= 26 && n >= 0) {
				break;
			}
			else {
				std::cout << "Please enter a value between 0 ~ 26" << std::endl;
			}
		}

		std::cin.clear();
		std::cin.ignore(1000, '\n');
		// create a kernel
		encryptKernel = cl::Kernel(program, "encrypt_Decrypt");
		decryptKernel = cl::Kernel(program, "encrypt_Decrypt");
		// create command queue
		queue = cl::CommandQueue(context, device);

		std::string line;
		while (std::getline(inputFile, line)) {
			if (line.empty()) {
				encryptedFile << '\n';
				decryptedFile << '\n';
				encryptedFile2 << '\n';
				decryptedFile2 << '\n';
				continue;
			}




			// create buffers

			inputBuffer = cl::Buffer(context, CL_MEM_READ_ONLY | CL_MEM_HOST_NO_ACCESS | CL_MEM_COPY_HOST_PTR, sizeof(char) * line.size(), const_cast<char*>(line.data()));
			encryptedBuffer = cl::Buffer(context, CL_MEM_READ_WRITE, sizeof(char) * line.size());
			decryptedBuffer = cl::Buffer(context, CL_MEM_WRITE_ONLY | CL_MEM_HOST_READ_ONLY, sizeof(char) * line.size());




			// Set kernel arguments and enqueue kernel for encryption.
			encryptKernel.setArg(0, inputBuffer);
			encryptKernel.setArg(1, encryptedBuffer);
			encryptKernel.setArg(2, n);
			queue.enqueueNDRangeKernel(encryptKernel, cl::NullRange, cl::NDRange(line.size()), cl::NullRange);


			// Set kernel arguments and enqueue kernel for decryption.
			decryptKernel.setArg(0, encryptedBuffer);
			decryptKernel.setArg(1, decryptedBuffer);
			decryptKernel.setArg(2, -n);
			queue.enqueueNDRangeKernel(decryptKernel, cl::NullRange, cl::NDRange(line.size()), cl::NullRange);

			// Read the results back from the device.
			char* encryptedData = new char[line.size()];
			char* decryptedData = new char[line.size()];
			queue.enqueueReadBuffer(encryptedBuffer, CL_TRUE, 0, sizeof(char) * line.size(), encryptedData);
			queue.enqueueReadBuffer(decryptedBuffer, CL_TRUE, 0, sizeof(char) * line.size(), decryptedData);

			// Write the results to the output files.
			encryptedFile.write(encryptedData, line.size());
			encryptedFile << '\n';
			decryptedFile.write(decryptedData, line.size());
			decryptedFile << '\n';
			

			//set kernel
			encryptKernel2 = cl::Kernel(program, "encrypt");
			decryptKernel2 = cl::Kernel(program, "decrypt");

			//reset buffer
			encryptedBuffer = cl::Buffer(context, CL_MEM_READ_WRITE, sizeof(char) * line.size());
			decryptedBuffer = cl::Buffer(context, CL_MEM_WRITE_ONLY | CL_MEM_HOST_READ_ONLY, sizeof(char) * line.size());

			// Set kernel arguments and enqueue kernel for encryption.
			encryptKernel2.setArg(0, inputBuffer);
			encryptKernel2.setArg(1, encryptedBuffer);
			queue.enqueueNDRangeKernel(encryptKernel2, cl::NullRange, cl::NDRange(line.size()), cl::NullRange);

			// Set kernel arguments and enqueue kernel for decryption.
			decryptKernel2.setArg(0, encryptedBuffer);
			decryptKernel2.setArg(1, decryptedBuffer);
			queue.enqueueNDRangeKernel(decryptKernel2, cl::NullRange, cl::NDRange(line.size()), cl::NullRange);

			// Read the results back from the device.
			char* encryptedData2 = new char[line.size()];
			char* decryptedData2 = new char[line.size()];
			queue.enqueueReadBuffer(encryptedBuffer, CL_TRUE, 0, sizeof(char)* line.size(), encryptedData2);
			queue.enqueueReadBuffer(decryptedBuffer, CL_TRUE, 0, sizeof(char)* line.size(), decryptedData2);

			// Write the results to the output files.
			encryptedFile2.write(encryptedData2, line.size());
			encryptedFile2 << '\n';
			decryptedFile2.write(decryptedData2, line.size());
			decryptedFile2 << '\n';

			

			// Free the allocated memory.
			delete[] encryptedData;
			delete[] decryptedData;
			delete[] encryptedData2;
			delete[] decryptedData2;
		}

		std::cout << "task2b_ciphertext.txt generated." << std::endl;
		std::cout << "--------------------" << std::endl;

		std::cout << "task2b_decrypted.txt generated." << std::endl;
		std::cout << "--------------------" << std::endl;

		std::cout << "task2c_ciphertext.txt generated." << std::endl;
		std::cout << "--------------------" << std::endl;

		std::cout << "task2c_decrypted.txt generated." << std::endl;
		std::cout << "--------------------" << std::endl;
		inputFile.close();
		encryptedFile.close();
		decryptedFile.close();
		encryptedFile2.close();
		decryptedFile2.close();

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

