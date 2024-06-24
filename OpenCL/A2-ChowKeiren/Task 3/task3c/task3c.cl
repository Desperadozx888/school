__constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | 
      CLK_ADDRESS_CLAMP | CLK_FILTER_NEAREST; 

// Gaussian blurring filter for single direction
__constant float GaussianBlurring[7] = {
    0.00598, 0.060626, 0.241843, 0.383103, 0.241843, 0.060626, 0.00598
};

__kernel void luminance(
    read_only image2d_t src_image,
    write_only image2d_t dst_image) {

    /* Get pixel coordinate */
    int2 coord = (int2)(get_global_id(0), get_global_id(1));

    /* Read pixel value */
    float4 pixel = read_imagef(src_image, sampler, coord);

    float luminance = 0.299 * pixel.x + 0.587 * pixel.y + 0.114 * pixel.z;

    /* Set red and blue channels to 0, and green channel to luminance */
    float4 nightVisionPixel = (float4)(0.0f, luminance, 0.0f, pixel.w);

    /* Write new pixel value to output */
    write_imagef(dst_image, coord, nightVisionPixel);
}


__kernel void gaussian_Blurring(read_only image2d_t src_image,
					write_only image2d_t dst_image,
					const int n) {

   /* Get work-item’s row and column position */
   int column = get_global_id(0); 
   int row = get_global_id(1);

   /* Accumulated pixel value */
   float4 sum = (float4)(0.0);

   /* Filter's current index */
   int filter_index =  0;

   int2 coord;
   float4 pixel;

   // Gaussian blurring filter for vertical pass
   if(n == 1){
        coord.y = row;
       /* Iterate over the columns */
        for (int j = -3; j <= 3; j++) {
        coord.x = column + j;
        /* Read value pixel from the image */
        pixel = read_imagef(src_image, sampler, coord);
        /* Accumulate weighted sum */
        sum.xyz += pixel.xyz * GaussianBlurring[filter_index++];
    
            }
        
    }else{
        // Gaussian blurring filter for horizontal pass
            /* Iterate over the rows */
            coord.x = column;
            for(int i = -3; i <= 3; i++) {
                coord.y =  row + i;
                /* Read value pixel from the temporary image */
                pixel = read_imagef(src_image, sampler, coord);
                /* Accumulate weighted sum */
                sum.xyz += pixel.xyz * GaussianBlurring[filter_index++];
                 }
            
        }
   /* Write new pixel value to output */
   coord = (int2)(column, row); 
   write_imagef(dst_image, coord, sum);
}

__kernel void blacken(read_only image2d_t src_image,
					write_only image2d_t dst_image,
					float threshold) {

	/* Get pixel coordinate */
    int2 coord = (int2)(get_global_id(0), get_global_id(1));

    /* Read pixel value */
    float4 pixel = read_imagef(src_image, sampler, coord);

    /* Calculate luminance value */
    float luminance = 0.299f * pixel.x + 0.587f * pixel.y + 0.114f * pixel.z;

    /* Apply thresholding */
    float4 output_pixel = (luminance > threshold) ? pixel : (float4)(0.0f, 0.0f, 0.0f, 1.0f);

    /* Write new pixel value to output */
    write_imagef(dst_image, coord, output_pixel);
}

__kernel void combine_images(read_only image2d_t src_image,
                             read_only image2d_t src_image2,
                             write_only image2d_t dst_image) {

   /* Get pixel coordinate */
   int2 coord = (int2)(get_global_id(0), get_global_id(1));

   /* Read pixel values from the source images */
   float4 pixel1 = read_imagef(src_image, sampler, coord);
   float4 pixel2 = read_imagef(src_image2, sampler, coord);

   /* Combine pixel values */
   float4 combined_pixel = pixel1 + pixel2;
   
   /* Ensure that the combined pixel values do not exceed the maximum color value */
   combined_pixel = clamp(combined_pixel, 0.0f, 1.0f);

   /* Write the new pixel value to the output image */
   write_imagef(dst_image, coord, combined_pixel);
}


__kernel void combine_images2(read_only image2d_t src_image,
                             read_only image2d_t noise,
                             write_only image2d_t dst_image) {

   /* Get pixel coordinate */
   int2 coord = (int2)(get_global_id(0), get_global_id(1));

   /* Read pixel values from the source images */
   float4 pixel1 = read_imagef(src_image, sampler, coord);
   float4 pixel2 = read_imagef(noise, sampler, coord);

   /* Combine pixel values by multiplying them */
   float4 combined_pixel = pixel1 * pixel2;
   
   /* Ensure that the combined pixel values do not exceed the maximum color value */
   combined_pixel = clamp(combined_pixel, 0.0f, 1.0f);

   /* Write the new pixel value to the output image */
   write_imagef(dst_image, coord, combined_pixel);
}
