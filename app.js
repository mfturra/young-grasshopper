// Holistic calculate function
window.onload = () =>
    {
        // Activate tab onload
        document.getElementById("defaultOpen").click();

        // Acquire users general tuition cost
        document.querySelector('#yearly-cost').oninput = calculateCost;
        document.querySelector('#total-years').oninput = calculateCost;

        // Acquire users projected loan costs
        document.querySelector('#loan-interest-value').oninput = calculateCost;

        // Acquire users expected income
        document.querySelector('#num-semesters').oninput = calculateCost;
        document.querySelector('#hours-worked').oninput = calculateCost;
        document.querySelector('#hourly-rate').oninput = calculateCost;
    }

document.addEventListener('DOMContentLoaded', () => {
    const loanTypeSelection = document.getElementById('loan_type_selection');
    const undecidedLoanType = document.getElementById('hidden_loan_type_undecided');
    const fixedLoanType =     document.getElementById('hidden_loan_type_fixed');
    const variableLoanType =  document.getElementById('hidden_loan_type_variable')

    loanTypeSelection.addEventListener('change', function handleChange(event) {
        // Get selected value
        const selectedValue = event.target.value;
        
        // Hide all loan type sections
        undecidedLoanType.style.display =    'none';
        fixedLoanType.style.display =        'none';
        variableLoanType.style.display =     'none';

        // Reveal the selected loan type section
        if (selectedValue === '0') {
            undecidedLoanType.style.display = 'block';
        } else if (selectedValue === '1') {
            fixedLoanType.style.display = 'block';
        } else if (selectedValue === '2') {
            variableLoanType.style.display = 'block';
        }
})});

function openTab (event, tabName) {
    var i, tabcontent, tablinks;
    
    // Hide all element with class='tabcontent'
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("researchlinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show current tab and add "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    event.currentTarget.className += " active";

}

function researchingTabs (event, tabName) {
    var i, tabcontent, tablinks;
    
    // Hide all element with class='tabcontent'
    tabcontent = document.getElementsByClassName("research-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show current tab and add "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    event.currentTarget.className += " active";

}


function calculateCost() {
    var yearly_cost =   Number(document.getElementById('yearly-cost').value);
    var total_years =   Number(document.getElementById('total-years').value);
    var loan_interest = Number(document.getElementById('loan-interest-value').value);
    var num_semesters = Number(document.getElementById('num-semesters').value);
    var hours_worked =  Number(document.getElementById('hours-worked').value);
    var hourly_rate =   Number(document.getElementById('hourly-rate').value);
    var avg_weeks_in_semesters = 15;

    // Tuition Calculations
    var total_tuition_cost = yearly_cost * total_years;

    // Loan Calculations
    var total_loan_expenses = (total_tuition_cost * (loan_interest * 0.01)) + total_tuition_cost;

    // Expected Earnings Calculations
    var expected_weekly_earnings = hours_worked * hourly_rate;
    var expected_semester_earnings = expected_weekly_earnings * avg_weeks_in_semesters; // average number of weeks in semester
    var expected_degree_earnings = expected_semester_earnings * num_semesters;

    // Final Outstanding Degree Balance
    var final_degree_cost = total_loan_expenses - expected_degree_earnings;


    // Output values to console
    console.log(total_tuition_cost)
    console.log(total_loan_expenses)
    console.log(expected_weekly_earnings)
    console.log(expected_semester_earnings)
    console.log(expected_degree_earnings)
    console.log(final_degree_cost)


    // Show Total Cost of Tuition
    document.getElementById('general-tuition-cost').style.display = 'block';
    document.querySelector('#total_tuition_cost').innerHTML = total_tuition_cost;

    // Show Total Cost of Loan
    document.getElementById('tuition-loan1').style.display = 'block';
    document.querySelector('#loan_total_cost').innerHTML = total_loan_expenses;

    // Show Income Generated
    document.getElementById('weekly-earnings').style.display = 'block';
    document.querySelector('#expected_weekly_earnings').innerHTML = expected_weekly_earnings;

    document.getElementById('semester-earnings').style.display = 'block';
    document.querySelector('#expected_semester_earnings').innerHTML = expected_semester_earnings;

    document.getElementById('degree-earnings').style.display = 'block';
    document.querySelector('#expected_degree_earnings').innerHTML = expected_degree_earnings;    

    // Final Loan Cost minus Earnings
    document.getElementById('tuition-loan2').style.display = 'block';
    document.querySelector('#loan_total_cost2').innerHTML = total_loan_expenses;

    document.getElementById('degree-earnings2').style.display = 'block';
    document.querySelector('#expected_degree_earnings2').innerHTML = expected_degree_earnings;   

    document.getElementById('final-outstanding-balance').style.display = 'block';
    document.querySelector('#loan-minus-earnings').innerHTML = final_degree_cost;    
}