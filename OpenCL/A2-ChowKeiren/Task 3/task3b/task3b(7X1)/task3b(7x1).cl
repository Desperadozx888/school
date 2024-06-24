__constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | 
      CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST; 

// Gaussian blurring filter for single direction
__constant float GaussianBlurring[7] = {
    0.00598, 0.060626, 0.241843, 0.383103, 0.241843, 0.060626, 0.00598
};

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