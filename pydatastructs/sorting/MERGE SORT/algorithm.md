# Merge Sort Algorithm 

## **Merge Sort**

### **Input**  
An unsorted array `A` of size `n`.

### **Output**  
A sorted array `A` in ascending order.

---

## **Algorithm Description**

1. **Base Case**  
   - If the size of the array `A` is 1 or less, it is already sorted. Return the array.

2. **Divide Step**  
   - Find the middle index `mid` of the array:  
        $ \text{mid} = \text{start} + \frac{\text{end} - \text{start}}{2} $.
   - Split the array `A` into two subarrays:  
     - Left subarray: `A[start...mid]`  
     - Right subarray: `A[mid+1...end]`.

3. **Conquer Step**  
   - Recursively apply Merge Sort on the left subarray `A[start...mid]`.  
   - Recursively apply Merge Sort on the right subarray `A[mid+1...end]`.

4. **Merge Step**  
   - Merge the two sorted subarrays `A[start...mid]` and `A[mid+1...end]` into a single sorted array.  
     - Compare elements from both subarrays.  
     - Place the smaller element into the result array and move the pointer of the corresponding subarray.  
     - Repeat this process until all elements are merged.  
     - If one subarray is exhausted, append the remaining elements from the other subarray to the result.

5. **Return Step**  
   - Once all recursive calls are complete and merging is done, the entire array `A` will be sorted.

---

## **Time Complexity**

- **Best Case**: \(O(n \log n)\)  
  This occurs when the array is already sorted but still requires dividing and merging steps.

- **Average Case**: \(O(n \log n)\)  
  Most inputs result in balanced divisions and regular merging.

- **Worst Case**: \(O(n \log n)\)  
  Even in the worst-case scenario, all divisions and merging steps require consistent work.

---

## **Space Complexity**

- **Auxiliary Space**: \(O(n)\)  
  Merge Sort requires extra memory to store temporary arrays during the merging step.

---

## **Example Walkthrough**

### Input Array:  
`[38, 27, 43, 3, 9, 82, 10]`

### Step-by-Step Process:

1. **Initial Split**:  
   - Divide `[38, 27, 43, 3, 9, 82, 10]` into `[38, 27, 43]` and `[3, 9, 82, 10]`.

2. **Recursive Splitting**:  
   - `[38, 27, 43]` becomes `[38]`, `[27]`, and `[43]`.  
   - `[3, 9, 82, 10]` becomes `[3]`, `[9]`, `[82]`, `[10]`.

3. **Merging Subarrays**:  
   - Merge `[38]` and `[27]` into `[27, 38]`.  
   - Merge `[27, 38]` with `[43]` into `[27, 38, 43]`.  
   - Similarly, merge `[3]`, `[9]`, `[82]`, `[10]` into `[3, 9, 10, 82]`.

4. **Final Merge**:  
   - Merge `[27, 38, 43]` with `[3, 9, 10, 82]` into `[3, 9, 10, 27, 38, 43, 82]`.

### Output:  
`[3, 9, 10, 27, 38, 43, 82]`

---


