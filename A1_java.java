//Chow Keiren - 7233450
public class Main {

    public static void main(String[] args) {
        // female array & male array
        int Age_female[] = {20, 18, 23, 21, 19, 22, 17};
        int Age_male[] = {18, 18, 20, 23};

        //Create new class sort&Search
        com.company.SortAndSearch obj = new com.company.SortAndSearch();

        //Print Arrays
        System.out.print("Female: ");
        obj.printArray(Age_female);

        System.out.print("\nMale: ");
        obj.printArray(Age_male);

        //Sorting and Binary Search
        //Sorting
        obj.quickSort(Age_female, 0, Age_female.length - 1);
        System.out.printf("\nAnswer: ");
        //Binary Search
        for (int i = 0; i < Age_female.length; i++) {
            if (obj.binarySearch(Age_male, Age_female[i]) != -1)
                System.out.printf("%d ",Age_female[i]);
        }
    }
}


class SortAndSearch
{
    /* The main function that implements QuickSort()
    arr[] --> Array to be sorted,
    first --> Starting index,
    last --> Ending index */

    // A utility function to swap two elements
    static void swap(int[] arr, int i, int j)
    {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    /* This function takes last element as pivot, places
       the pivot element at its correct position in sorted
       array, and places all smaller (smaller than pivot)
       to left of pivot and all greater elements to right
       of pivot */
    static int partition(int[] arr, int low, int high)
    {

        // pivot
        int pivot = arr[high];

        // Index of smaller element and
        // indicates the right position
        // of pivot found so far
        int i = (low - 1);

        for(int j = low; j <= high - 1; j++)
        {

            // If current element is smaller
            // than the pivot
            if (arr[j] < pivot)
            {

                // Increment index of
                // smaller element
                i++;
                swap(arr, i, j);
            }
        }
        swap(arr, i + 1, high);
        return (i + 1);
    }

    /* The main function that implements QuickSort
              arr[] --> Array to be sorted,
              low --> Starting index,
              high --> Ending index
     */
    static void quickSort(int[] arr, int low, int high)
    {
        if (low < high)
        {

            // pi is partitioning index, arr[p]
            // is now at right place
            int pi = partition(arr, low, high);

            // Separately sort elements before
            // partition and after partition
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    int binarySearch(int arr[], int x)
    {
        int l = 0, r = arr.length - 1;
        while (l <= r) {
            int m = l + (r - l) / 2;

            // Check if x is present at mid
            if (arr[m] == x)
                return m;

            // If x greater, ignore left half
            if (arr[m] < x)
                l = m + 1;

                // If x is smaller, ignore right half
            else
                r = m - 1;
        }

        // if we reach here, then element was
        // not present
        return -1;
    }

    void printArray(int arr[])
    {
        int n = arr.length;
        for (int i=0; i<n; ++i)
            System.out.print(arr[i]+" ");
        System.out.println();
    }

}