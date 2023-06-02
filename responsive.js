// Get the voting form and results elements
const votingForm = document.getElementById('votingForm');
const candidate1Result = document.getElementById('candidate1Result');
const candidate2Result = document.getElementById('candidate2Result');
const candidate3Result = document.getElementById('candidate3Result');

// Event listener for form submission
votingForm.addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent form submission

    // Get the selected candidate
    const selectedCandidate = document.querySelector('input[name="candidate"]:checked').value;

    // Simulate voting and update the results
    if (selectedCandidate === 'Peter Gregory Obi') {
        updateResult(candidate1Result);
    } else if (selectedCandidate === 'Bola Ahmed Tinubu') {
        updateResult(candidate2Result);
    } else if (selectedCandidate === 'Atiku Abubakar') {
        updateResult(candidate3Result);
    }

    // Clear the selected option
    document.querySelector('input[name="candidate"]:checked').checked = false;
});

// Function to update the result
function updateResult(candidateElement) {
    const currentVotes = parseInt(candidateElement.textContent) || 0;
    candidateElement.textContent = currentVotes + 1;
}
