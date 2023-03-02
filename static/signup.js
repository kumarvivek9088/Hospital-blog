const patient = document.getElementById("patient");
const doctor = document.getElementById("doctor");

patient.addEventListener("click",()=>{
	patient.classList.add("active");
	doctor.classList.remove("active");
})

doctor.addEventListener("click",()=>{
	doctor.classList.add("active");
	patient.classList.remove("active");
})