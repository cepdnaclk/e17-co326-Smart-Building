
# DATA ANALYSIS


## Energy optimization
![Alt text](./DATA%20ANALYSIS_1.jpg?raw=true "Title")
### <span style="color:skyblue"> Get data from database</span>
For the analysis of each collection, sufficient records should be there in the collection in order to analyze correctly. Therefore after the collection related to a relevant topic is filled with at least 10 records,all records are analyzed. 

### <span style="color:skyblue">Calculate threshold</span>
Basic idea of calculating the threshold value is to provide a parameter which can be used to control actuators.
In this case, values which is larger than mean + 1.5* standard deviation are considered as outliers. Therefore upon receiving value bigger than that, actuators should be controlled to lower the energy consumption.
```
if (arr.length < 10) {
    msg.payload = Infinity;
    return msg;
}
//handle insufficient data

let mean = arr.reduce((acc, curr) => {
    return acc + curr
}, 0) / arr.length;
 
// Assigning (value - mean) ^ 2 to every array item
arr = arr.map((k) => {
    return (k - mean) ** 2
})
 
// Calculating the sum of updated array
let sum = arr.reduce((acc, curr) => acc + curr, 0);
 
// Calculating the variance
let variance = sum / arr.length
 
// Returning the Standard deviation
let std = Math.sqrt(sum / arr.length)
let thresh = mean + 1.5 * std;
```
![Alt text](./DATA%20ANALYSIS_2.jpg?raw=true "Title")

###  <span style="color:skyblue">Store threshold value in a global variable </span>
 
global.set('floor0_thresh',msg.payload)
 
These values change when database entries are updated/new entries are inserted.

![Alt text](./DATA%20ANALYSIS_3.jpg?raw=true "Title")