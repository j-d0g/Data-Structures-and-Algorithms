package comp26120;

import java.util.ArrayList;

public class darray implements set<String> {
    private ArrayList<String> list = new ArrayList<String>();
    private boolean sorted = false;

    SearchModes mode;
    int verbose;

    public darray(speller_config config) {
	mode = SearchModes.getSearchMode(config.mode);
	verbose = config.verbose;
    }

    public void insert(String value) {
        list.add(value);

        // changing the array means it may no longer be sorted
        sorted = false;
    }

    public boolean find(String value) {
        if (mode == SearchModes.LINEAR_SEARCH) {
            // TODO implemented linear search through list
            for (int i=0; i<list.size(); i++){
              if (list.get(i) == value){
                return true;
              }
              // return false;
            }
        } else { //Binary Search
            if (! sorted) {
                if (verbose > 0) {
                    System.out.println("Dynamic Array not sorted, sorting... \n");
                }

                sort(mode);
                if (verbose > 0) {
                    System.out.println("Dynamic Array sorted\n");
                }

                sorted = true;
            }
            // TODO implement binary search through list
            int r = list.size()-1;
            int l = 0;
            // int m = (l+r)/2;

            while (l <= r){
              int m = l + (r-l)/2; //remove

              if (list.get(m).equals(value)){
                return true;
              }

              else if (list.get(m).equals(value)){
                r = m;
                m=l+(r-l)/2; //remove
              }
              else {
                l = m;
                m = l + (r-l)/2; //remove
              }
              // m = (l+r)/2 (refactored out of else statements)
            }
        }
	return false;
    }

    public void print_set ()
    {
	System.out.print("DArray:\n");
	for(int i=0;i<list.size();i++){
	    System.out.format("\t%s\n",list.get(i));
	}
    }

    public void print_stats()
    {
	System.out.format("Dynamic array contains %d elements\n",list.size());
    }


    // Sorting Methods

    public enum SearchModes   { LINEAR_SEARCH,  // =0 in mode flag
				BINARY_SEARCH_ONE,  // = 1
				BINARY_SEARCH_TWO, // = 2
				BINARY_SEARCH_THREE, // =3
				BINARY_SEARCH_FOUR, // = 4
				BINARY_SEARCH_FIVE; // =5


	public static SearchModes getSearchMode(int i) {
	    switch (i) {
	    case 1:
		return BINARY_SEARCH_ONE;
	    case 2:
		return BINARY_SEARCH_TWO;
	    case 3:
		return BINARY_SEARCH_THREE;
	    case 4:
		return BINARY_SEARCH_FOUR;
	    case 5:
		return BINARY_SEARCH_FIVE;
	    default:
		return LINEAR_SEARCH;

	    }
	}


    };

    private void sort(SearchModes select){

	switch(select){
	case BINARY_SEARCH_ONE   : insertion_sort(); break;
	case BINARY_SEARCH_TWO   : quick_sort(); break;
	case BINARY_SEARCH_THREE :
	case BINARY_SEARCH_FOUR  :
	case BINARY_SEARCH_FIVE  :  // Add your own choices here
	default:
	    System.err.format("The value %d is not supported in sorting.c\n",
              select);
	    // Keep this exit code as the tests treat 23 specially
	    System.exit(23);
	}
    }


    // You may find this helpful
    // It swaps the element at index a and the element at index b in list
    private void swap(int a, int b)
    {
        String temp = list.get(a);
        list.set(a, list.get(b));
        list.set(b, temp);
    }


    private void insertion_sort(){
      // String[] A = new String[list.size()-1];
      // A[0] = list.get(0);
      // for (int i=1; i<list.size(); i++){
      //   String key = A[i];
      //   j = i-1;
      //   while (j>=0 && A[j] > key){
      //     A[j+1] = A[i]
      //   }
      //   sortedList[i] = list.get(i);
      // }
	System.err.format("Not implemented\n");
	System.exit(-1);
    }

    // Hint: you probably want to define a help function for the recursive call
    private void quick_sort() {
	System.err.format("Not implemented\n");
	System.exit(-1);
    }

}
