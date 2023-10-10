// Holistic calculate function
window.onload = () =>
    {
        // Calculates the balance due to the student upon finishing their degree
        document.querySelector('#yearly-cost').oninput = calculateCost;
        document.querySelector('#total-years').oninput = calculateCost;
    }
  
function calculateCost() {
    var yearly_cost = Number(document.getElementById('yearly-cost').value);
    var total_years = Number(document.getElementById('total-years').value);
    var total_cost = yearly_cost * total_years;

    console.log(total_cost)

    // Show Total Cost of Tuition
    document.getElementById('outstanding-balance').style.display = 'block';
    document.querySelector('#total').innerHTML = total_cost;

    /*assign values of ID : yearly_cost, total_years and hours_worked to 
    variables for further calculations.*/



    // let yearly_cost = document.querySelector('#yearly-cost').value;
    // let total_years = document.querySelector('#total-years').value;


    // let hours_worked = document.querySelector('#hours-worked').value;
    // let semester_weeks = 15;
  
    // console.log(hours_worked);
    // /*if statement will work when user presses 
    //       calculate without entering values. */
    // //so will display an alert box and return.
    // if (yearly_cost === '' && total_years === 'Select') {
    //     alert("Please enter valid values");
    //     return;
    // }

    // if (yearly_cost === '' && hours_worked === 'Select' && hours-worked === 'Select') {
    //     alert("Please enter valid values");
    //     return;
    // }
  
    //now we are checking number of total_years 
    // if (total_years === '1')
    // //if there is only one total_years then we need not to display each.
    //     document.querySelector('#each').style.display = 'none';
    // else
    // //if there are more than one total_years we will display each.  
    //     document.querySelector('#each').style.display = 'block';
  
    /*calculating the tip by multiplying total-bill and number of
     hours_worked; then dividing it by number of total_years.*/
    //fixing the total yearly_cost upto 2 digits of decimal
    
    // let total = yearly_cost - (semester_weeks * hours_worked) / total_years;
    // component that includes scholarships

    // Round the value to 2 decimal places
    // total = total.toFixed(2);
  
    
}
