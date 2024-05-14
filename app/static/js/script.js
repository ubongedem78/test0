document.addEventListener("DOMContentLoaded", function () {
  const attendanceData = document.getElementById("attendanceData");
  const downloadButton = document.getElementById("downloadButton");
  const currentDateElement = document.getElementById("currentDate");
  const recordNewAttendance = document.getElementById("recordAttendanceBtn");

  // Define the base URL
  const baseURL = "https://attendance-project-7hkr.onrender.com";

  function fetchAttendanceData() {
    axios
      .get(baseURL + "/attendance") // Prepend the base URL to the request URL
      .then((response) => {
        const data = response.data;
        // Clear previous attendance data
        attendanceData.innerHTML = "";

        // Add each attendance record to the table
        data.forEach((record) => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${record.name}</td>
            <td>${record.idNumber}</td>
            <td>${record.timestamp}</td>
          `;
          attendanceData.appendChild(row);
        });
      })
      .catch((error) => {
        console.error("Error fetching attendance data:", error);
      });
  }

  function downloadAttendancePDF() {
    // Send a request to the backend to generate the PDF file
    axios
      .get(baseURL + "/attendance/pdf", { responseType: "blob" })
      .then((response) => {
        // Create a Blob from the response data
        const blob = new Blob([response.data], { type: "application/pdf" });
        // Create a URL for the Blob
        const url = window.URL.createObjectURL(blob);
        // Create a link element
        const link = document.createElement("a");
        // Set the href attribute to the URL of the Blob
        link.href = url;
        // Set the download attribute to specify the filename
        link.download = "attendance_sheet.pdf";
        // Append the link to the document body
        document.body.appendChild(link);
        // Click the link to initiate the download
        link.click();
        // Remove the link from the document body
        document.body.removeChild(link);
        // Release the object URL
        window.URL.revokeObjectURL(url);
      })
      .catch((error) => {
        console.error("Error downloading attendance PDF:", error);
      });
  }

  function recordNewAttendanceForToday() {
    if (confirm("Are you sure you want to record new attendance?")) {
      axios
        .delete(baseURL + "/record_new_attendance")
        .then(() => {
          // Refresh the page after recording new attendance
          location.reload();
        })
        .catch((error) => {
          console.error("Error recording new attendance:", error);
        });
    }
  }

  function getCurrentDate() {
    const now = new Date();
    const formattedDate = now.toLocaleDateString("en-US", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    });
    currentDateElement.textContent = formattedDate;
  }

  // Fetch attendance data and populate the table
  fetchAttendanceData();
  getCurrentDate();

  setInterval(fetchAttendanceData, 60000);

  // Add event listener to the download button
  downloadButton.addEventListener("click", downloadAttendancePDF);
  recordNewAttendance.addEventListener("click", recordNewAttendanceForToday);
});
